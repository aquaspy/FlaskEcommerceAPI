# This is a ecommerce API in flask. 

#Getting started

To use the project, it's recommended to run in a python environment.

Then, inside the environment, you can run:

```
flask shell
db.drop_all()
db.create_all()
user = User(username="admin", password="123")
db.session.add(user) 
db.session.commit()
```

This will allow the API usage.
# Using the API

Here are some examples of how you can use the API. The swagger file can be used to import the API endpoints on postman directly.

```
curl -X POST http://127.0.0.1:5000/api/products/add -H "Content-Type: application/json" -d '{"name": "Laptop", "price": 1999.99, "description": "Gaming laptop2"}'

curl -X DELETE http://127.0.0.1:5000/api/products/delete/2

curl -X PUT http://127.0.0.1:5000/api/products/update/3 -H "Content-Type: application/json" -d '{ "price": 4500.99, "description": "Gaming laptop3"}'
```
