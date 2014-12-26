from django.db import models
from django.contrib.auth.models import User
from uuidfield import UUIDField

class QWCTicket(models.Model):
    ticket = UUIDField(auto=True)
    user = models.ForeignKey(User)
    company_file = models.CharField(max_length=255, default='', blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s | %s" %(self.user, self.ticket)