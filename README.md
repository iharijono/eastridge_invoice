# What is this
This is a README for a simplified demo invoice app

## Contents
- Remarks
- Requirements for deployment & test    
- Quickstart: Test & Debug    

## Remarks
- I do not wish to use elaborated directory/file layouts (and python packaging techniques) right now as I want to keep the demo quick to implement (sorry for that), straight-forward and easy to use/demonstrate.     
  The application does NOT have a lot of logics and abstraction right now,
  instead it focuses on the data model, database and its access.
  Therefore it does not make a lot of sense to have unit tests (as there is hardly complicated logics here).
  So I decided to forsake the (unit) tests in order to quickly implement the functionalities. 
- I strive to avoid using external python library if it is not a must (see the requirements below).   
- As the project description does NOT specify to implement complete CRUD operations, only 'create' is implemented. So the data is never deleted/updated (via the demo application)
- Consequently, there is no delete operation supported for Invoice and InvoiceItem. If delete an Invoice in the DB manually, there will NOT be a cascade delete automatically (its invoice items are deleted as well)
- In other words, the behaviour of update and delete are NOT defined here!
- However, I provide 'read' or get for the sake of making sure that the creation of invoice and invoice items are persisted.

## Requirements for deployment & test  
- Python 3.x.x and pip (refer to how to install python for your development environment)  
- sqlalchemy and sqlite (installed together with sqlalchemy)
```
% pip install sqlalchemy

```
- flask  
```
% pip install flask

```  
OR better
- Install all python libraries with requirements.txt
```
% pip install -r requirements.txt

```  
- curl or any other REST API client (postman)

## Quickstart: Test & Debug       
- Start the app that print the information how to use it:   
```
% python main.py -h

```  
- Start the app (backend) to accept RESTful API request:   
```
% python main.py

or with more output:

% python main.py -v

```  
- Run the REST API client ('curl') against the URL (use 'POST' to create a new invoice, 'GET' to retrieve it back)    
WARNING: Please give the date with the correct format YYYY-MM-DD, I do NOT make a sanity check on the back end this time, Sorry!!!

- INVOICE  

-- Retrieve all invoices from the DB
```
% curl -i http://localhost:9000/invoices
# you will get JSON formatted data, something like {"invoices": []}
```

-- Add an invoices in the DB with default date of 'today'
```
% curl -i -H "Content-Type: application/json" -X POST -d '{}' http://localhost:9000/invoices
{
  "invoice_id": 4
}
```

-- Add an invoices in the DB with date of 02-10-2020, please give the correct date format below!! sorry, I do NOT check the format at the back end!!!
```
# on linux
% curl -i -H "Content-Type: application/json" -X POST -d '{"date":"2020-02-10"}' http://localhost:9000/invoices
# on windows
> curl.exe -i -H "Content-Type: application/json" -X POST -d '{"""date""":"""2020-02-10"""}' http://localhost:9000/invoices
#
# IMPORTANT: you will get the invoice_id of the newly created invoice.
#            remember this id as you will need it if you want to create
#            invoice items that belongs to this invoice
{
  "invoice_id": 4
}
```  
-- Retrieve AGAIN all invoices from the DB
```
% curl -i http://localhost:9000/invoices
# you will get JSON formatted data for example:
[
  {
    "date": "Mon, 10 Feb 2020 00:00:00 GMT",
    "id": 1,
    "invoice_items": []
  },
  {
    "date": "Wed, 05 Feb 2020 00:00:00 GMT",
    "id": 2,
    "invoice_items": []
  },
  {
    "date": "Thu, 06 Feb 2020 00:00:00 GMT",
    "id": 3,
    "invoice_items": []
  }
]
```    
-- You can also retrieve a specific invoice (by its ID)
```
% curl -i http://localhost:9000/invoices/2
# you will get JSON formatted data for example:

  {
    "date": "Wed, 05 Feb 2020 00:00:00 GMT",
    "id": 2,
    "invoice_items": []
  }
```   

- INVOICE ITEM

-- Add an invoice item to the invoice id '1' (you must have created the invoice, see above) 
```
# on linux
% curl -i -H "Content-Type: application/json" -X POST -d '{"units":"3", "amount": "10.15", "description" : "t-shirt", "invoice_id": "1"}' http://localhost:9000/invoice_items
# on windows
> curl.exe -i -H "Content-Type: application/json" -X POST -d '{"""units""":"""3""", """amount""": """10.15""", """description""" : """t-shirt""", """invoice_id""": """1"""}' http://localhost:9000/invoice_items
#
# WARNING: There is NO sanity check on the backend, please give a correct value for the unit, amount and invoice_id
# 
{
  "invoice_item_id": 1
}
```    
-- Add another invoice item to the invoice id '1' (you must have created the invoice, see above) 
```
# on linux
% curl -i -H "Content-Type: application/json" -X POST -d '{"units":"2", "amount": "110.15", "description" : "t-shirt111", "invoice_id": "1"}' http://localhost:9000/invoice_items
# on windows
> curl.exe -i -H "Content-Type: application/json" -X POST -d '{"""units""":"""2""", """amount""": """110.15""", """description""" : """t-shirt111""", """invoice_id""": """1"""}' http://localhost:9000/invoice_items
#
# WARNING: There is NO sanity check on the backend, please give a correct value for the unit, amount and invoice_id
# 
{
  "invoice_item_id": 2
}
```    
-- Retrieve AGAIN all invoices from the DB
```
% curl -i http://localhost:9000/invoices
# you will get JSON formatted data for example:
[
  {
    "date": "Mon, 10 Feb 2020 00:00:00 GMT",
    "id": 1,
    "invoice_items": [
      {
        "amount": "10.15",
        "description": "t-shirt",
        "id": 1,
        "invoice_id": 1,
        "units": 3
      },
      {
        "amount": "110.15",
        "description": "t-shirt111",
        "id": 2,
        "invoice_id": 1,
        "units": 2
      }
    ]
  },
  {
    "date": "Wed, 05 Feb 2020 00:00:00 GMT",
    "id": 2,
    "invoice_items": []
  },
  {
    "date": "Thu, 06 Feb 2020 00:00:00 GMT",
    "id": 3,
    "invoice_items": []
  }
]
```    
