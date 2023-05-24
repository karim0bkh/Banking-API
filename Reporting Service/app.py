import grpc_requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/generate_report', methods=['POST'])
def handle_generate_report():
    data = request.get_json()
    customer_id = data.get("customer_id")
    if not customer_id:
        return "Customer ID is missing.", 400
    
    try:
        generate_report(customer_id)
    
        return jsonify("Report generated successfully." , 200)
    except Exception as e:
        return str(e), 500

def generate_report(customer_id):
    # Define the gRPC endpoint
    endpoint = "localhost:50051"  # Replace with the actual gRPC server endpoint

    # Create a gRPC client
    client = grpc_requests.Client(endpoint)

    # Create the gRPC request payload
    payload = {
        "customerId": customer_id
    }

    # Send the gRPC request
    response = client.request("transaction.TransactionService", "GenerateReport", payload)
    print(response)

    # Extract the transactions from the response
    transactions = response.get("transactions", [])

    # Generate the PDF
    pdf_file = f"report_{customer_id}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(100, 700, "Transaction Report")

    y = 670
    for transaction in transactions:
        # Extract transaction details
        transaction_id = transaction.get("transactionId")
        from_account_id = transaction.get("fromAccountId")
        to_account_id = transaction.get("toAccountId")
        amount = transaction.get("amount")

        # Draw transaction details on the PDF
        c.drawString(100, y , f"Transaction ID: {transaction_id}")
        c.drawString(100, y - 20, f"From Account: {from_account_id}")
        c.drawString(100, y - 40, f"To Account: {to_account_id}")
        c.drawString(100, y - 60, f"Amount: {amount}")
        c.drawString(100, y - 80, f"*****************************************")
        y -= 100

    c.save()
    print(f"Report generated: {pdf_file}")

if __name__ == '__main__':
    app.run(debug=True , port=8004)
