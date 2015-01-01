import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qwc.settings")
import django
django.setup()

from django.contrib.auth.models import User

from quickbooks.models import MessageQue
from quickbooks import models
from quickbooks.qbxml import QBXML

from django.db.models import get_app, get_models
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

models = []
for modell in get_models():
    models.append(modell)
will_be_deleted_text = bcolors.OKBLUE + "WARNING!! all this data in this models are going to die! %s" + bcolors.ENDC
print(will_be_deleted_text %("the models are:"))
for m in models:
    print(bcolors.FAIL + "%s => (%s records)" %(m.__name__, m.objects.count()) + bcolors.ENDC)
print(will_be_deleted_text %(""))

confirm = None
confirm = input("TO CONTINUE TYPE %s YES %s :"%(bcolors.HEADER, bcolors.ENDC)).lower()
if confirm != "yes":
    raise Exception("User Canceled ")

for model in get_models():
    print("Deleting ==> %s" %(bcolors.FAIL + model.__name__) + bcolors.ENDC)
    model.objects.all().delete()

# Let's create two users one for dashboard and another for quickbooks authentication.
print("Creating a user for quickbooks authentication. username = quickbooks password = kickstart")
qb = User.objects.create_user('quickbooks', 'quickbooks@localhost.com', 'kickstart')
print("Creating a django password username = admin password = admin")
User.objects.create_superuser('admin', 'admin@localhost.com', 'admin')

# Generates some quickbooks messages.
print("Generating Quickbooks messages")
q = QBXML().initial()
for query in q:

    MessageQue.objects.create(name=query['name'], message=query['message'], description='Auto Generated', repeat=True,
                              user=qb)
    print("Generated: %s" %(query['name']))

