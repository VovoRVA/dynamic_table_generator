# Dynamic Models Generator
This Django application provides a REST API for creating and managing dynamic models with variable fields. The models can be created at runtime with fields specified in the request. The API allows creating and updating the models, adding rows to the models, and retrieving the rows.

## Design Decisions and Caveats

Based on my understanding, the API must maintain the functionality of the Django ORM while allowing for dynamic model definition. To achieve this, we are leveraging the power of Django and its ORM rather than opting for a lower-level approach. While this approach allows for dynamic model definition from models, it poses challenges with cache control. To overcome these challenges, my development approach emphasizes simplicity and follows best practices to ensure high performance and maintainability.


However, the current implementation has some downsides that should be addressed in the future. Firstly, the cache management is not optimal, and there is room for improvement in this area. Secondly, the current implementation offers a limited amount of options for customizing the models, which could be problematic if more complex models are needed. It should be noted that the current implementation is more of a proof of concept (POC) approach, aimed at demonstrating the basic functionality of the API.

One aspect that has not been implemented is authentication, which is not strictly necessary for the current testing purposes. However, in a production environment, authentication should be implemented to ensure security and privacy of the data.

Overall, the current implementation of the API provides a functional and easy-to-use solution for dynamic model definition, while keeping the ORM functionality of Django intact. However, there is room for improvement in some areas, and future development should aim to address these issues.
# Usage

## Creating a dynamic model
To create a dynamic model, send a POST request to the /table/ endpoint with the following parameters in the request body:

model_name: The name of the model to create.
fields: A dictionary of field names and types. The types can be string, number, or boolean.

Example request:

`

```javascript
POST /table/
{
    "model_name": "Product",
    "fields": {
        "name": "string",
        "price": "number",
        "available": "boolean"
    }
}
```

## Updating a dynamic model
To update a dynamic model, send a PUT request to the /table/{id}/ endpoint, where {id} is the ID of the model to update. 
The request body should have the same format as for creating a dynamic model.

Example request:

```javascript
PUT /table/1/
{
    "model_name": "Product",
    "fields": {
        "name": "string",
        "price": "number",
        "available": "boolean",
        "description": "string"
    }
}
```

## Creating a row
To create a row in a dynamic model, send a POST request to the /table/{id}/row/ endpoint, where {id} is the ID of the model. The request body should be a dictionary of field names and values.

Example request:

```javascript
PUT /table/1/row/
{
    "name": "Product 1",
    "price": 19.99,
    "available": true
}
```
## Retrieving rows
To retrieve rows from a dynamic model, send a GET request to the /table/{id}/rows/ endpoint, where {id} is the ID of the model. The response will be a list of row dictionaries, where each dictionary represents a row in the model.

```
GET /table/1/rows/
```




