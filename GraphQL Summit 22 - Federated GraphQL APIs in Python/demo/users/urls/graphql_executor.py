import json
import logging

from falcon import Request, Response

from schema import schema


class GraphQLExecutor:
    @staticmethod
    def on_post(request: Request, response: Response) -> None:
        result = schema.execute(request.media['query'] if 'query' in request.media else None,
                                operation_name=request.media[
                                    'operationName'] if 'operationName' in request.media else None,
                                variables=request.media['variables'] if 'variables' in request.media else None)
        response.text = json.dumps(result.formatted)

        if result.errors:
            for e in result.errors:
                logging.error("", exc_info=e.original_error)