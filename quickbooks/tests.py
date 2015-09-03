from collections import OrderedDict

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

import xmltodict

from quickbooks.models import *
from quickbooks.views import home

from lxml import etree

bill_added = """
<?xml version="1.0" encoding="utf-8"?>
<?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <BillAddRs statusCode="INTTYPE" statusSeverity="STRTYPE" statusMessage="STRTYPE">
            <BillRet>
                <TxnID >{{ txn_id }}</TxnID>
                <TimeCreated >{{ time_created }}</TimeCreated>
                <TimeModified >{{ time_modified }}</TimeModified>
                <EditSequence >{{ edit_sequence }}</EditSequence>
                <TxnNumber >{{ txn_number }}</TxnNumber>
                <VendorRef>
                    <ListID >{{ vendor_ref_list_id }}</ListID>
                    <FullName >{{ vendor_ref_full_name }}</FullName>
                </VendorRef>
                <TxnDate >{{ txn_date }}</TxnDate>
                <AmountDue >{{ amount_due }}</AmountDue>
                <ExpenseLineRet>
                    <TxnLineID >{{ expense_line_ret_txn_line_id }}</TxnLineID>
                    <AccountRef>
                        <ListID >{{ expense_line_ret_account_ref_list_id }}</ListID>
                        <FullName >{{ account_ref_full_name }}</FullName>
                    </AccountRef>
                    <Amount >{{ expense_line_ret_amount }}</Amount>
                    <CustomerRef>   
                        <ListID >{{ expense_line_ret_customer_ref_list_id }}</ListID>
                        <FullName >{{ expense_line_ret_customer_ref_full_name }}</FullName>
                    </CustomerRef>
                </ExpenseLineRet>
            </BillRet>
        </BillAddRs>
    </QBXMLMsgsRq>
</QBXML>
"""

class QuickbooksQBXML(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user('quickbooks', 'quickbooks@localhost.com', 'kickstart')
        self.ti = QWCTicket.objects.create(user=self.user)
        self.ticket = self.ti.ticket
        self.qbxml = QBXML()
        # Create some initial data...
        self.vendor = QBVendor.objects.create(list_id=100, first_name="John", last_name="Brown")
        self.account = QBAccount.objects.create(list_id=200, name="Primary Account")
        self.customer = QBCustomer.objects.create(list_id=300, first_name="Mr", last_name="Customer")


    def test_nested(self):
        # Using the ticket created in setUp     
        """ We need to test that when the bill response is received
            that the proper model structure is created for the bill and 
            it's ExpenseLineAdd items
            So we'll start by constructing the receiveResponse that 
            the web connector would send to our app
        """

        options = [
            ("BillRet", 
                [
                    ("TxnID", "1000"),
                    ("TimeCreated", "2015/01/01 00:00"),
                    ("TimeModified", "2015/01/01 00:00"),
                    ("EditSequence", "123456789"),
                    ("TxnNumber", "1000"),
                    ("VendorRef", 
                        [
                            ("ListID", self.vendor.list_id),
                            ("FullName", self.vendor.full_name),
                        ]
                    ),
                    ("TxnDate", "2015/01/01 00:00"),
                    ("AmountDue", "9000"),
                    ("ExpenseLineRet", 
                        [
                            ("TxnLineID", "2000"),
                            ("AccountRef", 
                                [
                                    ("ListID", self.account.list_id),
                                    ("FullName", self.account.name),
                                ]
                            ),
                            ("Amount", "3000"),
                            ("CustomerRef", 
                                [
                                    ("ListID", self.customer.list_id),
                                    ("FullName", self.customer.full_name)
                                ]
                            )
                        ]
                    ),
                    ("ExpenseLineRet", 
                        [
                            ("TxnLineID", "2001"),
                            ("AccountRef", 
                                [
                                    ("ListID", self.account.list_id),
                                    ("FullName", self.account.name),
                                ]
                            ),
                            ("Amount", "6000"),
                            ("CustomerRef", 
                                [
                                    ("ListID", self.customer.list_id),
                                    ("FullName", self.customer.full_name)
                                ]
                            )
                        ]
                    ),
                ]
            )
        ]
        c = {
            'QBXML': {
                'QBXMLMsgsRq': {
                    '@onError': 'stopOnError',
                    'BillAddRq': {
                        '@requestID': '2022',
                        'BillAdd':
                            OrderedDict(options)
                    }
                }
            }
        }
        xml = self.qbxml.xml_prefix + xmltodict.unparse(c, full_document=False)
        request = self.factory.post("/quickbooks/", xml, content_type="application/xml")
        response = home(request)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(QBBill.objects.filter(txn_id="1000").exists())
        bill = QBBill.objects.get(txn_id="1000")
        self.assertEquals(bill.account_ref, self.account)
        self.assertEquals(bill.customer_ref, self.customer)
        # count the many to many field items
