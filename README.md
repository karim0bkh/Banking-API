# Banking-API
a Banking API using gRPC , REST and GraphQL using TypeScript, Python, GoLang and Rust , PostgreSQL as a database.
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
  - **gRPC request**: `Deposit`

- **Endpoint**: `/withdraw`
  - **Method**: POST
  - **Description**: Handles the withdrawal of funds.
  - **gRPC request**: `Withdraw`

- **Endpoint**: `/get_transaction`
  - **Method**: POST
  - **Description**: Retrieves transaction details.
  - **gRPC request**: `GetTransaction`

## Reporting Microservice

- **Endpoint**: `/generate_report`
  - **Method**: POST
  - **Description**: Generates a report using the provided data.
  - **HTTP request**: POST to `http://localhost:8004/generate_report`

## Account Service

- **Endpoint**: `/customers`
  - **Method**: POST
  - **Description**: Proxy the request to the customer service to create a new customer.

- **Endpoint**: `/customers/<int:customer_id>`
  - **Method**: PUT
  - **Description**: Proxy the request to the customer service to update an existing customer.

- **Endpoint**: `/customers/<int:customer_id>`
  - **Method**: DELETE
  - **Description**: Proxy the request to the customer service to delete an existing customer.

- **Endpoint**: `/customers/<int:customer_id>/accounts`
  - **Method**: POST
  - **Description**: Proxy the request to the account service to create a new account for a customer.

- **Endpoint**: `/customers/<int:customer_id>/accounts/<int:account_id>`
  - **Method**: PUT
  - **Description**: Proxy the request to the account service to update an existing account for a customer.

- **Endpoint**: `/customers/<int:customer_id>/accounts/<int:account_id>`
  - **Method**: DELETE
  - **Description**: Proxy the request to the account service to delete an existing account for a customer.

## Auth Service

- **Endpoint**: `/login`
  - **Method**: POST
  - **Description**: Authenticates a user based on the provided credentials using Basic Authentication.
  - **HTTP request**: POST to `http://localhost:8002/login`

- **Endpoint**: `/register`
  - **Method**: POST
  - **Description**: Registers a new user using the provided data.
  - **HTTP request**: POST to `http://localhost:8002/register`

## Customer Service

- **Endpoint**: `/graphql`
  - **Method**: POST
  - **Description**: Proxies the GraphQL request to the GraphQL service.
  - **HTTP request**: POST to `http://localhost:8003/graphql`

> Note: this project was made by Karim Ben Khaled.


</details>
