const {ApolloServer, gql} = require('apollo-server');
const {ApolloGateway, IntrospectAndCompose} = require('@apollo/gateway');
const {serializeQueryPlan} = require('@apollo/query-planner');

const gateway = new ApolloGateway({
    supergraphSdl: new IntrospectAndCompose({
        subgraphs: [
            {name: 'flights', url: 'http://localhost:8000/graphql'},
            {name: 'users', url: 'http://localhost:8001/graphql'},
            // ...additional subgraphs...
        ],
    }),

    experimental_didResolveQueryPlan: function (options) {
        if (options.requestContext.operationName !== 'IntrospectionQuery') {
            const fs = require('fs');

            const content = serializeQueryPlan(options.queryPlan);
            try {
                fs.writeFileSync('./plan.txt', content);
                // file written successfully
            } catch (err) {
                console.error(err);
            }
        }
    }
});


// Pass the ApolloGateway to the ApolloServer constructor
const server = new ApolloServer({
    gateway,
});

server.listen().then(({url}) => {
    console.log(`🚀 Server ready at ${url}`);
});