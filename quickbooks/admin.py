from django.contrib import admin
from quickbooks.models import *

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
admin.site.register(QBVendor)
admin.site.register(QBBill)
