import os
import logging
from django.shortcuts import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from suds.client import Client
from suds.plugin import MessagePlugin
from lxml import etree
from quickbooks.models import QWCTicket
from quickbooks.models import UserProfile
from quickbooks.models import ReceiveResponse

from quickbooks.qwc_xml import authenticated
from quickbooks.qwc_xml import failed
from quickbooks.qwc_xml import close_connection
from quickbooks.qwc_xml import processed
from quickbooks.qwc_xml import process_failed
from quickbooks.qwc_xml import do_for_me

from quickbooks.uttils import tag

# This is to log every message to the console.
class LogPlugin(MessagePlugin):
  def sending(self, context):
    print(str(context.envelope))
  def received(self, context):
    print(str(context.reply))


@csrf_exempt
def show_wsdl(request):
    contents = ""
    with(open(os.path.join(settings.BASE_DIR, 'quickbooks', 'qb.wsdl'), 'r')) as f:
        contents = f.read()
    return HttpResponse(contents, content_type='text/xml')

@csrf_exempt
def home(request):
    c = request.body
    if request.method == "GET":
        return HttpResponse('The request need to be POST')
    url = 'file://' + os.path.join(settings.BASE_DIR, 'quickbooks', 'qb.wsdl')
    client = Client(url, plugins=[LogPlugin()])
    client.set_options(nosend=True)
    contents = etree.parse(request)
    root = contents.getroot()

    # We need to listen to authenticate, token or error.
    cont = root[0][0]
    ticket = cont.find(tag('ticket'))
    if cont.tag == tag('authenticate', 'intuit'):
        username = cont.find(tag('strUserName')).text
        password = cont.find(tag('strPassword')).text
        # Authenticate with database
        a = authenticate(username=username, password=password)
        if a:
            # everything active need to be inactive

            ac = QWCTicket.objects.filter(user=a, active=True)
            if ac != None:
                for ca in ac:
                    ca.active = False
                    ca.save()
            ti = QWCTicket.objects.create(user=a)
            # resp = client.service.authenticateResponse(ti.ticket).envelope
            s = ''
            try:
                s = a.userprofile.company_file
            except:
                pass
            return HttpResponse(authenticated %(ti.ticket, s), content_type='text/xml')
        else:
            return HttpResponse(failed, content_type='text/xml')

    if ticket is not None:
        receive_response = root[0].find(tag('receiveResponseXML'))
        send_request = root[0].find(tag('sendRequestXML'))
        if receive_response != None:
            tick = QWCTicket.objects.get(ticket=ticket.text)
            ReceiveResponse.objects.create(ticket=tick, response=receive_response[1].text)

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
            return HttpResponse(do_for_me, content_type='text/xml')
            return HttpResponse(close_connection %("Finished!"), content_type='text/xml')



    return HttpResponse('do_for_me', content_type='text/xml')