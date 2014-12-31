Quickbooks & Django Desktop
===========================================

####A very messy implementation of Quickbooks desktop mirroring.
####Two-way communication between Quickbooks and Django/Python.

Requirements:
 - python 3.4 (Tested on 3.4.2)
 - pip

## To Start :

### Clone this repo
```https://github.com/royendgel/django-quickbooks.git```

### Install the requirements (it's recommended using virtualenv)
```pip install -r requirements.txt```

### Do database migration
```python manage.py migrate```

### Run the initial python file to kick start trying otherwise not.
```python initialize.py```

### Start the server
```python manage.py runserver```

Note : Remember if you are using mac/linux and you are trying this with virualbox or remote.
Change your server to 0.0.0.0:8000

### Double click on the webconnector file in this directory
as password enter kickstart



###Tested with 9500 entries. it is working ! Work in progress.

Need to be done (Two way communication ) :

- Customers
- Accounts
- Estimates
- Invoices


More things:
- Advanced queries(Not really I don't see why for now)
- Irritation for big company files

#####Any Question or help contact me: royendgel@techprocur.com