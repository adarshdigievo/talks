#  Copyright © 2020 - 2022 Strollby, Inc or it's affiliates. All Rights Reserved.
#  Project : Strollby Experiences
#  Filename : apollo_studio_sandbox.py
#  Author : u220567
#  Current modification time : Wed, 20 Jul 2022 at 1:29 PM India Standard Time
#  Last modified time : Wed, 20 Jul 2022 at 1:29 PM India Standard Time
from falcon import HTTP_200, MEDIA_HTML, Request, Response


class ApolloSandbox:
    """ Apollo studio sandbox for Development use only.  """
    def on_get(self, _: Request, resp: Response) -> None:
        """Handles GET requests"""
        resp.status = HTTP_200
        resp.content_type = MEDIA_HTML
        resp.text = (
            '''
                <div id="sandbox" style="position:absolute;top:0;right:0;bottom:0;left:0"></div>
                <script
                 src="https://embeddable-sandbox.cdn.apollographql.com/_latest/embeddable-sandbox.umd.production.min.js">
                 </script>
                <script>
                 new window.EmbeddedSandbox({
                   target: "#sandbox",
                   // Pass through your server href if you are embedding on an endpoint.
                   // Otherwise, you can pass whatever endpoint you want Sandbox to start up with here.
                   initialEndpoint: window.location.origin + "/graphql",
                 });
                 // advanced options: https://www.apollographql.com/docs/studio/explorer/sandbox#embedding-sandbox
                </script>
            '''
        )
