const { ApolloServer, gql } = require('apollo-server');
require('./config.js')
const { Page } = require('./models');



// Type definitions define the "shape" of your data and specify
// which ways the data can be fetched from the GraphQL server.
const typeDefs = gql`
  # Comments in GraphQL are defined with the hash (#) symbol.

  # This "Book" type can be used in other type declarations.
  type Page {
    url: String!,
    domain: String!,
    title: String,
    og_type: String,
    og_site_name: String,
    og_image: String,
    og_title: String,
    og_url: String,
    raw_text: String
  }

  type PageFeed {
    # cursor specifies the place in the list where we left off
    cursor: String!
    
    # this is a chunk of messages to be returned
    pages: [Page]!
  }

  # The "Query" type is the root of all GraphQL queries.
  # (A "Mutation" type will be covered later on.)
  type Query {
    pages(domain: String, limit: Int, offset: Int): [Page]
  }
`;

// Resolvers define the technique for fetching the types in the
// schema. 
const resolvers = {
  Query: {
    pages: async (_, args) => {
      args.offset = args.offset || 0
      args.limit = args.limit || 10
      if (args.limit > 100 || args.limit < 0) {
        args.limit = 100
      }
      let results = await Page.find({domain: args.domain || "muzmatch.com"})
              .skip(args.offset)
              .limit(args.limit)
              .exec();
      return results
    }

    
          //  async () => await User.find({}).exec()
  }
};

// In the most basic sense, the ApolloServer can be started
// by passing type definitions (typeDefs) and the resolvers
// responsible for fetching the data for those types.
const server = new ApolloServer({ typeDefs, resolvers, listen: "0.0.0.0" });

// This `listen` method launches a web-server.  Existing apps
// can utilize middleware options, which we'll discuss later.
server.listen().then(({ url }) => {
  console.log(`🚀  Server ready at ${url}`);
});
