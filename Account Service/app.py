# app.py

import os
from flask import Flask, request
from flask_restful import Api, Resource
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Customer, Account
# Load environment variables from .env file
load_dotenv()

# Create Flask application
app = Flask(__name__)
api = Api(app)

# Database connection
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
Session = sessionmaker(bind=engine)


# Customer resource
class CustomerResource(Resource):
    def post(self):
        # Create a new customer
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")

        session = Session()
        customer = Customer(name=name, email=email)
        session.add(customer)
        session.commit()
        session.close()

        return {"message": "Customer created successfully"}, 201

    def put(self, customer_id):
        # Update an existing customer
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")

        session = Session()
        customer = session.query(Customer).filter_by(id=customer_id).first()

        if customer:
            customer.name = name
            customer.email = email
            session.commit()
            session.close()
            return {"message": "Customer updated successfully"}, 200
        else:
            session.close()
            return {"message": "Customer not found"}, 404

    def delete(self, customer_id):
        # Delete a customer
        session = Session()
        customer = session.query(Customer).filter_by(id=customer_id).first()

        if customer:
            session.delete(customer)
            session.commit()
            session.close()
            return {"message": "Customer deleted successfully"}, 200
        else:
            session.close()
            return {"message": "Customer not found"}, 404


# Account resource
class AccountResource(Resource):
    def post(self, customer_id):
        # Create a new account for a customer
        data = request.get_json()
        account_number = data.get("account_number")
        balance = data.get("balance")
        currency = data.get("currency")

        session = Session()
        customer = session.query(Customer).filter_by(id=customer_id).first()

        if customer:
            account = Account(
                account_number=account_number,
                balance=balance,
                currency=currency,
                customer=customer,
            )
            session.add(account)
            session.commit()
            session.close()
            return {"message": "Account created successfully"}, 201
        else:
            session.close()
            return {"message": "Customer not found"}, 404

    def put(self, customer_id, account_id):
        # Update an account for a customer
        data = request.get_json()
        account_number = data.get("account_number")
        balance = data.get("balance")
        currency = data.get("currency")

        session = Session()
        account = (
            session.query(Account)
            .filter_by(id=account_id, customer_id=customer_id)
            .first()
        )

        if account:
            account.account_number = account_number
            account.balance = balance
            account.currency = currency
            session.commit()
            session.close()
            return {"message": "Account updated successfully"}, 200
        else:
            session.close()
            return {"message": "Account not found"}, 404

    def delete(self, customer_id, account_id):
        # Delete an account for a customer
        session = Session()
        account = (
            session.query(Account)
            .filter_by(id=account_id, customer_id=customer_id)
            .first()
        )

        if account:
            session.delete(account)
            session.commit()
            session.close()
            return {"message": "Account deleted successfully"}, 200
        else:
            session.close()
            return {"message": "Account not found"}, 404


# API routes
api.add_resource(CustomerResource, "/customers", "/customers/<int:customer_id>")
api.add_resource(
    AccountResource,
    "/customers/<int:customer_id>/accounts",
    "/customers/<int:customer_id>/accounts/<int:account_id>",
)

if __name__ == "__main__":
    app.run(debug=True , port=8001)
