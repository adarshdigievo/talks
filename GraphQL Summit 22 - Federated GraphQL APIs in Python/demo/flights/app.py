import logging
from wsgiref.simple_server import make_server

import falcon

from database import init_db
from urls.apollo_studio_sandbox import ApolloSandbox
from urls.graphql_executor import GraphQLExecutor

app = falcon.App()

app.add_route('/graphql', GraphQLExecutor())
app.add_route('/', ApolloSandbox())

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    init_db()

    with make_server('', 8000, app) as httpd:
        logging.info('Serving on port http://localhost:8000 ...')

        # Serve until process is killed
        httpd.serve_forever()
