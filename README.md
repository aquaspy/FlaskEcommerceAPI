# This is a ecommerce API in flask. 


# Using the API

To use the API, you can use the following curl

```
curl -X POST http://127.0.0.1:5000/api/products/add -H "Content-Type: application/json" -d '{"name": "Laptop", "price": 1999.99, "description": "Gaming laptop2"}'

curl -X DELETE http://127.0.0.1:5000/api/products/delete/2

curl -X PUT http://127.0.0.1:5000/api/products/update/3 -H "Content-Type: application/json" -d '{ "price": 4500.99, "description": "Gaming laptop3"}'
```
