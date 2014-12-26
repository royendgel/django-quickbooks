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
