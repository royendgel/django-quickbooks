# Message that the quickbooks webconnector is sending for me
from quickbooks.uttils import xml_soap

REQUEST_CLOSE_CONNECTION = 'closeConnection'
REQUEST_AUTHENTICATE = 'authenticate'
REQUEST_RECEIVE_REQUEST = 'receiveResponseXML'
REQUEST_SEND_REQUEST = 'sendRequestXML'
REQUEST_CONNECTION_ERROR = 'connectionError'
REQUEST_GET_INTERACTIVE_URL = 'getInteractiveUrl'
REQUEST_INTERACTIVE_DONE = 'interactiveDone'
REQUEST_GET_LAST_ERROR = 'getLastError'
REQUEST_SERVER_VERSION = 'serverVersion'
REQUEST_CLIENT_VERSION = 'clientVersion'

REQUEST_TYPES = [
    (REQUEST_CLOSE_CONNECTION, "Close Connection"),
    (REQUEST_AUTHENTICATE, "Authenticate"),
    (REQUEST_RECEIVE_REQUEST, "Receive Request"),
    (REQUEST_SEND_REQUEST, "Send Request"),
    (REQUEST_CONNECTION_ERROR, "Connection Error"),
    (REQUEST_GET_INTERACTIVE_URL, "Get Interactive URL"),
    (REQUEST_GET_LAST_ERROR, "Get Last Error"),
    (REQUEST_SERVER_VERSION, "Server Version"),
    (REQUEST_CLIENT_VERSION, "Client Version"),
]

close_connection = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://developer.intuit.com/">
	<SOAP-ENV:Body>
		<ns1:closeConnectionResponse>
			<ns1:closeConnectionResult>%s</ns1:closeConnectionResult>
		</ns1:closeConnectionResponse>
	</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

authenticated = ("""<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://developer.intuit.com/">
    	<SOAP-ENV:Body>
    		<ns1:authenticateResponse>
    			<ns1:authenticateResult>
    				<ns1:string>%s</ns1:string>
    				<ns1:string>%s</ns1:string>
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

# This one is what suds is generating for me
xm2 = ("""<?xml version="1.0" encoding="UTF-8"?>
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

xm2 = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://developer.intuit.com/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   <SOAP-ENV:Header />
   <ns0:Body>
      <ns1:authenticateResponse>
         <ns1:authenticateResult>41c03431-1366-4a42-8067-315a4be5158f</ns1:authenticateResult>
      </ns1:authenticateResponse>
   </ns0:Body>
</SOAP-ENV:Envelope>"""

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


qrequest = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://developer.intuit.com/">
	<SOAP-ENV:Body>
		<ns1:sendRequestXMLResponse>
			<ns1:sendRequestXMLResult>%s</ns1:sendRequestXMLResult>
		</ns1:sendRequestXMLResponse>
	</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""


processed = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://developer.intuit.com/">
	<SOAP-ENV:Body>
		<ns1:receiveResponseXMLResponse>
			<ns1:receiveResponseXMLResult>%s</ns1:receiveResponseXMLResult>
		</ns1:receiveResponseXMLResponse>
	</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""



process_failed = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
	<soap:Body>
		<receiveResponseXML xmlns="http://developer.intuit.com/">
			<ticket>438d2fc02a519df5fcc2eef0e7ad3898</ticket>
			<response />
			<hresult>0x80040400</hresult>
			<message>QuickBooks found an error when parsing the provided XML text stream.</message>
		</receiveResponseXML>
	</soap:Body>
</soap:Envelope>"""

get_last_error = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://developer.intuit.com/">
    <SOAP-ENV:Body>
        <ns1:getLastErrorResponse>
            <ns1:getLastErrorResult>%s</ns1:getLastErrorResult>
        </ns1:getLastErrorResponse>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""
