// resolvers/customerResolver.js

const customerResolver = {
    Query: {
      customers: async (parent, args, { db }) => {
        const query = 'SELECT * FROM customers';
        const result = await db.query(query);
        return result.rows;
      },
      customer: async (parent, { id }, { db }) => {
        const query = 'SELECT * FROM customers WHERE id = $1';
        const values = [id];
        const result = await db.query(query, values);
        return result.rows[0];
      }
    },
    Customer: {
      accounts: async (parent, args, { db }) => {
        const query = 'SELECT * FROM accounts WHERE customer_id = $1';
        const values = [parent.id];
        const result = await db.query(query, values);
        return result.rows;
      }
    },
  };
  
  module.exports = customerResolver;
  