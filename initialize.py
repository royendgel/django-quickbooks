import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qwc.settings")
import django
django.setup()

from django.contrib.auth.models import User

from quickbooks.models import MessageQue
from quickbooks import models
from quickbooks.qbxml import QBXML

from django.db.models import get_app, get_models

for model in get_models():
    model.objects.all().delete()

# Let's create two users one for dashboard and another for quickbooks authentication.
qb = User.objects.create_user('quickbooks', 'quickbooks@localhost.com', 'kickstart')
User.objects.create_superuser('admin', 'admin@localhost.com', 'admin')

# Generates some quickbooks messages.

q = QBXML().initial()
for query in q:
    MessageQue.objects.create(name=query['name'], message=query['message'], description='Auto Generated', repeat=True,
                              user=qb)

