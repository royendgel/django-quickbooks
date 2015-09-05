Django Quickbooks Desktop
===========================================

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

### Run the initial python file to kick start trying. (Use only in clean installation!!)
### It will wipe all your models.
`python initialize.py`

### Start the server
`python manage.py runserver`

Note : Remember if you are using mac/linux and you are trying this with virualbox/VM.
Change your server to 0.0.0.0:8000

### Get the webconnector file
Open your browser and go to http://localhost:8000/quickbooks/get-company-file
open that file in your text editor and edit your server url.
or better edit in views : get_company_file

```python
def get_company_file(request):
    response = HttpResponse(generate_qbc_file(), content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename="quickbooksconnector.qwc"'
    return response

```

change `generate_qbc_file()` to something like this `generate_qbc_file(app_url="http://192.168.1.20/quickbooks/")`
remember the trailing slash at quickbooks/.

run that file on the computer that have quickbooks & webconnector installed.

Then finally enter the password for the company file.
as password enter kickstart


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