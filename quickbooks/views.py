import os
import logging as log
import re

from django.db.models import get_app, get_models
from django.shortcuts import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from lxml import etree

from quickbooks.models import QWCTicket
from quickbooks.models import DjangoUserProfile
from quickbooks.models import ReceiveResponse
from quickbooks.models import MessageQue

from quickbooks.qwc_xml import authenticated
from quickbooks.qwc_xml import failed
from quickbooks.qwc_xml import close_connection
from quickbooks.qwc_xml import processed
from quickbooks.qwc_xml import process_failed
from quickbooks.qwc_xml import qrequest

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


@csrf_exempt
def show_wsdl(request):
    contents = ""
    with(open(os.path.join(settings.BASE_DIR, 'quickbooks', 'qb.wsdl'), 'r')) as f:
        contents = f.read()
    return HttpResponse(contents, content_type='text/xml')


@csrf_exempt
def home(request):
    c = request.body
    # logging.debug(c)
    if request.method == "GET":
        logging.debug("kdhohdjdhdj")
        return HttpResponse('The request need to be POST')
    url = 'file://' + os.path.join(settings.BASE_DIR, 'quickbooks', 'qb.wsdl')

    # FIXME: huge_tree allow this thing to eat up your memory!
    parser = etree.XMLParser(huge_tree=True)
    contents = etree.parse(request, parser)
    root = contents.getroot()

    # We need to listen to authenticate, token or error.
    cont = root[0][0]
    ticket = cont.find(tag('ticket'))
    if cont.tag == tag('authenticate', 'intuit'):
        logging.debug('Authentication call detected')
        username = cont.find(tag('strUserName')).text
        password = cont.find(tag('strPassword')).text

        # Authenticate with database
        a = authenticate(username=username, password=password)
        if a:
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
                profile = DjangoUserProfile.objects.create(user=t.user)
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
        if send_request != None:
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
                return HttpResponse(close_connection % ("Finished!"), content_type='text/xml')

            return HttpResponse(close_connection % (100), content_type='text/xml')
        else:
            logging.debug("sendRequestXML Not detected")

        if receive_response != None:
            logging.debug(receive_response.text)
            tick = QWCTicket.objects.get(ticket=ticket.text)
            response = receive_response[1].text
            request_id = None
            try:
                receive_plain = etree.fromstring(response)
                receive_query_name = etree.fromstring(response)[0][0].tag[:-2]
            except Exception, e:
                logging.debug("Error it apears like response is empty")
                logging.error(e)
            if response != None:
                logging.debug('response is %s' % (response))
                resp = ReceiveResponse.objects.create(ticket=tick, response=response, name=receive_query_name)
                # Let's try to do something with this response now!
                qn = re.sub("([A-Z])", " \g<0>", receive_query_name).split(" ")[1]
                logging.info("THAT IS ===> %s" %(qn))
                if qn in QBXML().names:
                    # does that model name  exists ? if so enter data in that thing
                    ms = get_models()
                    m = None
                    for model in ms:
                        if model.__name__ == 'QB' + qn:
                            m = model
                    if m != None:
                        logging.debug("Model does exist")
                        items = receive_plain[0][0]
                        logging.debug('items are ==> %s', str(items))
                        for item in items:
                            t = {}
                            for it in item:
                                logging.debug('items => %s' %(str(it.tag)))
                                if it.tag == 'ListID':
                                    list_id = it.text
                                    logging.debug("listid is %s" %(str(list_id)))
                                t.update({convert(it.tag): it.text})
                            # but first.. does that already exists ?
                            logging.debug("qbwc %s" %(t))
                            if list_id:
                                m.objects.update_or_create(list_id=t['list_id'], defaults=t)
                            else:
                                logging.debug("no list_id strange ?? ")
                            # Do something if this response was a Response , maybe update the database with relationship?
                            logging.debug('Check if we need to do something after handling with a response')

                            # First get related objects of the selected model hope it is only one.
                            request_id = receive_plain[0][0].attrib['requestID']
                            if list_id and request_id:
                                logging.debug(request_id)
                                for md in m._meta.get_all_related_objects():
                                    logging.debug('Looking for models')
                                    logging.debug(md)
                                    mod = md.model.objects.filter(pk=request_id)[0]
                                    if mod:
                                        mod.quickbooks = m.objects.get(pk=list_id)
                                        mod.save()

                            else:
                                logging.debug('Nothing found in settings')

                    else:
                        if settings.DEBUG:

                            logging.debug("Model does not exist")
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

def get_company_file(request):
    response = HttpResponse(generate_qbc_file(), content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename="quickbooks.QWC"'
    return response