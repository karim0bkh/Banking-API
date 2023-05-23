package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"net"

	"google.golang.org/protobuf"
	pb "./"

	"google.golang.org/grpc"
)

const (
	port           = ":50051"
	dbConnectionString = "postgres://user:password@localhost/banking_db?sslmode=disable"
)

type server struct {
	db *sql.DB
}

func main() {
	// Connect to the PostgreSQL database
	db, err := sql.Open("postgres", dbConnectionString)
	if err != nil {
		log.Fatalf("failed to connect to the database: %v", err)
	}
	defer db.Close()

	// Create the transaction service server
	s := grpc.NewServer()
	pb.RegisterTransactionServiceServer(s, &server{db: db})

	// Start listening on the designated port
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	log.Printf("Server listening on port %s", port)

	// Start serving incoming requests
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
