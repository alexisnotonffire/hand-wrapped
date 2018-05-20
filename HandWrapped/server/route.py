from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from ruamel.yaml import YAML

class Handler(BaseHTTPRequestHandler):
    def do_GET(req):
        request = urlparse(req.path)
        if request.path == '/spotify':
            token = parse_qs(request.query)['code']
            req.send_response(200)
            req.send_header('content-type', 'text/html')
            req.end_headers()
            req.wfile.write(b'handled')
            with open('./../config.yaml', 'r') as f:
                config = YAML().load(f)
                config['app']['spotify']['code'] = token

            with open('./../config.yaml', 'w') as f:
                YAML().dump(config, f)

        else:
            print(request.path)
            req.send_response(404)
            req.send_header('content-type', 'text/html')
            req.end_headers()
            req.wfile.write(b"this is not the page you're looking for")
