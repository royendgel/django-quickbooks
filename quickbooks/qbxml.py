from quickbooks.qwc_xml import qrequest
from quickbooks.uttils import convert

class QBXML:

    def __init__(self):
        self.message = [
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

    def __build_name(self):
        return "InvoiceQueryRq"

    def __build_request(self):
        return convert("")

    def invoice(self):
        return ""

