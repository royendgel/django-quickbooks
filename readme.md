Quickbooks & Django Desktop
===========================================

####A very messy implementation of Quickbooks desktop mirroring.
#####You get everything without magic.
####Two-way communication between Quickbooks and Django/Python.

Requirements:
 - python 3.4 (Tested on 3.4.2)
 - pip

## To Start :

### Clone this repo
`git clone https://github.com/royendgel/django-quickbooks.git`

### Install the requirements (it's recommended using virtualenv)
`pip install -r requirements.txt`

### Do database migration
`python manage.py migrate`

### Run the initial python file to kick start trying otherwise not. (Use only in clean installation!!)
### It will wipe all your models.
`python initialize.py`

### Start the server
`python manage.py runserver`

Note : Remember if you are using mac/linux and you are trying this with virualbox or remote.
Change your server to 0.0.0.0:8000

### Double click on the webconnector file in this directory
as password enter kickstart



###Tested with 9500 entries. it is working ! Work in progress.

Currently if you start as described above with intialize.py it will read and store data as xml in your db.
This are the tested queries read:

- Customer
- Bill
- Account
- Check
- Account
- Estimate
- Invoice
- ReceivePayment
- Vendor
- ToDo


Need to be done (Write new and/or modified records back to quickbooks) :

- Customer
- Bill
- Account
- Check
- Account
- Estimate
- Invoice
- ReceivePayment
- Vendor
- ToDo


More things:
- Time stamped so I can ask for only changed or added records
- Irritation for big company files
- Advanced queries(Not really I don't see why for now)

#####Any Question or help contact me: royendgel@techprocur.com