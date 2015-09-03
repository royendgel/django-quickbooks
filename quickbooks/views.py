import os
import logging as log
import re
from pprint import pprint

from django.db.models import get_app, get_models
from django.shortcuts import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.db.models.fields.related import OneToOneField, ForeignKey
from django.views.generic import View
from django.utils import timezone
import django.dispatch

from lxml import etree

from quickbooks.models import QWCTicket
from quickbooks.models import UserProfile
from quickbooks.models import ReceiveResponse
from quickbooks.models import MessageQue
from quickbooks.models import ResponseError
from quickbooks.models import QWCMessage

from quickbooks.qwc_xml import *

from quickbooks.decorators import catch_errors

from quickbooks.uttils import convert
from quickbooks.uttils import xml_soap
from quickbooks.uttils import generate_qbc_file
from quickbooks.uttils import tag

from quickbooks.qbxml import QBXML
from quickbooks.settings import QUICKBOOKS_RESPONSE

QSETTINGS = None
if hasattr(settings, 'QUICKBOOKS_RESPONSE'):
    QSETTINGS = settings.QUICKBOOKS_RESPONSE
else:
    QSETTINGS = QUICKBOOKS_RESPONSE

logging = log.getLogger(__name__)

request_received = django.dispatch.Signal(providing_args=["request_type", "root", "qbxml"])
session_started = django.dispatch.Signal(providing_args=["start_time", "authenticated"])
session_ended = django.dispatch.Signal(providing_args=["end_time", "result", "message"])

@csrf_exempt
def show_wsdl(request):
    contents = ""
    with(open(os.path.join(settings.BASE_DIR, 'quickbooks', 'qb.wsdl'), 'r')) as f:
        contents = f.read()
    return HttpResponse(contents, content_type='text/xml')

def get_model(qn):
    ms = get_models()
    m = None
    for model in ms:
        if model.__name__ == 'QB' + qn:
            m = model
    return m

def has_m2m_field(m, field_name):
    return field_name in [f.name for f in m._meta.many_to_many]


def get_related_field(m, field_name):
    return m._meta.get_field(field_name)

def has_related_field(m, field_name):
    return field_name in [f.name for f in m._meta.fields if isinstance(f, ForeignKey)]    

def get_related_fk_model(m, field_name):
    return m._meta.get_field(field_name).rel.to

def has_field(m, field_name):
    """ Has a regular field (not relation)
    """
    return field_name in [f.name for f in m._meta.fields if not isinstance(f, ForeignKey)]

def get_request_type(root):
    request_types = [
        REQUEST_AUTHENTICATE, 
        REQUEST_RECEIVE_REQUEST,
        REQUEST_SEND_REQUEST,
        REQUEST_CLOSE_CONNECTION,
        REQUEST_CONNECTION_ERROR,
        REQUEST_GET_INTERACTIVE_URL,
        REQUEST_INTERACTIVE_DONE,
        REQUEST_GET_LAST_ERROR,
        REQUEST_SERVER_VERSION,
        REQUEST_CLIENT_VERSION
    ]
    cont = root[0][0]
    for request_type in request_types:
        if cont.tag == tag(request_type, 'intuit'):
            return request_type
    return None


@csrf_exempt
@catch_errors
def home(request):
    c = request.body
    logging.debug(c)
    if request.method == "GET":
        logging.debug("kdhohdjdhdj")
        return HttpResponse('The request need to be POST')
    url = 'file://' + os.path.join(settings.BASE_DIR, 'quickbooks', 'qb.wsdl')

    # FIXME: huge_tree allow this thing to eat up your memory!
    parser = etree.XMLParser(huge_tree=True)
    contents = etree.parse(request, parser)
    root = contents.getroot()
    request_type = get_request_type(root)
    # Log the message
    QWCMessage.objects.create(request_type=request_type, 
        message=etree.tostring(root, pretty_print=True)
    )
    print('REQUEST TYPE RECEIVED IS: %s ========================================' % (request_type or 'Unkown'))
    if request_type:
        print etree.tostring(root, pretty_print=True)   

    # Dispatch the signal
    qbxml = None
    if request_type == REQUEST_RECEIVE_REQUEST:
        qbxml = etree.fromstring(root[0].find(tag('receiveResponseXML'))[1].text)
    request_received.send(sender=type(request), request_type=request_type, root=root, qbxml=qbxml)

    if request_type == REQUEST_GET_LAST_ERROR:
        last_error = ResponseError.get_last_error()
        message = last_error.content if last_error else ""
        return HttpResponse(get_last_error % message, content_type='text/xml')

    # We need to listen to authenticate, token or error.
    cont = root[0][0]
    ticket = cont.find(tag('ticket'))
    if request_type == REQUEST_AUTHENTICATE:
        logging.debug('Authentication call detected')
        username = cont.find(tag('strUserName')).text
        password = cont.find(tag('strPassword')).text

        # Authenticate with database
        a = authenticate(username=username, password=password)
        if a:
            session_started.send(sender=type(request), start_time=timezone.localtime(timezone.now()), authenticated=True)
            logging.debug('Valid Authentication username and password user: %s' % (a.username))
            # everything active need to be inactive
            ac = QWCTicket.objects.filter(user=a, active=True)
            if ac != None:
                for ca in ac:
                    ca.active = False
                    ca.save()
            ti = QWCTicket.objects.create(user=a)
            logging.debug('Ticket has been created ticket: %s' % (ti.ticket))
            # resp = client.service.authenticateResponse(ti.ticket).envelope
            s = ''
            try:
                s = a.userprofile.company_file
                logging.debug('company file detected: %s' % (s))
            except:
                logging.debug('Company file not found')
            logging.debug("Authenticated xml message sent")
            return HttpResponse(authenticated % (ti.ticket, s), content_type='text/xml')
        else:
            logging.debug('invalid user detected username: %s password %s' % (username, password))
            session_started.send(sender=type(request), start_time=timezone.localtime(timezone.now()), authenticated=False)
            session_ended.send(sender=type(request), end_time=timezone.localtime(timezone.now()), result=False, message="Invalid username or password supplied")
            return HttpResponse(failed, content_type='text/xml')

    if ticket is not None:
        t = QWCTicket.objects.get(ticket=ticket.text)
        if t is not None:
            # all_fancy_stuff = cont.find(tag('strHCPResponse')).text
            profile = None
            company_file_location = cont.find(tag('strCompanyFileName'))

            # update the company_file location if it's not updated.
            try:
                profile = t.user.userprofile
            except Exception as e:
                profile = UserProfile.objects.create(user=t.user)
            if company_file_location is not None:
                if company_file_location != profile.company_file:
                    profile.company_file = company_file_location.text
                    profile.save()

        logging.debug("Dealing with ticket: %s" % (ticket.text))
        receive_response = root[0].find(tag('receiveResponseXML'))
        logging.debug(root.findall(tag('receiveResponseXML')))
        logging.debug(root.find(tag('receiveResponseXML')))
        logging.debug(root.findtext(tag('receiveResponseXML')))
        send_request = root[0].find(tag('sendRequestXML'))
        list_id = None
        logging.debug('LIST ID ====>> %s', str(list_id))
        logging.debug(send_request)
        if request_type == REQUEST_SEND_REQUEST:
            logging.debug("sendRequestXML detected tags will appear below:")
            for child in send_request:
                logging.debug(child.tag)
            mq = MessageQue.objects.filter(user=t.user, active=True)
            if len(mq) != 0:
                logging.debug("MessageQue has one or more messages awaiting")
                m = mq[0]
                ms = m.message
                logging.debug("sending message in que: %s" % (m.id))

                # Mark message as consumed
                m.active = False
                m.save()
                return HttpResponse(qrequest % (xml_soap(ms)), content_type='text/xml')
            else:
                logging.debug("No message in messageQue")
                logging.info("activating everything that is set to repeat")
                logging.debug('Finished')
                repeats = MessageQue.objects.filter(repeat=True, active=False)
                for repeat in repeats:
                    repeat.active = True
                    repeat.save()
                # delete tickets and messages that are not in use:
                MessageQue.objects.filter(repeat=False, active=False).delete()
                QWCTicket.objects.filter(active=False).delete()
                session_ended.send(sender=type(request), end_time=timezone.localtime(timezone.now()), result=True, message="All messages processed successfully")
                return HttpResponse(close_connection % ("Finished!"), content_type='text/xml')

            return HttpResponse(close_connection % (100), content_type='text/xml')
        else:
            logging.debug("sendRequestXML Not detected")

        if request_type == REQUEST_RECEIVE_REQUEST:
            logging.debug(receive_response.text)
            tick = QWCTicket.objects.get(ticket=ticket.text)
            response = receive_response[1].text
            request_id = None
            try:
                receive_plain = etree.fromstring(response)
                receive_query_name = receive_plain[0][0].tag[:-2]
            except Exception, e:
                logging.debug("Error it apears like response is empty")
                logging.error(e)
            if response != None:
                logging.debug('response is %s' % (response))
                resp = ReceiveResponse.objects.create(ticket=tick, response=response, name=receive_query_name)
                # Let's try to do something with this response now!
                qn = "".join(re.sub("([A-Z])", " \g<0>", receive_query_name).split(" ")[1:-1])
                print("RESPONSE TYPE: %s" % receive_query_name)
                logging.info("THAT IS ===> %s" %(qn))
                if qn in QBXML.NAMES:
                    # does that model name  exists ? if so enter data in that thing
                    m = get_model(qn)
                    if m != None:
                        logging.debug("Model does exist")
                        print("Model exists for %s" % qn)
                        items = receive_plain[0][0]
                        logging.debug('items are ==> %s', str(items))
                        print('items are ==> %s', str(items))
                        list_id, txn_id = None, None
                        ids = {}
                        for item in items:
                            t = {}
                            m2m_data = {}
                            for it in item:
                                converted_tag = convert(it.tag)
                                logging.debug('items => %s' %(str(it.tag)))
                                if it.tag == 'ListID':
                                    list_id = it.text
                                    ids["list_id"] = list_id
                                    logging.debug("listid is %s" %(str(list_id)))
                                elif it.tag == 'TxnID':
                                    txn_id = it.text
                                    ids["txn_id"] = txn_id
                                if len(it):
                                    # This is a nested item
                                    if has_related_field(m, converted_tag):
                                        print("HEYYY %s has %s as a related field" % (m, converted_tag))
                                        nested_attr = {}
                                        related_model = get_related_fk_model(m, converted_tag)
                                        related_field = get_related_field(m, converted_tag)
                                        related_name = related_field.related_query_name()
                                        nested_list_ids = {}
                                        for itt in it:
                                            converted_nested_tag = convert(itt.tag)
                                            if itt.tag == "ListID":
                                                print("Found nested list ID: %s" % itt.text)
                                                nested_list_ids[converted_nested_tag] = itt.text
                                            if has_field(related_model, converted_nested_tag): # only save fields, not fk fields or m2m fields
                                                nested_attr.update({converted_nested_tag: itt.text})
                                            else:
                                                print("%s isn't a normal field on %s, it maybe a relation... we're not currently doing nested relations tho..." % (converted_nested_tag, related_model))
                                        if not nested_list_ids and ids:
                                            # If the nested model doesn't have a ListID on it, try and find it by the relationship
                                            for _id, val in ids.items():
                                                nested_list_ids["%s__%s" % (related_name, _id)] = val
                                        if nested_attr and nested_list_ids:
                                            related_obj, created = related_model.objects.update_or_create(defaults=nested_attr, **nested_list_ids)
                                            t[converted_tag] = related_obj
                                    elif has_m2m_field(m, converted_tag):
                                        print("HEYYY %s has a M2M field" % converted_tag)
                                elif has_field(m, converted_tag):
                                    t.update({converted_tag: it.text})
                            # but first.. does that already exists ?
                            logging.debug("qbwc %s" %(t))
                            print("Will look for objects matching %s and update with the following attributes... " % ids)
                            pprint(t)
                            if ids:
                                obj, created = m.objects.update_or_create(defaults=t, **ids)
                                # Deal with the m2m models 
                            else:
                                logging.debug("no list_id or txn_id strange ?? ")
                            # Do something if this response was a Response , maybe update the database with relationship?
                            logging.debug('Check if we need to do something after handling with a response')

                            # First get related objects of the selected model hope it is only one.
                            request_id = receive_plain[0][0].attrib['requestID']
                            if ids and request_id:
                                logging.debug(request_id)
                                for md in m._meta.get_all_related_objects():
                                    logging.debug('Looking for models')
                                    logging.debug(md)
                                    try:
                                        mod = md.model.objects.filter(pk=request_id)[0]
                                    except IndexError:
                                        mod = None
                                    if mod:
                                        pk = ids.get(ids.keys()[0])
                                        if pk:
                                            mod.quickbooks = m.objects.get(pk=pk)
                                        mod.save()
                                    else:
                                        print("No model found to object")
                            else:
                                logging.debug('Nothing found in settings')

                    else:
                        if settings.DEBUG:

                            logging.debug("Model does not exist")
                            print('No model exists for %s' % qn)
                            # this model does not exist, what about making a file with all it's data maybe we can use it
                            # Dump it only if debug is set to True (DEBUG=True)
                            # if it does not catch here remember to look in qbxml().names
                            items = receive_plain[0][0]
                            with(open(os.path.join(settings.BASE_DIR, '..', str(qn) + '_model.txt'), 'w+')) as f:
                                f.write("class QB%s(models.Model):\n" %(qn))
                                keys = []
                                for item in items:
                                    t = {}
                                    for it in item:
                                        keys.append(it.tag)
                                for key in set(keys):
                                    if key == 'ListID':
                                        f.write("    %s = models.CharField(max_length=2500, primary_key=True) # %s\n" %(convert(key), key))
                                    else:
                                        f.write("    %s = models.CharField(max_length=2500, blank=True, null=True) # %s\n" %(convert(key), key))
                                logging.debug('writed the class in a txt file please copy and paste it in your models')



                return HttpResponse(close_connection % ('ssss'), content_type='text/xml')
        else:
            logging.debug("This message does not contain response")
    logging.info("Calling close")
    return HttpResponse(close_connection % ('closed!!!'), content_type='text/xml')

def get_items():
    for item in items:
        for element in item:
            tag_set.append(element.tag)
            for tag in element:
                tag_set.append(tag.tag)

    all_tags = set(tag_set)
    for t in all_tags:
        with(open('play_c_fields.py', 'a+')) as f:
            print(t)
            f.write("%s = models.CharField(max_length=255, blank=True, null=True) # %s \n" %(convert(t), t))




def welcome(request):
    return HttpResponse('<h1>Use /quickbooks</h1>', content_type='text/html')

class GetQWCFileView(View):

    def get_qwc_file(self):
        return generate_qbc_file()

    def get(self, request):
        response = HttpResponse(self.get_qwc_file(), content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename="quickbooks.QWC"'
        return response
