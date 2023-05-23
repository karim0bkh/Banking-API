package main

import (
	"context"
	"log"

	pb "TransactionService/proto"
)

func (s *server) mustEmbedUnimplementedTransactionServiceServer() {}


func (s *server) Transfer(ctx context.Context, req *pb.TransferRequest) (*pb.TransferResponse, error) {
	fromAccountID := req.GetFromAccountId()
	toAccountID := req.GetToAccountId()
	amount := req.GetAmount()

	// Retrieve from account details
	fromAccount, err := retrieveAccount(s.db, fromAccountID)
	if err != nil {
		log.Printf("failed to retrieve from account: %v", err)
		return nil, err
	}

	// Retrieve to account details
	toAccount, err := retrieveAccount(s.db, toAccountID)
	if err != nil {
		log.Printf("failed to retrieve to account: %v", err)
		return nil, err
	}

	// Check if the from account has sufficient balance
	if fromAccount.Balance < amount {
		return &pb.TransferResponse{
			Success: false,
			Message: "insufficient balance in the from account",
		}, nil
	}

	// Perform the transfer
	fromAccount.Balance -= amount
	toAccount.Balance += amount

	// Update from account in the database
	err = updateAccount(s.db, fromAccount)
	if err != nil {
		log.Printf("failed to update from account: %v", err)
		return nil, err
	}

	// Update to account in the database
	err = updateAccount(s.db, toAccount)
	if err != nil {
		log.Printf("failed to update to account: %v", err)
		return nil, err
	}

	// Create transaction record
	transactionID := generateTransactionID()
	transaction := &pb.Transaction{
		TransactionId: transactionID,
		FromAccountId: fromAccountID,
		ToAccountId:   toAccountID,
		Amount:        amount,
	}

	// Save transaction to the database
	err = saveTransaction(s.db, transaction)
	if err != nil {
		log.Printf("failed to save transaction: %v", err)
		return nil, err
	}

	return &pb.TransferResponse{
		Success:      true,
		Message:      "Transfer successful",
	}, nil
}

func (s *server) Deposit(ctx context.Context, req *pb.DepositRequest) (*pb.DepositResponse, error) {
	accountID := req.GetAccountId()
	amount := req.GetAmount()

	// Retrieve account details
	account, err := retrieveAccount(s.db, accountID)
	if err != nil {
		log.Printf("failed to retrieve account: %v", err)
		return nil, err
	}

	// Perform the deposit
	account.Balance += amount

	// Update account in the database
	err = updateAccount(s.db, account)
	if err != nil {
		log.Printf("failed to update account: %v", err)
		return nil, err
	}

	// Create transaction record
	transactionID := generateTransactionID()
	transaction := &pb.Transaction_DEPOSIT{
		TransactionId: transactionID,
		AccountId:       accountID,
		Amount:        amount,
	}

	// Save transaction to the database
	err = saveTransaction_Transaction_DEPOSIT(s.db, transaction)
	if err != nil {
		log.Printf("failed to save transaction: %v", err)
		return nil, err
	}

	return &pb.DepositResponse{
		Success:      true,
		Message:      "Deposit successful",
	}, nil
}

func (s *server) Withdraw(ctx context.Context, req *pb.WithdrawRequest) (*pb.WithdrawResponse, error) {
	accountID := req.GetAccountId()
	amount := req.GetAmount()

	// Retrieve account details
	account, err := retrieveAccount(s.db, accountID)
	if err != nil {
		log.Printf("failed to retrieve account: %v", err)
		return nil, err
	}

	// Check if the account has sufficient balance
	if account.Balance < amount {
		return &pb.WithdrawResponse{
			Success: false,
			Message: "insufficient balance in the account",
		}, nil
	}

	// Perform the withdrawal
	account.Balance -= amount

	// Update account in the database
	err = updateAccount(s.db, account)
	if err != nil {
		log.Printf("failed to update account: %v", err)
		return nil, err
	}

	// Create transaction record
	transactionID := generateTransactionID()
	transaction := &pb.Transaction_WITHDRAWAL{
		TransactionId: transactionID,
		AccountId:       accountID,
		Amount:        amount,
	}

	// Save transaction to the database
	err = saveTransaction_Transaction_WITHDRAWAL(s.db, transaction)
	if err != nil {
		log.Printf("failed to save transaction: %v", err)
		return nil, err
	}

	return &pb.WithdrawResponse{
		Success:      true,
		Message:      "Withdrawal successful",
	}, nil
}

func (s *server) GetTransaction(ctx context.Context, req *pb.GetTransactionRequest) (*pb.GetTransactionResponse, error) {
	transactionID := req.GetTransactionId()

	// Retrieve transaction details
	transaction, err := retrieveTransaction(s.db, transactionID)
	if err != nil {
		log.Printf("failed to retrieve transaction: %v", err)
		return nil, err
	}

	return &pb.GetTransactionResponse{
		Transaction: transaction,
	}, nil
}

func (s *server) GenerateReport(ctx context.Context, req *pb.GenerateReportRequest) (*pb.GenerateReportResponse, error) {
	customerID := req.GetCustomerId()

	// Retrieve transactions for the given customer ID
	transactions, err := retrieveTransactionsByCustomer(s.db, customerID)
	if err != nil {
		log.Printf("failed to retrieve transactions: %v", err)
		return nil, err
	}

	return &pb.GenerateReportResponse{
		Transactions: transactions,
	}, nil
}
