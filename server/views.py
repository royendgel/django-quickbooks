from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from suds.client import Client
from suds.plugin import MessagePlugin
import os
from lxml import etree
from django.contrib.auth import authenticate
import logging
from server.models import QWCTicket



# Message that the quickbooks webconnector is sending for me


close_connection = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://developer.intuit.com/">
	<SOAP-ENV:Body>
		<ns1:closeConnectionResponse>
			<ns1:closeConnectionResult>%s</ns1:closeConnectionResult>
		</ns1:closeConnectionResponse>
	</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

# This one will authenticate the web conector I use this only for testing.
authenticated = ("""<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://developer.intuit.com/">
    	<SOAP-ENV:Body>
    		<ns1:authenticateResponse>
    			<ns1:authenticateResult>
    				<ns1:string>%s</ns1:string>
    				<ns1:string></ns1:string>
    			</ns1:authenticateResult>
    		</ns1:authenticateResponse>
    	</SOAP-ENV:Body>
    </SOAP-ENV:Envelope>""")

failed = ("""<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://developer.intuit.com/">
    	<SOAP-ENV:Body>
    		<ns1:authenticateResponse>
    			<ns1:authenticateResult>
    			</ns1:authenticateResult>
    		</ns1:authenticateResponse>
    	</SOAP-ENV:Body>
    </SOAP-ENV:Envelope>""")

# This one is what suds is generating for me
xm2 = ("""<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope
    xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ns0="http://developer.intuit.com/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <SOAP-ENV:Header/>
    <ns1:Body>
        <ns0:authenticateResponse>
            <ns0:authenticateResult>15c9ce293bd3f41b761c21635b14fa06</ns0:authenticateResult>
        </ns0:authenticateResponse>
    </ns1:Body>
</SOAP-ENV:Envelope>""")

xm3 = """"<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://developer.intuit.com/">
	<SOAP-ENV:Body>
		<ns1:authenticateResponse>
			<ns1:authenticateResult>
				<ns1:string>15c9ce293bd3f41b761c21635b14fa06</ns1:string>
				<ns1:string></ns1:string>
			</ns1:authenticateResult>
		</ns1:authenticateResponse>
	</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""


do_for_me = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://developer.intuit.com/">
	<SOAP-ENV:Body>
		<ns1:sendRequestXMLResponse>
			<ns1:sendRequestXMLResult>&lt;?xml version=&quot;1.0&quot; encoding=&quot;utf-8&quot;?&gt;
			&lt;?qbxml version=&quot;2.1&quot;?&gt;
			&lt;QBXML&gt;
				&lt;QBXMLMsgsRq onError=&quot;stopOnError&quot;&gt;
					&lt;ReceivePaymentAddRq requestID=&quot;UmVjZWl2ZVBheW1lbnRBZGR8MTE2&quot;&gt;
						&lt;ReceivePaymentAdd&gt;
							&lt;CustomerRef&gt;
								&lt;ListID&gt;90000-1241602188&lt;/ListID&gt;
							&lt;/CustomerRef&gt;
							&lt;TxnDate&gt;2009-05-06&lt;/TxnDate&gt;
							&lt;RefNumber&gt;116&lt;/RefNumber&gt;
							&lt;TotalAmount&gt;265.40&lt;/TotalAmount&gt;
							&lt;Memo&gt;Payment for invoice #116&lt;/Memo&gt;
							&lt;IsAutoApply&gt;true&lt;/IsAutoApply&gt;
						&lt;/ReceivePaymentAdd&gt;
					&lt;/ReceivePaymentAddRq&gt;
				&lt;/QBXMLMsgsRq&gt;
			&lt;/QBXML&gt;</ns1:sendRequestXMLResult>
		</ns1:sendRequestXMLResponse>
	</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

# This is to log every message to the console.
class LogPlugin(MessagePlugin):
  def sending(self, context):
    print(str(context.envelope))
  def received(self, context):
    print(str(context.reply))


def tag(tag, mode='intuit'):
    intuit = '{http://developer.intuit.com/}'
    soap = '{http://schemas.xmlsoap.org/soap/envelope/}'
    return intuit + tag if mode == 'intuit' else soap + tag

@csrf_exempt
def show_wsdl(request):
    contents = ""
    with(open(os.path.join(settings.BASE_DIR, 'server', 'qb.wsdl'), 'r')) as f:
        contents = f.read()
    return HttpResponse(contents, content_type='text/xml')

@csrf_exempt
def home(request):
    if request.method == "GET":
        return HttpResponse('The request need to be POST')
    # print(request.body)
    url = 'file://' + os.path.join(settings.BASE_DIR, 'server', 'qb.wsdl')
    client = Client(url, plugins=[LogPlugin()])
    client.set_options(nosend=True)
    contents = etree.parse(request)
    root = contents.getroot()
    # resp = client.service.authenticateResponse('15c9ce293bd3f41b761c21635b14fa06').envelope
    # We need to listen to authenticate, token or error.
    cont = root[0][0]
    ticket = cont.find(tag('ticket'))
    if cont.tag == tag('authenticate', 'intuit'):
        username = cont.find(tag('strUserName')).text
        password = cont.find(tag('strPassword')).text
        # Authenticate with database
        a = authenticate(username=username, password=password)
        if a:
            # Delete any ticket this user have.
            QWCTicket.objects.filter(user=a).delete()
            ti = QWCTicket.objects.create(user=a)
            company_file_location =
            return HttpResponse(authenticated %(ti.ticket), content_type='text/xml')
        else:
            return HttpResponse(failed, content_type='text/xml')

    if ticket is not None:
        t = QWCTicket.objects.get(ticket=ticket.text)
        if t is not None:
            # all_fancy_stuff = cont.find(tag('strHCPResponse')).text
            company_file_location = cont.find(tag('strCompanyFileName'))
            #
            # update the company_file location if it's not updated.
            if company_file_location is not None:
                if company_file_location != t.company_file:
                    t.company_file = company_file_location
                    t.save()
            return HttpResponse(close_connection %("Finished"), content_type='text/xml')

    return HttpResponse('do_for_me', content_type='text/xml')