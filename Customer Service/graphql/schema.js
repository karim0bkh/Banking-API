// graphql/schema.js

const { gql } = require('apollo-server-express');

const typeDefs = gql`
  type Customer {
    id: ID!
    name: String!
    email: String!
    accounts: [Account]
  }

  type Account {
    id: ID!
    accountNumber: String!
    balance: Float!
    currency: String!
    customer: Customer!
  }

  type Query {
    customers: [Customer]
    customer(id: ID!): Customer
    accounts: [Account]       
    account(id: ID!): Account 
  }
`;

module.exports = typeDefs;
