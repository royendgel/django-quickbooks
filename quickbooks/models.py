from django.db import models
from django.contrib.auth.models import User
from uuidfield import UUIDField

class QWCTicket(models.Model):
    ticket = UUIDField(auto=True)
    user = models.ForeignKey(User)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s | %s" %(self.user, self.ticket)

class ReceiveResponse(models.Model):
    ticket = models.ForeignKey(QWCTicket)
    response = models.TextField()

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
    user = models.ForeignKey(User)
    message = models.TextField()
    active = models.BooleanField(default=True)

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