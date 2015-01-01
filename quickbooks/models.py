from django.db import models
from django.contrib.auth.models import User
from uuidfield import UUIDField

from quickbooks.qbxml import QBXML
class QWCTicket(models.Model):
    ticket = UUIDField(auto=True)
    user = models.ForeignKey(User)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s | %s" %(self.user, self.ticket)

class ReceiveResponse(models.Model):
    ticket = models.ForeignKey(QWCTicket)
    response = models.TextField()
    processed = models.BooleanField(default=False)
    name = models.CharField(blank=True, null=True, default='', max_length=255)

    def __str__(self):
        return "%s" %(self.ticket)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    company_file = models.CharField(max_length=255, default='', blank=True)
    major_version = models.CharField(max_length=255, default='', blank=True)
    minor_version = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return "%s" %(self.user)

class MessageQue(models.Model):
    name = models.CharField(default='Query', max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User)
    message = models.TextField()
    active = models.BooleanField(default=True)
    repeat = models.BooleanField(default=False)
    last_accessed = models.TimeField(auto_now=True)

    def __str__(self):
        return "%s | %s" %(self.user, self.active)

class QBCustomer(models.Model):
    state = models.CharField(max_length=255, blank=True, null=True)  # State
    notes = models.CharField(max_length=255, blank=True, null=True)  # Notes
    postal_code = models.CharField(max_length=255, blank=True, null=True)  # PostalCode
    middle_name = models.CharField(max_length=255, blank=True, null=True)  # MiddleName
    phone = models.CharField(max_length=255, blank=True, null=True)  # Phone
    fax = models.CharField(max_length=255, blank=True, null=True)  # Fax
    city = models.CharField(max_length=255, blank=True, null=True)  # City
    contact = models.CharField(max_length=255, blank=True, null=True)  # Contact
    account_number = models.CharField(max_length=255, blank=True, null=True)  # AccountNumber
    full_name = models.CharField(max_length=255, blank=True, null=True)  # FullName
    company_name = models.CharField(max_length=255, blank=True, null=True)  # CompanyName
    name = models.CharField(max_length=255, blank=True, null=True)  # Name
    ship_address = models.CharField(max_length=255, blank=True, null=True)  # ShipAddress
    sublevel = models.CharField(max_length=255, blank=True, null=True)  # Sublevel
    alt_phone = models.CharField(max_length=255, blank=True, null=True)  # AltPhone
    first_name = models.CharField(max_length=255, blank=True, null=True)  # FirstName
    last_name = models.CharField(max_length=255, blank=True, null=True)  # LastName
    customer_type_ref = models.CharField(max_length=255, blank=True, null=True)  # CustomerTypeRef
    total_balance = models.CharField(max_length=255, blank=True, null=True)  # TotalBalance
    bill_address = models.CharField(max_length=255, blank=True, null=True)  # BillAddress
    addr2 = models.CharField(max_length=255, blank=True, null=True)  # Addr2
    item_sales_tax_ref = models.CharField(max_length=255, blank=True, null=True)  # ItemSalesTaxRef
    alt_contact = models.CharField(max_length=255, blank=True, null=True)  # AltContact
    addr4 = models.CharField(max_length=255, blank=True, null=True)  # Addr4
    is_active = models.CharField(max_length=255, blank=True, null=True)  # IsActive
    addr3 = models.CharField(max_length=255, blank=True, null=True)  # Addr3
    list_id = models.CharField(max_length=255, blank=True, null=True)  # ListID
    addr1 = models.CharField(max_length=255, blank=True, null=True)  # Addr1
    job_status = models.CharField(max_length=255, blank=True, null=True)  # JobStatus
    edit_sequence = models.CharField(max_length=255, blank=True, null=True)  # EditSequence
    time_created = models.CharField(max_length=255, blank=True, null=True)  # TimeCreated
    time_modified = models.CharField(max_length=255, blank=True, null=True)  # TimeModified
    sales_tax_code_ref = models.CharField(max_length=255, blank=True, null=True)  # SalesTaxCodeRef
    balance = models.CharField(max_length=255, blank=True, null=True)  # Balance
    terms_ref = models.CharField(max_length=255, blank=True, null=True)  # TermsRef
    salutation = models.CharField(max_length=255, blank=True, null=True)  # Salutation
    email = models.CharField(max_length=255, blank=True, null=True)  # Email

    def __str__(self):
        return self.name

class QBAccount(models.Model):
    cash_flow_classification = models.CharField(max_length=255, blank=True, null=True)  # CashFlowClassification
    account_number = models.CharField(max_length=255, blank=True, null=True)  # AccountNumber
    special_account_type = models.CharField(max_length=255, blank=True, null=True)  # SpecialAccountType
    desc = models.CharField(max_length=255, blank=True, null=True)  # Desc
    time_modified = models.CharField(max_length=255, blank=True, null=True)  # TimeModified
    edit_sequence = models.CharField(max_length=255, blank=True, null=True)  # EditSequence
    total_balance = models.CharField(max_length=255, blank=True, null=True)  # TotalBalance
    is_active = models.CharField(max_length=255, blank=True, null=True)  # IsActive
    list_id = models.CharField(max_length=255, blank=True, null=True)  # ListID
    name = models.CharField(max_length=255, blank=True, null=True)  # Name
    full_name = models.CharField(max_length=255, blank=True, null=True)  # FullName
    time_created = models.CharField(max_length=255, blank=True, null=True)  # TimeCreated
    sublevel = models.CharField(max_length=255, blank=True, null=True)  # Sublevel
    account_type = models.CharField(max_length=255, blank=True, null=True)  # AccountType
    parent_ref = models.CharField(max_length=255, blank=True, null=True)  # ParentRef
    balance = models.CharField(max_length=255, blank=True, null=True)  # Balance

    def __str__(self):
        return self.name

class QBCheck(models.Model):
    time_modified = models.CharField(max_length=255, blank=True, null=True)  # TimeModified
    account_ref = models.CharField(max_length=255, blank=True, null=True)  # AccountRef
    txn_date = models.CharField(max_length=255, blank=True, null=True)  # TxnDate
    city = models.CharField(max_length=255, blank=True, null=True)  # City
    addr1 = models.CharField(max_length=255, blank=True, null=True)  # Addr1
    list_id = models.CharField(max_length=255, blank=True, null=True)  # ListID
    country = models.CharField(max_length=255, blank=True, null=True)  # Country
    amount = models.CharField(max_length=255, blank=True, null=True)  # Amount
    is_to_be_printed = models.CharField(max_length=255, blank=True, null=True)  # IsToBePrinted
    addr2 = models.CharField(max_length=255, blank=True, null=True)  # Addr2
    memo = models.CharField(max_length=255, blank=True, null=True)  # Memo
    addr4 = models.CharField(max_length=255, blank=True, null=True)  # Addr4
    postal_code = models.CharField(max_length=255, blank=True, null=True)  # PostalCode
    addr3 = models.CharField(max_length=255, blank=True, null=True)  # Addr3
    ref_number = models.CharField(max_length=255, blank=True, null=True)  # RefNumber
    address = models.CharField(max_length=255, blank=True, null=True)  # Address
    time_created = models.CharField(max_length=255, blank=True, null=True)  # TimeCreated
    full_name = models.CharField(max_length=255, blank=True, null=True)  # FullName
    edit_sequence = models.CharField(max_length=255, blank=True, null=True)  # EditSequence
    state = models.CharField(max_length=255, blank=True, null=True)  # State
    payee_entity_ref = models.CharField(max_length=255, blank=True, null=True)  # PayeeEntityRef
    txn_number = models.CharField(max_length=255, blank=True, null=True)  # TxnNumber
    txn_id = models.CharField(max_length=255, blank=True, null=True)  # TxnID

    def __str__(self):
        return self.full_name

class QBEstimate(models.Model):
    bill_address = models.CharField(max_length=255, blank=True, null=True)  # BillAddress
    ref_number = models.CharField(max_length=255, blank=True, null=True)  # RefNumber
    full_name = models.CharField(max_length=255, blank=True, null=True)  # FullName
    addr1 = models.CharField(max_length=255, blank=True, null=True)  # Addr1
    txn_date = models.CharField(max_length=255, blank=True, null=True)  # TxnDate
    customer_ref = models.CharField(max_length=255, blank=True, null=True)  # CustomerRef
    customer_sales_tax_code_ref = models.CharField(max_length=255, blank=True, null=True)  # CustomerSalesTaxCodeRef
    addr2 = models.CharField(max_length=255, blank=True, null=True)  # Addr2
    addr4 = models.CharField(max_length=255, blank=True, null=True)  # Addr4
    txn_number = models.CharField(max_length=255, blank=True, null=True)  # TxnNumber
    total_amount = models.CharField(max_length=255, blank=True, null=True)  # TotalAmount
    time_modified = models.CharField(max_length=255, blank=True, null=True)  # TimeModified
    memo = models.CharField(max_length=255, blank=True, null=True)  # Memo
    postal_code = models.CharField(max_length=255, blank=True, null=True)  # PostalCode
    due_date = models.CharField(max_length=255, blank=True, null=True)  # DueDate
    addr3 = models.CharField(max_length=255, blank=True, null=True)  # Addr3
    subtotal = models.CharField(max_length=255, blank=True, null=True)  # Subtotal
    item_sales_tax_ref = models.CharField(max_length=255, blank=True, null=True)  # ItemSalesTaxRef
    sales_tax_percentage = models.CharField(max_length=255, blank=True, null=True)  # SalesTaxPercentage
    txn_id = models.CharField(max_length=255, blank=True, null=True)  # TxnID
    class_ref = models.CharField(max_length=255, blank=True, null=True)  # ClassRef
    city = models.CharField(max_length=255, blank=True, null=True)  # City
    sales_tax_total = models.CharField(max_length=255, blank=True, null=True)  # SalesTaxTotal
    list_id = models.CharField(max_length=255, blank=True, null=True)  # ListID
    state = models.CharField(max_length=255, blank=True, null=True)  # State
    edit_sequence = models.CharField(max_length=255, blank=True, null=True)  # EditSequence
    time_created = models.CharField(max_length=255, blank=True, null=True)  # TimeCreated

    def __str__(self):
        return self.full_name

class QBInvoice(models.Model):
    addr1 = models.CharField(max_length=255, blank=True, null=True)  # Addr1
    addr3 = models.CharField(max_length=255, blank=True, null=True)  # Addr3
    sales_tax_percentage = models.CharField(max_length=255, blank=True, null=True)  # SalesTaxPercentage
    full_name = models.CharField(max_length=255, blank=True, null=True)  # FullName
    time_modified = models.CharField(max_length=255, blank=True, null=True)  # TimeModified
    applied_amount = models.CharField(max_length=255, blank=True, null=True)  # AppliedAmount
    ship_date = models.CharField(max_length=255, blank=True, null=True)  # ShipDate
    customer_sales_tax_code_ref = models.CharField(max_length=255, blank=True, null=True)  # CustomerSalesTaxCodeRef
    po_number = models.CharField(max_length=255, blank=True, null=True)  # PONumber
    addr2 = models.CharField(max_length=255, blank=True, null=True)  # Addr2
    item_sales_tax_ref = models.CharField(max_length=255, blank=True, null=True)  # ItemSalesTaxRef
    ship_address = models.CharField(max_length=255, blank=True, null=True)  # ShipAddress
    bill_address = models.CharField(max_length=255, blank=True, null=True)  # BillAddress
    txn_number = models.CharField(max_length=255, blank=True, null=True)  # TxnNumber
    sales_tax_total = models.CharField(max_length=255, blank=True, null=True)  # SalesTaxTotal
    is_paid = models.CharField(max_length=255, blank=True, null=True)  # IsPaid
    suggested_discount_amount = models.CharField(max_length=255, blank=True, null=True)  # SuggestedDiscountAmount
    ref_number = models.CharField(max_length=255, blank=True, null=True)  # RefNumber
    class_ref = models.CharField(max_length=255, blank=True, null=True)  # ClassRef
    txn_date = models.CharField(max_length=255, blank=True, null=True)  # TxnDate
    addr4 = models.CharField(max_length=255, blank=True, null=True)  # Addr4
    postal_code = models.CharField(max_length=255, blank=True, null=True)  # PostalCode
    ar_account_ref = models.CharField(max_length=255, blank=True, null=True)  # ARAccountRef
    is_finance_charge = models.CharField(max_length=255, blank=True, null=True)  # IsFinanceCharge
    is_to_be_printed = models.CharField(max_length=255, blank=True, null=True)  # IsToBePrinted
    suggested_discount_date = models.CharField(max_length=255, blank=True, null=True)  # SuggestedDiscountDate
    time_created = models.CharField(max_length=255, blank=True, null=True)  # TimeCreated
    memo = models.CharField(max_length=255, blank=True, null=True)  # Memo
    terms_ref = models.CharField(max_length=255, blank=True, null=True)  # TermsRef
    customer_ref = models.CharField(max_length=255, blank=True, null=True)  # CustomerRef
    city = models.CharField(max_length=255, blank=True, null=True)  # City
    due_date = models.CharField(max_length=255, blank=True, null=True)  # DueDate
    txn_id = models.CharField(max_length=255, blank=True, null=True)  # TxnID
    balance_remaining = models.CharField(max_length=255, blank=True, null=True)  # BalanceRemaining
    subtotal = models.CharField(max_length=255, blank=True, null=True)  # Subtotal
    state = models.CharField(max_length=255, blank=True, null=True)  # State
    list_id = models.CharField(max_length=255, blank=True, null=True)  # ListID
    is_pending = models.CharField(max_length=255, blank=True, null=True)  # IsPending
    edit_sequence = models.CharField(max_length=255, blank=True, null=True)  # EditSequence

    def __str__(self):
        return self.full_name