// index.js

const express = require('express');
const { ApolloServer } = require('apollo-server-express');
const { Pool } = require('pg');
const typeDefs = require('./graphql/schema');
const customerResolver = require('./resolvers/customerResolver');
const accountResolver = require('./resolvers/accountResolver');

const app = express();

// PostgreSQL database configuration
const pool = new Pool({
  host: 'localhost',
  port: '5432',
  user: 'postgres',
  password: 'karimbkh',
  database: 'bank'
});

// Create Apollo Server
const server = new ApolloServer({
  typeDefs,
  resolvers: [customerResolver, accountResolver],
  context: {
    db: pool
  }
});

async function startServer() {
  await server.start();

  // Apply middleware to Express app
  server.applyMiddleware({ app });

  // Start the server
  const PORT = 8003;
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`GraphQL Playground available at http://localhost:${PORT}${server.graphqlPath}`);
  });
}

startServer();
