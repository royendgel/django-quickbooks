from quickbooks.qwc_xml import qrequest
from quickbooks.uttils import xml_soap
import xmltodict

class QBXML:

    def __init__(self):
        self.xml_prefix = '''<?xml version="1.0" encoding="utf-8"?><?qbxml version="2.1"?>'''
        self.names = [
            'Customer',
            'Bill',
            'Account',
            'Check',
            'Account',
            'Estimate',
            'Invoice',
            'ReceivePayment',
            'Vendor',
            'ToDo',
        ]

        self.method = [
            'Query',
            'Add',
            'Mod',
        ]

    def __build_name(self, name, method, request):
        method = method.title()
        request = request.title()
        return name + method + request

        return "InvoiceQueryRq"

    def __build_xml(self, name, method='query', request='rq', request_id=None):
        request_id = '22222'
        c = {
            'QBXML': {
                'QBXMLMsgsRq': {
                    '@onError': 'stopOnError',
                    self.__build_name(name, method=method, request=request): {
                        '@requestID': request_id
                    }
                }
            }
        }

        return self.xml_prefix +  xmltodict.unparse(c,full_document=False)

    def invoice(self):
        return ""

    def customer(self, name):
        return self.__build_xml(name, request_id=3333)

    def initial(self):
        msg = []
        for name in self.names:
            msg.append({'name' : name.lower() ,'message' : self.__build_xml(name=name)})
        return msg

