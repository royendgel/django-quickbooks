from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.utils.timezone import make_aware
from django.utils import timezone

from uuidfield import UUIDField


from quickbooks.qbxml import *
from quickbooks.qwc_xml import REQUEST_TYPES

class QWCTicket(models.Model):
    ticket = UUIDField(auto=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s | %s" %(self.user, self.ticket)

class ReceiveResponse(models.Model):
    ticket = models.ForeignKey(QWCTicket)
    response = models.TextField()
    processed = models.BooleanField(default=False)
    name = models.CharField(blank=True, null=True, default='', max_length=2500)

    def __str__(self):
        return "%s" %(self.ticket)

class ResponseError(models.Model):

    status_code = models.PositiveIntegerField()
    content = models.TextField(blank=True, null=True)
    reason_phrase = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    @staticmethod
    def log_error(request, exception):
        print("LOGGING ERROR: %s and exception %s" % (type(request), type(exception)))
        content_type = request.META.get("CONTENT_TYPE")
        method = request.method
        if method == 'POST':
            return ResponseError.objects.create(
                status_code=500,
                content=exception.message,
                reason_phrase=exception.message
            )
        return None

    @staticmethod
    def get_last_error():
        try:
            error = ResponseError.objects.filter(processed=False).latest("date")
            error.processed = True
            error.save()
            return error
        except ResponseError.DoesNotExist:
            return None

class QWCMessage(models.Model):
    request_type = models.CharField(max_length=255, choices=REQUEST_TYPES)
    description = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)


def get_errors_and_messages(date=None):
    if not date:
        date = timezone.now() - timedelta(hours=24)
    message_list = []
    errors = ResponseError.objects.filter(date__gte=date).order_by('-date')
    for error in errors:
        message_list.append(dict(
                date=error.date,
                message=error.content,
                error=True,
            ))

    messages = QWCMessage.objects.filter(date__gte=date).order_by('-date')
    for message in messages:
        message_list.append(dict(
                date=message.date,
                message=message.get_request_type_display(),
                error=False
            ))

    # Sort all messages
    message_list.sort(key=lambda message: message.get("date"), reverse=True)
    return message_list



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    company_file = models.CharField(max_length=2500, default='', blank=True)
    major_version = models.CharField(max_length=2500, default='', blank=True)
    minor_version = models.CharField(max_length=2500, default='', blank=True)

    def __str__(self):
        return "%s" %(self.user)

class MessageQue(models.Model):
    name = models.CharField(default='Query', max_length=2500)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField()
    active = models.BooleanField(default=True)
    repeat = models.BooleanField(default=False)
    last_accessed = models.TimeField(auto_now=True)

    def __str__(self):
        return "%s | %s => %s" %(self.user, self.active, self.name)

class QBCustomer(models.Model):
    state = models.CharField(max_length=2500, blank=True, null=True)  # State
    notes = models.CharField(max_length=2500, blank=True, null=True)  # Notes
    postal_code = models.CharField(max_length=2500, blank=True, null=True)  # PostalCode
    middle_name = models.CharField(max_length=2500, blank=True, null=True)  # MiddleName
    phone = models.CharField(max_length=2500, blank=True, null=True)  # Phone
    fax = models.CharField(max_length=2500, blank=True, null=True)  # Fax
    city = models.CharField(max_length=2500, blank=True, null=True)  # City
    contact = models.CharField(max_length=2500, blank=True, null=True)  # Contact
    account_number = models.CharField(max_length=2500, blank=True, null=True)  # AccountNumber
    full_name = models.CharField(max_length=2500, blank=True, null=True)  # FullName
    company_name = models.CharField(max_length=2500, blank=True, null=True)  # CompanyName
    name = models.CharField(max_length=2500, blank=True, null=True)  # Name
    ship_address = models.CharField(max_length=2500, blank=True, null=True)  # ShipAddress
    sublevel = models.CharField(max_length=2500, blank=True, null=True)  # Sublevel
    alt_phone = models.CharField(max_length=2500, blank=True, null=True)  # AltPhone
    first_name = models.CharField(max_length=2500, blank=True, null=True)  # FirstName
    last_name = models.CharField(max_length=2500, blank=True, null=True)  # LastName
    customer_type_ref = models.CharField(max_length=2500, blank=True, null=True)  # CustomerTypeRef
    total_balance = models.CharField(max_length=2500, blank=True, null=True)  # TotalBalance
    bill_address = models.CharField(max_length=2500, blank=True, null=True)  # BillAddress
    addr2 = models.CharField(max_length=2500, blank=True, null=True)  # Addr2
    item_sales_tax_ref = models.CharField(max_length=2500, blank=True, null=True)  # ItemSalesTaxRef
    alt_contact = models.CharField(max_length=2500, blank=True, null=True)  # AltContact
    addr4 = models.CharField(max_length=2500, blank=True, null=True)  # Addr4
    is_active = models.CharField(max_length=2500, blank=True, null=True)  # IsActive
    addr3 = models.CharField(max_length=2500, blank=True, null=True)  # Addr3
    list_id = models.CharField(max_length=2500, primary_key=True)  # ListID
    addr1 = models.CharField(max_length=2500, blank=True, null=True)  # Addr1
    job_status = models.CharField(max_length=2500, blank=True, null=True)  # JobStatus
    edit_sequence = models.CharField(max_length=2500, blank=True, null=True)  # EditSequence
    time_created = models.CharField(max_length=2500, blank=True, null=True)  # TimeCreated
    time_modified = models.CharField(max_length=2500, blank=True, null=True)  # TimeModified
    sales_tax_code_ref = models.CharField(max_length=2500, blank=True, null=True)  # SalesTaxCodeRef
    balance = models.CharField(max_length=2500, blank=True, null=True)  # Balance
    terms_ref = models.CharField(max_length=2500, blank=True, null=True)  # TermsRef
    salutation = models.CharField(max_length=2500, blank=True, null=True)  # Salutation
    email = models.CharField(max_length=2500, blank=True, null=True)  # Email

    def __str__(self):
        return "%s" %(self.name.encode('utf-8'))

class QBEmployee(models.Model):

    list_id = models.CharField(max_length=2500, primary_key=True)  # ListID
    first_name = models.CharField(max_length=2500, blank=True, null=True)  # FirstName
    middle_name = models.CharField(max_length=2500, blank=True, null=True)  # MiddleName
    last_name = models.CharField(max_length=2500, blank=True, null=True)  # LastName
    full_name = models.CharField(max_length=2500, blank=True, null=True)  # FullName
    name = models.CharField(max_length=2500, blank=True, null=True)  # Name

    notes = models.CharField(max_length=2500, blank=True, null=True)  # Notes
    phone = models.CharField(max_length=2500, blank=True, null=True)  # Phone
    fax = models.CharField(max_length=2500, blank=True, null=True)  # Fax
    city = models.CharField(max_length=2500, blank=True, null=True)  # City
    contact = models.CharField(max_length=2500, blank=True, null=True)  # Contact
    account_number = models.CharField(max_length=2500, blank=True, null=True)  # AccountNumber
    company_name = models.CharField(max_length=2500, blank=True, null=True)  # CompanyName
    is_active = models.CharField(max_length=2500, blank=True, null=True)  # IsActive
    edit_sequence = models.CharField(max_length=2500, blank=True, null=True)  # EditSequence
    time_created = models.CharField(max_length=2500, blank=True, null=True)  # TimeCreated
    time_modified = models.CharField(max_length=2500, blank=True, null=True)  # TimeModified
    salutation = models.CharField(max_length=2500, blank=True, null=True)  # Salutation
    email = models.CharField(max_length=2500, blank=True, null=True)  # Email

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)

class QBAccount(models.Model):
    cash_flow_classification = models.CharField(max_length=2500, blank=True, null=True)  # CashFlowClassification
    account_number = models.CharField(max_length=2500, blank=True, null=True)  # AccountNumber
    special_account_type = models.CharField(max_length=2500, blank=True, null=True)  # SpecialAccountType
    desc = models.CharField(max_length=2500, blank=True, null=True)  # Desc
    time_modified = models.CharField(max_length=2500, blank=True, null=True)  # TimeModified
    edit_sequence = models.CharField(max_length=2500, blank=True, null=True)  # EditSequence
    total_balance = models.CharField(max_length=2500, blank=True, null=True)  # TotalBalance
    is_active = models.CharField(max_length=2500, blank=True, null=True)  # IsActive
    list_id = models.CharField(max_length=2500, primary_key=True)  # ListID
    name = models.CharField(max_length=2500, blank=True, null=True)  # Name
    full_name = models.CharField(max_length=2500, blank=True, null=True)  # FullName
    time_created = models.CharField(max_length=2500, blank=True, null=True)  # TimeCreated
    sublevel = models.CharField(max_length=2500, blank=True, null=True)  # Sublevel
    account_type = models.CharField(max_length=2500, blank=True, null=True)  # AccountType
    parent_ref = models.CharField(max_length=2500, blank=True, null=True)  # ParentRef
    balance = models.CharField(max_length=2500, blank=True, null=True)  # Balance

    def __str__(self):
        return self.name

class QBCheck(models.Model):
    time_modified = models.CharField(max_length=2500, blank=True, null=True)  # TimeModified
    account_ref = models.CharField(max_length=2500, blank=True, null=True)  # AccountRef
    txn_date = models.CharField(max_length=2500, blank=True, null=True)  # TxnDate
    city = models.CharField(max_length=2500, blank=True, null=True)  # City
    addr1 = models.CharField(max_length=2500, blank=True, null=True)  # Addr1
    list_id = models.CharField(max_length=2500, primary_key=True)  # ListID
    country = models.CharField(max_length=2500, blank=True, null=True)  # Country
    amount = models.CharField(max_length=2500, blank=True, null=True)  # Amount
    is_to_be_printed = models.CharField(max_length=2500, blank=True, null=True)  # IsToBePrinted
    addr2 = models.CharField(max_length=2500, blank=True, null=True)  # Addr2
    memo = models.CharField(max_length=2500, blank=True, null=True)  # Memo
    addr4 = models.CharField(max_length=2500, blank=True, null=True)  # Addr4
    postal_code = models.CharField(max_length=2500, blank=True, null=True)  # PostalCode
    addr3 = models.CharField(max_length=2500, blank=True, null=True)  # Addr3
    ref_number = models.CharField(max_length=2500, blank=True, null=True)  # RefNumber
    address = models.CharField(max_length=2500, blank=True, null=True)  # Address
    time_created = models.CharField(max_length=2500, blank=True, null=True)  # TimeCreated
    full_name = models.CharField(max_length=2500, blank=True, null=True)  # FullName
    edit_sequence = models.CharField(max_length=2500, blank=True, null=True)  # EditSequence
    state = models.CharField(max_length=2500, blank=True, null=True)  # State
    payee_entity_ref = models.CharField(max_length=2500, blank=True, null=True)  # PayeeEntityRef
    txn_number = models.CharField(max_length=2500, blank=True, null=True)  # TxnNumber
    txn_id = models.CharField(max_length=2500, blank=True, null=True)  # TxnID

    def __str__(self):
        return self.memo

class QBEstimate(models.Model):
    bill_address = models.CharField(max_length=2500, blank=True, null=True)  # BillAddress
    ref_number = models.CharField(max_length=2500, blank=True, null=True)  # RefNumber
    full_name = models.CharField(max_length=2500, blank=True, null=True)  # FullName
    addr1 = models.CharField(max_length=2500, blank=True, null=True)  # Addr1
    txn_date = models.CharField(max_length=2500, blank=True, null=True)  # TxnDate
    customer_ref = models.CharField(max_length=2500, blank=True, null=True)  # CustomerRef
    customer_sales_tax_code_ref = models.CharField(max_length=2500, blank=True, null=True)  # CustomerSalesTaxCodeRef
    addr2 = models.CharField(max_length=2500, blank=True, null=True)  # Addr2
    addr4 = models.CharField(max_length=2500, blank=True, null=True)  # Addr4
    txn_number = models.CharField(max_length=2500, blank=True, null=True)  # TxnNumber
    total_amount = models.CharField(max_length=2500, blank=True, null=True)  # TotalAmount
    time_modified = models.CharField(max_length=2500, blank=True, null=True)  # TimeModified
    memo = models.CharField(max_length=2500, blank=True, null=True)  # Memo
    postal_code = models.CharField(max_length=2500, blank=True, null=True)  # PostalCode
    due_date = models.CharField(max_length=2500, blank=True, null=True)  # DueDate
    addr3 = models.CharField(max_length=2500, blank=True, null=True)  # Addr3
    subtotal = models.CharField(max_length=2500, blank=True, null=True)  # Subtotal
    item_sales_tax_ref = models.CharField(max_length=2500, blank=True, null=True)  # ItemSalesTaxRef
    sales_tax_percentage = models.CharField(max_length=2500, blank=True, null=True)  # SalesTaxPercentage
    txn_id = models.CharField(max_length=2500, blank=True, null=True)  # TxnID
    class_ref = models.CharField(max_length=2500, blank=True, null=True)  # ClassRef
    city = models.CharField(max_length=2500, blank=True, null=True)  # City
    sales_tax_total = models.CharField(max_length=2500, blank=True, null=True)  # SalesTaxTotal
    list_id = models.CharField(max_length=2500, primary_key=True)  # ListID
    state = models.CharField(max_length=2500, blank=True, null=True)  # State
    edit_sequence = models.CharField(max_length=2500, blank=True, null=True)  # EditSequence
    time_created = models.CharField(max_length=2500, blank=True, null=True)  # TimeCreated

    def __str__(self):
        return self.full_name

class QBInvoice(models.Model):
    addr1 = models.CharField(max_length=2500, blank=True, null=True)  # Addr1
    addr3 = models.CharField(max_length=2500, blank=True, null=True)  # Addr3
    sales_tax_percentage = models.CharField(max_length=2500, blank=True, null=True)  # SalesTaxPercentage
    full_name = models.CharField(max_length=2500, blank=True, null=True)  # FullName
    time_modified = models.CharField(max_length=2500, blank=True, null=True)  # TimeModified
    applied_amount = models.CharField(max_length=2500, blank=True, null=True)  # AppliedAmount
    ship_date = models.CharField(max_length=2500, blank=True, null=True)  # ShipDate
    customer_sales_tax_code_ref = models.CharField(max_length=2500, blank=True, null=True)  # CustomerSalesTaxCodeRef
    po_number = models.CharField(max_length=2500, blank=True, null=True)  # PONumber
    addr2 = models.CharField(max_length=2500, blank=True, null=True)  # Addr2
    item_sales_tax_ref = models.CharField(max_length=2500, blank=True, null=True)  # ItemSalesTaxRef
    ship_address = models.CharField(max_length=2500, blank=True, null=True)  # ShipAddress
    bill_address = models.CharField(max_length=2500, blank=True, null=True)  # BillAddress
    txn_number = models.CharField(max_length=2500, blank=True, null=True)  # TxnNumber
    sales_tax_total = models.CharField(max_length=2500, blank=True, null=True)  # SalesTaxTotal
    is_paid = models.CharField(max_length=2500, blank=True, null=True)  # IsPaid
    suggested_discount_amount = models.CharField(max_length=2500, blank=True, null=True)  # SuggestedDiscountAmount
    ref_number = models.CharField(max_length=2500, blank=True, null=True)  # RefNumber
    class_ref = models.CharField(max_length=2500, blank=True, null=True)  # ClassRef
    txn_date = models.CharField(max_length=2500, blank=True, null=True)  # TxnDate
    addr4 = models.CharField(max_length=2500, blank=True, null=True)  # Addr4
    postal_code = models.CharField(max_length=2500, blank=True, null=True)  # PostalCode
    ar_account_ref = models.CharField(max_length=2500, blank=True, null=True)  # ARAccountRef
    is_finance_charge = models.CharField(max_length=2500, blank=True, null=True)  # IsFinanceCharge
    is_to_be_printed = models.CharField(max_length=2500, blank=True, null=True)  # IsToBePrinted
    suggested_discount_date = models.CharField(max_length=2500, blank=True, null=True)  # SuggestedDiscountDate
    time_created = models.CharField(max_length=2500, blank=True, null=True)  # TimeCreated
    memo = models.CharField(max_length=2500, blank=True, null=True)  # Memo
    terms_ref = models.CharField(max_length=2500, blank=True, null=True)  # TermsRef
    customer_ref = models.CharField(max_length=2500, blank=True, null=True)  # CustomerRef
    city = models.CharField(max_length=2500, blank=True, null=True)  # City
    due_date = models.CharField(max_length=2500, blank=True, null=True)  # DueDate
    txn_id = models.CharField(max_length=2500, blank=True, null=True)  # TxnID
    balance_remaining = models.CharField(max_length=2500, blank=True, null=True)  # BalanceRemaining
    subtotal = models.CharField(max_length=2500, blank=True, null=True)  # Subtotal
    state = models.CharField(max_length=2500, blank=True, null=True)  # State
    list_id = models.CharField(max_length=2500, primary_key=True)  # ListID
    is_pending = models.CharField(max_length=2500, blank=True, null=True)  # IsPending
    edit_sequence = models.CharField(max_length=2500, blank=True, null=True)  # EditSequence
    invoice_line_add = models.ManyToManyField("QBInvoiceLineAdd", blank=True, null=True)

    def __str__(self):
        return self.subtotal

class QBInvoiceLineAdd(models.Model):
    desc = models.CharField(max_length=2500, blank=True, null=True)
    quantity = models.CharField(max_length=2500, blank=True, null=True)
    unit_of_measure = models.CharField(max_length=2500, blank=True, null=True)
    amount = models.CharField(max_length=2500, blank=True, null=True)

    def __unicode__(self):
        return self.desc

class QBItem(models.Model):
    item_desc = models.CharField(max_length=2500, blank=True, null=True) # ItemDesc
    item_group_line = models.CharField(max_length=2500, blank=True, null=True) # ItemGroupLine
    sales_tax_code_ref = models.CharField(max_length=2500, blank=True, null=True) # SalesTaxCodeRef
    edit_sequence = models.CharField(max_length=2500, blank=True, null=True) # EditSequence
    average_cost = models.CharField(max_length=2500, blank=True, null=True) # AverageCost
    tax_vendor_ref = models.CharField(max_length=2500, blank=True, null=True) # TaxVendorRef
    tax_rate = models.CharField(max_length=2500, blank=True, null=True) # TaxRate
    quantity_on_order = models.CharField(max_length=2500, blank=True, null=True) # QuantityOnOrder
    sales_and_purchase = models.CharField(max_length=2500, blank=True, null=True) # SalesAndPurchase
    purchase_cost = models.CharField(max_length=2500, blank=True, null=True) # PurchaseCost
    list_id = models.CharField(max_length=2500, primary_key=True) # ListID
    cogs_account_ref = models.CharField(max_length=2500, blank=True, null=True) # COGSAccountRef
    discount_rate_percent = models.CharField(max_length=2500, blank=True, null=True) # DiscountRatePercent
    reorder_point = models.CharField(max_length=2500, blank=True, null=True) # ReorderPoint
    purchase_desc = models.CharField(max_length=2500, blank=True, null=True) # PurchaseDesc
    pref_vendor_ref = models.CharField(max_length=2500, blank=True, null=True) # PrefVendorRef
    quantity_on_sales_order = models.CharField(max_length=2500, blank=True, null=True) # QuantityOnSalesOrder
    name = models.CharField(max_length=2500, blank=True, null=True) # Name
    sublevel = models.CharField(max_length=2500, blank=True, null=True) # Sublevel
    income_account_ref = models.CharField(max_length=2500, blank=True, null=True) # IncomeAccountRef
    quantity_on_hand = models.CharField(max_length=2500, blank=True, null=True) # QuantityOnHand
    discount_rate = models.CharField(max_length=2500, blank=True, null=True) # DiscountRate
    sales_or_purchase = models.ForeignKey("QBSalesOrPurchase", blank=True, null=True) # SalesOrPurchase
    account_ref = models.CharField(max_length=2500, blank=True, null=True) # AccountRef
    is_print_items_in_group = models.CharField(max_length=2500, blank=True, null=True) # IsPrintItemsInGroup
    time_created = models.CharField(max_length=2500, blank=True, null=True) # TimeCreated
    sales_desc = models.CharField(max_length=2500, blank=True, null=True) # SalesDesc
    asset_account_ref = models.CharField(max_length=2500, blank=True, null=True) # AssetAccountRef
    time_modified = models.CharField(max_length=2500, blank=True, null=True) # TimeModified
    parent_ref = models.CharField(max_length=2500, blank=True, null=True) # ParentRef
    full_name = models.CharField(max_length=2500, blank=True, null=True) # FullName
    sales_price = models.CharField(max_length=2500, blank=True, null=True) # SalesPrice
    is_active = models.CharField(max_length=2500, blank=True, null=True) # IsActive

    def __unicode__(self):
        return unicode(self.name) 
        # return "ss"

class QBSalesOrPurchase(models.Model):

    price = models.CharField(max_length=2500, blank=True, null=True)
    account_ref = models.ForeignKey("QBAccount", blank=True, null=True)


class QBVendor(models.Model):

    name = models.CharField(max_length=2500, blank=True, null=True)
    first_name = models.CharField(max_length=2500, blank=True, null=True)  # FirstName
    middle_name = models.CharField(max_length=2500, blank=True, null=True)  # MiddleName
    last_name = models.CharField(max_length=2500, blank=True, null=True)  # LastName
    full_name = models.CharField(max_length=2500, blank=True, null=True)  # FullName
    company_name = models.CharField(max_length=2500, blank=True, null=True) # CompanyName
    salutation = models.CharField(max_length=2500, blank=True, null=True)  # Salutation
    job_title = models.CharField(max_length=2500, blank=True, null=True)  # JobTitle
    phone = models.CharField(max_length=2500, blank=True, null=True)  # Phone
    alt_phone = models.CharField(max_length=2500, blank=True, null=True)  # AltPhone
    fax = models.CharField(max_length=2500, blank=True, null=True)  # Fax
    email = models.CharField(max_length=2500, blank=True, null=True)  # Email
    contact = models.CharField(max_length=2500, blank=True, null=True)  # Contact
    alt_contact = models.CharField(max_length=2500, blank=True, null=True)  # AltContact
    notes = models.CharField(max_length=2500, blank=True, null=True)  # Notes
    account_number = models.CharField(max_length=2500, blank=True, null=True)  # AccountNumber
    credit_limit = models.CharField(max_length=2500, blank=True, null=True)  # CreditLimit
    vendor_tax_ident = models.CharField(max_length=2500, blank=True, null=True)
    list_id = models.CharField(max_length=2500, primary_key=True)  # ListID
    is_pending = models.CharField(max_length=2500, blank=True, null=True)  # IsPending
    edit_sequence = models.CharField(max_length=2500, blank=True, null=True)  # EditSequence

    def __unicode__(self):
        return unicode(self.full_name)

class QBBill(models.Model):

    txn_date = models.CharField(max_length=255, blank=True, null=True) # TxnDate
    txn_id = models.CharField(max_length=255, primary_key=True) # TxnID
    due_date = models.CharField(max_length=255, blank=True, null=True) # DueDate
    ref_number = models.CharField(max_length=2500, blank=True, null=True) # RefNumber
    memo = models.CharField(max_length=2500, blank=True, null=True) # Memo
    exchange_rate = models.CharField(max_length=2500, blank=True, null=True) # ExchangeRate

    is_pending = models.CharField(max_length=2500, blank=True, null=True)  # IsPending
    is_paid = models.CharField(max_length=2500, blank=True, null=True) # IsPaid
    edit_sequence = models.CharField(max_length=2500, blank=True, null=True)  # EditSequence
    vendor_ref = models.ForeignKey("QBVendor", blank=True, null=True) # VendorRef

    expense_line_add = models.ManyToManyField("ExpenseLineAdd", blank=True, null=True)
    item_line_add = models.ManyToManyField("QBItemLineAdd", blank=True, null=True)


class ExpenseLineAdd(models.Model):

    account_ref = models.ForeignKey("QBAccount", blank=True, null=True) # AccountRef
    amount = models.CharField(max_length=2500, blank=True, null=True) # Amount
    memo = models.CharField(max_length=2500, blank=True, null=True)
    customer_ref = models.ForeignKey("QBCustomer", blank=True, null=True)


class QBItemLineAdd(models.Model):

    item_ref = models.ForeignKey("QBItem", blank=True, null=True) # ItemRef
    serial_number = models.CharField(max_length=255, blank=True, null=True) # SerialNumber
    lot_number = models.CharField(max_length=255, blank=True, null=True) # LotNumber
    desc = models.CharField(max_length=255, blank=True, null=True) # Desc
    quantity = models.CharField(max_length=255, blank=True, null=True) # Quantity
    amount = models.CharField(max_length=2500, blank=True, null=True) # Amount
    cost = models.CharField(max_length=255, blank=True, null=True) # Cost
    unit_of_measure = models.CharField(max_length=255, blank=True, null=True) # UnitOfMeasure
    memo = models.CharField(max_length=2500, blank=True, null=True) # Memo
    customer_ref = models.ForeignKey("QBCustomer", blank=True, null=True) # CustomerRef
    sales_rep_ref = models.ForeignKey("QBEmployee", blank=True, null=True)


class QBItemPayment(models.Model):

    list_id = models.CharField(max_length=2500, primary_key=True)  # ListID
    name = models.CharField(max_length=255, blank=True, null=True) # Name
    item_desc = models.CharField(max_length=255, blank=True, null=True) # ItemDesc
    edit_sequence = models.CharField(max_length=2500, blank=True, null=True)  # EditSequence
    time_created = models.CharField(max_length=2500, blank=True, null=True)  # TimeCreated
    time_modified = models.CharField(max_length=2500, blank=True, null=True)  # TimeModified
    
    def __unicode__(self):
        return self.name