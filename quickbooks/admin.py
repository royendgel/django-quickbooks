from django.contrib import admin
from quickbooks.models import QWCTicket
from quickbooks.models import UserProfile
from quickbooks.models import ReceiveResponse
from quickbooks.models import MessageQue
from quickbooks.models import QBCustomer

class QBCustomerAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'list_id']


admin.site.register(QWCTicket)
admin.site.register(UserProfile)
admin.site.register(ReceiveResponse)
admin.site.register(MessageQue)
admin.site.register(QBCustomer, QBCustomerAdmin)
