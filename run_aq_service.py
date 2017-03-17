

from bottle import route, run, template, default_app, request, response
import bottle
import json

from aquery_process import process_advanced_query

app = default_app()

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


@bottle.get('/')
def home():
    return '<strong>Hello from NDEx Advanced Query Service!</strong>'


# /search/network/{networkId}/query?size={limit}
@route('/search/network/<networkId>/query' , method=['OPTIONS','POST'] )
def get_advanced_query_request(networkId):
    size = request.query.get("size")
    request_json = json.load(request.body)
    #print(json.dumps(request_json, indent=3, sort_keys=True))

    process_advanced_query(networkId, size, request_json)

    return


app.install(EnableCors())
app.run(host='0.0.0.0', port=8072)