# Banking-API
a Banking API using gRPC , REST and GraphQL using TypeScript, Python, GoLang , PostgreSQL as a database.
<h1 align="center">API Gateway Documentation</h1>

This documentation provides an overview of the API gateway, which serves as a central entry point for routing requests to various microservices. The API gateway is built using Flask and acts as a proxy for the underlying microservices.

## Transaction Microservice

- **Endpoint**: `/transfer`
  - **Method**: POST
  - **Description**: Handles the transfer of funds.
  - **Payload**: {
  "fromAccountId": "account1",
  "toAccountId": "account2",
  "amount": 100.0
}

  - **gRPC request**: `Transfer`

- **Endpoint**: `/deposit`
  - **Method**: POST
  - **Description**: Handles the deposit of funds.
  - **Payload**: {
  "accountId": "account1",
  "amount": 200.0
}
  - **gRPC request**: `Deposit`

- **Endpoint**: `/withdraw`
  - **Method**: POST
  - **Description**: Handles the withdrawal of funds.
  - **Payload**: {
  "accountId": "account1",
  "amount": 200.0
}
  - **gRPC request**: `Withdraw`

- **Endpoint**: `/get_transaction`
  - **Method**: POST
  - **Description**: Retrieves transaction details.
  - **Payload**: {
  "transactionId": "transaction1"
}
  - **gRPC request**: `GetTransaction`

## Reporting Microservice

- **Endpoint**: `/generate_report`
  - **Method**: POST
  - **Description**: Generates a report using the provided data.
  - **Payload**: {
  "customerId": "customer1"
}
  - **HTTP request**: POST to `http://localhost:8004/generate_report`

## Account Service

- **Endpoint**: `/customers`
  - **Method**: POST
  - **Payload**: {
    "name" : "test user",
    "email" : "test@email.com"
 }
  - **Description**: Proxy the request to the customer service to create a new customer.

- **Endpoint**: `/customers/<int:customer_id>`
  - **Method**: PUT
  - **Payload**: {
    "name" : "update user",
    "email" : "test2@email.com"
 }
  - **Description**: Proxy the request to the customer service to update an existing customer.

- **Endpoint**: `/customers/<int:customer_id>`
  - **Method**: DELETE
  - **Description**: Proxy the request to the customer service to delete an existing customer.

- **Endpoint**: `/customers/<int:customer_id>/accounts`
  - **Method**: POST
  - **Payload**: {"account_number": "1234567890", "balance": 1000, "currency": "USD"}
  - **Description**: Proxy the request to the account service to create a new account for a customer.

- **Endpoint**: `/customers/<int:customer_id>/accounts/<int:account_id>`
  - **Method**: PUT
  - **Payload**: {"account_number": "77777777", "balance": 8000, "currency": "USD"}
  - **Description**: Proxy the request to the account service to update an existing account for a customer.

- **Endpoint**: `/customers/<int:customer_id>/accounts/<int:account_id>`
  - **Method**: DELETE
  - **Description**: Proxy the request to the account service to delete an existing account for a customer.

## Auth Service

- **Endpoint**: `/login`
  - **Method**: POST
  - **Payload**: {
    "username" : "username",
    "password" : "123456"
 }
  - **Description**: Authenticates a user based on the provided credentials using Basic Authentication.
  - **HTTP request**: POST to `http://localhost:8002/login`

- **Endpoint**: `/register`
  - **Method**: POST
  - **Payload**: {
    "email" : "user@email.com"
    "username" : "username",
    "password" : "123456"
 }
  - **Description**: Registers a new user using the provided data.
  - **HTTP request**: POST to `http://localhost:8002/register`

## Customer Service

- **Endpoint**: `/graphql`
  - **Method**: POST
  - **Description**: Proxies the GraphQL request to the GraphQL service.
  - **HTTP request**: POST to `http://localhost:8003/graphql`

> Note: this project was made by Karim Ben Khaled.


</details>
