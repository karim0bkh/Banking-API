// resolvers/accountResolver.js

const accountResolver = {
    Query: {
      accounts: async (parent, args, { db }) => {
        const query = 'SELECT * FROM accounts';
        const result = await db.query(query);
        return result.rows;
      },
      account: async (parent, { id }, { db }) => {
        const query = 'SELECT * FROM accounts WHERE id = $1';
        const values = [id];
        const result = await db.query(query, values);
        return result.rows[0];
      }
    },
    Account: {
      customer: async (parent, args, { db }) => {
        const query = 'SELECT * FROM customers WHERE id = $1';
        const values = [parent.customerId];
        const result = await db.query(query, values);
        return result.rows[0];
      }
    },
  };
  
  module.exports = accountResolver;
  