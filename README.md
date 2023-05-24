# Banking-API
a Banking API using gRPC , REST and GraphQL using TypeScript, Python, GoLang , PostgreSQL as a database.
<h1 align="center">API Gateway Documentation</h1>

This documentation provides an overview of the API gateway, which serves as a central entry point for routing requests to various microservices. The API gateway is built using Flask and acts as a proxy for the underlying microservices.


## Customer Service

Use GraphQL: GraphQL allows clients to fetch customer information and account details in a flexible and efficient manner. Clients can request specific fields and nested data structures, reducing over-fetching and allowing them to shape the data according to their needs.

## Account Service

Use REST: REST provides a standardized and familiar interface for managing bank accounts. Clients can perform CUD operations on accounts using HTTP verbs (POST, PUT, DELETE) and access account-related endpoints such as deleting account details, creating accounts, and performing usual requests about accounts and customer details.

## Transaction Service

Use gRPC: gRPC can be used for inter-service communication between the Transaction Service and other microservices, such as the Account Service. gRPC's efficiency and binary serialization make it suitable for real-time and high-performance scenarios involving transaction processing.

## Authentication Service

Use REST: REST is well-suited for client authentication and token generation. Clients can make HTTP requests to register, login, and obtain authentication tokens for subsequent API calls.

## Reporting Service

Use REST: Depending on the complexity and flexibility required by the reporting functionality, implementing a RESTful API for the Reporting Service microservice. REST is suitable for predefined reports with fixed data structures.

## API Endpoints

For detailed information about the API endpoints and their usage, please refer to the following sections:

- [Transaction Microservice](#transaction-microservice)
- [Reporting Microservice](#reporting-microservice)
- [Account Service](#account-service)
- [Auth Service](#auth-service)
- [GraphQL Service](#graphql-service)



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
