from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import requests
import grpc_requests

app = Flask(__name__)


#transaction microservice starts here
@app.route('/transfer', methods=['POST'])
def transfer():
    endpoint = "localhost:50051"  # Replace with the actual gRPC server endpoint

    # Create a gRPC client
    client = grpc_requests.Client(endpoint)

    # Create the gRPC request payload
    payload = request.get_json()

    # Send the gRPC request
    response = client.request("transaction.TransactionService", "Transfer", payload)
    print(response)
    return response
    # Extract the transactions from the response
    #re = response.get("transactions", [])

@app.route('/deposit', methods=['POST'])
def deposit():
    endpoint = "localhost:50051"  # Replace with the actual gRPC server endpoint

    # Create a gRPC client
    client = grpc_requests.Client(endpoint)

    # Create the gRPC request payload
    payload = request.get_json()

    # Send the gRPC request
    response = client.request("transaction.TransactionService", "Deposit", payload)
    print(response)
    return response
    # Extract the transactions from the response
    #re = response.get("transactions", [])

@app.route('/withdraw', methods=['POST'])
def withdraw():
    endpoint = "localhost:50051"  # Replace with the actual gRPC server endpoint

    # Create a gRPC client
    client = grpc_requests.Client(endpoint)

    # Create the gRPC request payload
    payload = request.get_json()

    # Send the gRPC request
    response = client.request("transaction.TransactionService", "Withdraw", payload)
    print(response)
    return response
    # Extract the transactions from the response
    #re = response.get("transactions", [])

@app.route('/get_transaction', methods=['POST'])
def get_transaction():
    endpoint = "localhost:50051"  # Replace with the actual gRPC server endpoint

    # Create a gRPC client
    client = grpc_requests.Client(endpoint)

    # Create the gRPC request payload
    payload = request.get_json()

    # Send the gRPC request
    response = client.request("transaction.TransactionService", "GetTransaction", payload)
    print(response)
    return response

#transaction microservice ends here



#reporting microservice starts here
@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.get_json()
    response = requests.post('http://localhost:8004/generate_report', json=data)
    return jsonify(response.json()), response.status_code
#reporting microservice ends here

#account service starts here 

api = Api(app)

CUSTOMER_SERVICE_URL = "http://localhost:8001"
ACCOUNT_SERVICE_URL = "http://localhost:8001"

class CustomerResource(Resource):
    def post(self):
        # Proxy the request to the customer service
        data = request.get_json()
        response = requests.post(f"{CUSTOMER_SERVICE_URL}/customers", json=data)
        print(response)
        return response.json(), response.status_code

    def put(self, customer_id):
        # Proxy the request to the customer service
        response = requests.put(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}", json=request.get_json())
        return response.json(), response.status_code

    def delete(self, customer_id):
        # Proxy the request to the customer service
        response = requests.delete(f"{CUSTOMER_SERVICE_URL}/customers/{customer_id}")
        return response.json(), response.status_code


# Account resource
class AccountResource(Resource):
    def post(self, customer_id):
        # Proxy the request to the account service
        response = requests.post(f"{ACCOUNT_SERVICE_URL}/customers/{customer_id}/accounts", json=request.get_json())
        return response.json(), response.status_code

    def put(self, customer_id, account_id):
        # Proxy the request to the account service
        response = requests.put(f"{ACCOUNT_SERVICE_URL}/customers/{customer_id}/accounts/{account_id}", json=request.get_json())
        return response.json(), response.status_code

    def delete(self, customer_id, account_id):
        # Proxy the request to the account service
        response = requests.delete(f"{ACCOUNT_SERVICE_URL}/customers/{customer_id}/accounts/{account_id}")
        return response.json(), response.status_code


# API routes
api.add_resource(CustomerResource, "/customers", "/customers/<int:customer_id>")
api.add_resource(AccountResource, "/customers/<int:customer_id>/accounts", "/customers/<int:customer_id>/accounts/<int:account_id>")



#account service ends here

#auth service starts here

@app.route('/login', methods=['POST'])
def login():
    # Extract the username and password from the request's Basic Authentication credentials
    auth = request.authorization

    # Check if the required credentials are present
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Invalid credentials555.'}), 401

    # Make a request to the desired endpoint with the Basic Authentication credentials
    url = "http://localhost:8002/login"
    username = auth.username
    password = auth.password
    response = requests.post(url, auth=(username, password))
    # Print the response for debugging purposes
    print(response)

    # Return the response and status code as a JSON response
    return jsonify(response.json()), response.status_code


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response = requests.post('http://localhost:8002/register', json=data)
    return jsonify(response.json()), response.status_code


#auth service ends here
GRAPHQL_SERVICE_URL = "http://localhost:8003/graphql"

@app.route('/graphql', methods=['POST'])
def graphql():
    # Proxy the GraphQL request to the GraphQL service
    response = requests.post(GRAPHQL_SERVICE_URL, json=request.get_json())
    return jsonify(response.json()), response.status_code


#customer service starts here


#customer service ends here

if __name__ == '__main__':
    app.run(debug=True)
 