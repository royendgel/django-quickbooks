from django.contrib import admin
from quickbooks.models import QWCTicket
from quickbooks.models import UserProfile
from quickbooks.models import ReceiveResponse




admin.site.register(QWCTicket)
admin.site.register(UserProfile)
admin.site.register(ReceiveResponse)