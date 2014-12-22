from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from suds.client import Client
from suds.plugin import MessagePlugin
import os
from lxml import etree

# Message that the quickbooks webconnector is sending for me


# This one will authenticate the web conector I use this only for testing.
xm = ("""<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://developer.intuit.com/">
    	<SOAP-ENV:Body>
    		<ns1:authenticateResponse>
    			<ns1:authenticateResult>
    				<ns1:string>15c9ce293bd3f41b761c21635b14fa06</ns1:string>
    				<ns1:string></ns1:string>
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
def whome(request):
    url = 'http://127.01.0.1:8000/quickbooks'
    url = 'http://127.01.0.1:8000/quickbooks'
    client = Client('file://'+os.path.join(settings.BASE_DIR, 'server', 'qb.wsdl'))
    # Usualy the xml I gonna receive:
    # for element in ET.iterparse(request):
    #     print(element)

    # is there a authenticate call ?
    contents = etree.parse(request)
    root = contents.getroot()
    if root[0][0].tag == tag('authenticate', 'intuit'):
        return HttpResponse(xm, content_type='text/xml')
        return HttpResponse(client.service.authenticateResponse, content_type='text/xml')
    else:
        print(root[0][0].tag)
    return HttpResponse('')

@csrf_exempt
def home(request):
    url = 'file://' + os.path.join(settings.BASE_DIR, 'server', 'qb.wsdl')
    client = Client(url, plugins=[LogPlugin()])
    client.set_options(nosend=True)
    contents = etree.parse(request)
    root = contents.getroot()
    resp = client.service.authenticateResponse('15c9ce293bd3f41b761c21635b14fa06').envelope
    # We need to listen to authenticate, token or error.
    if root[0][0].tag == tag('authenticate', 'intuit'):
        return HttpResponse(resp, content_type='text/xml')
    return HttpResponse('no response >> not authenticate', content_type='text/xml')