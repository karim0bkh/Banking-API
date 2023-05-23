package main

import (
	"database/sql"
	"fmt"
	"log"
	"github.com/google/uuid"

	pb "TransactionService/proto"
)

func retrieveAccount(db *sql.DB, accountID string) (*pb.Account, error) {
	// Retrieve account from the database based on the account ID
	query := "SELECT id, customer_id, balance FROM accounts WHERE id = $1"
	row := db.QueryRow(query, accountID)

	var account pb.Account
	err := row.Scan(&account.Id, &account.CustomerId, &account.Balance)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, fmt.Errorf("account not found")
		}
		log.Printf("failed to retrieve account: %v", err)
		return nil, err
	}

	return &account, nil
}

func updateAccount(db *sql.DB, account *pb.Account) error {
	// Update the account in the database
	query := "UPDATE accounts SET balance = $1 WHERE id = $2"
	_, err := db.Exec(query, account.Balance, account.Id)
	if err != nil {
		log.Printf("failed to update account: %v", err)
		return err
	}

	return nil
}

func saveTransaction(db *sql.DB, transaction *pb.Transaction) error {
	// Save the transaction to the database
	query := "INSERT INTO transactions (id, from_account_id, to_account_id, amount) VALUES ($1, $2, $3, $4)"
	_, err := db.Exec(query, transaction.TransactionId, transaction.FromAccountId, transaction.ToAccountId, transaction.Amount)
	if err != nil {
		log.Printf("failed to save transaction: %v", err)
		return err
	}

	return nil
}
func saveTransaction_Transaction_WITHDRAWAL(db *sql.DB, transaction *pb.Transaction_WITHDRAWAL) error {
	// Save the transaction to the database
	query := "INSERT INTO transactions (id, from_account_id, to_account_id, amount) VALUES ($1, $2, $3, $4)"
	_, err := db.Exec(query, transaction.TransactionId, transaction.AccountId, transaction.AccountId, transaction.Amount)
	if err != nil {
		log.Printf("failed to save transaction: %v", err)
		return err
	}

	return nil
}
func saveTransaction_Transaction_DEPOSIT(db *sql.DB, transaction *pb.Transaction_DEPOSIT) error {
	// Save the transaction to the database
	query := "INSERT INTO transactions (id, from_account_id, to_account_id, amount) VALUES ($1, $2, $3, $4)"
	_, err := db.Exec(query, transaction.TransactionId, transaction.AccountId, transaction.AccountId, transaction.Amount)
	if err != nil {
		log.Printf("failed to save transaction: %v", err)
		return err
	}

	return nil
}

func retrieveTransaction(db *sql.DB, transactionID string) (*pb.Transaction, error) {
	// Retrieve transaction from the database based on the transaction ID
	query := "SELECT id, from_account_id, to_account_id, amount FROM transactions WHERE id = $1"
	row := db.QueryRow(query, transactionID)

	var transaction pb.Transaction
	err := row.Scan(&transaction.TransactionId, &transaction.FromAccountId, &transaction.ToAccountId, &transaction.Amount)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, fmt.Errorf("transaction not found")
		}
		log.Printf("failed to retrieve transaction: %v", err)
		return nil, err
	}

	return &transaction, nil
}

func retrieveTransactionsByCustomer(db *sql.DB, customerID string) ([]*pb.Transaction, error) {
	// Retrieve transactions from the database for the given customer ID
	query := "SELECT id, from_account_id, to_account_id, amount FROM transactions WHERE from_account_id IN (SELECT id FROM accounts WHERE customer_id = $1) OR to_account_id IN (SELECT id FROM accounts WHERE customer_id = $1)"
	rows, err := db.Query(query, customerID)
	if err != nil {
		log.Printf("failed to retrieve transactions: %v", err)
		return nil, err
	}
	defer rows.Close()

	var transactions []*pb.Transaction
	for rows.Next() {
		var transaction pb.Transaction
		err := rows.Scan(&transaction.TransactionId, &transaction.FromAccountId, &transaction.ToAccountId, &transaction.Amount)
		if err != nil {
			log.Printf("failed to retrieve transaction: %v", err)
			return nil, err
		}
		transactions = append(transactions, &transaction)
	}

	return transactions, nil
}

func generateTransactionID() string {
	// Generate a unique transaction ID using UUID (Universally Unique Identifier)
	id := uuid.New()
	transactionID := id.String()
	return transactionID
}