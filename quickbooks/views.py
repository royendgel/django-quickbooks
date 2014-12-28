import os
import logging as log

from django.shortcuts import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from lxml import etree

from quickbooks.models import QWCTicket
from quickbooks.models import UserProfile
from quickbooks.models import ReceiveResponse
from quickbooks.models import MessageQue

from quickbooks.qwc_xml import authenticated
from quickbooks.qwc_xml import failed
from quickbooks.qwc_xml import close_connection
from quickbooks.qwc_xml import processed
from quickbooks.qwc_xml import process_failed
from quickbooks.qwc_xml import qrequest

from quickbooks.uttils import tag
from quickbooks.uttils import xml_soap

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
    contents = etree.parse(request)
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
            logging.debug('Valid Authentication username and password user: %s' %(a.username))
            # everything active need to be inactive
            ac = QWCTicket.objects.filter(user=a, active=True)
            if ac != None:
                for ca in ac:
                    ca.active = False
                    ca.save()
            ti = QWCTicket.objects.create(user=a)
            logging.debug('Ticket has been created ticket: %s' %(ti.ticket))
            # resp = client.service.authenticateResponse(ti.ticket).envelope
            s = ''
            try:
                s = a.userprofile.company_file
                logging.debug('company file detected: %s' %(s))
            except:
                logging.debug('Company file not found')
            logging.debug("Authenticated xml message sent")
            return HttpResponse(authenticated %(ti.ticket, s), content_type='text/xml')
        else:
            logging.debug('invalid user detected username: %s password %s' %(username, password))
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

        logging.debug("Dealing with ticket: %s" %(ticket.text))
        receive_response = root[0].find(tag('receiveResponseXML'))
        logging.debug(root.findall(tag('receiveResponseXML')))
        logging.debug(root.find(tag('receiveResponseXML')))
        logging.debug(root.findtext(tag('receiveResponseXML')))
        send_request = root[0].find(tag('sendRequestXML'))
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
                return HttpResponse(qrequest %(xml_soap(ms)), content_type='text/xml')
            else:
                logging.debug("No message in messageQue")
                logging.debug('Finished')
                return HttpResponse(close_connection % ("Finished!"), content_type='text/xml')

            return HttpResponse(close_connection %(100), content_type='text/xml')
        else:
            logging.debug("sendRequestXML Not detected")

        if receive_response != None:
            logging.debug(receive_response.text)
            tick = QWCTicket.objects.get(ticket=ticket.text)
            response = receive_response[1].text
            if response != None:
                logging.debug('response is %s' %(response))
                ReceiveResponse.objects.create(ticket=tick, response=receive_response[1].text)
                return HttpResponse(close_connection %('ssss'), content_type='text/xml')
        else:
            logging.debug("This message does not contain response")

    return HttpResponse(close_connection %('closed'), content_type='text/xml')