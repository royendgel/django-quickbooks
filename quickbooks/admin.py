from django.contrib import admin
from quickbooks.models import QWCTicket
from quickbooks.models import UserProfile
from quickbooks.models import ReceiveResponse
from quickbooks.models import MessageQue
from quickbooks.models import QBCustomer
from quickbooks.models import QBAccount
from quickbooks.models import QBCheck
from quickbooks.models import QBEstimate
from quickbooks.models import QBInvoice
from quickbooks.models import QBItem


class QBCustomerAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'list_id']

class QBCheckAdmin(admin.ModelAdmin):
    list_display = ['memo', 'amount']


class QBInvoiceAdmin(admin.ModelAdmin):
    list_display = ['subtotal']


class ReceiveResponseAdmin(admin.ModelAdmin):
    pass


class QBEstimateAdmin(admin.ModelAdmin):
    pass

class QBAccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(QWCTicket)
admin.site.register(UserProfile)
admin.site.register(ReceiveResponse, ReceiveResponseAdmin)
admin.site.register(QBInvoice, QBInvoiceAdmin)
admin.site.register(QBEstimate, QBEstimateAdmin)
admin.site.register(QBCheck, QBCheckAdmin)
admin.site.register(QBAccount, QBAccountAdmin)
admin.site.register(MessageQue)
admin.site.register(QBCustomer, QBCustomerAdmin)
admin.site.register(QBItem)
