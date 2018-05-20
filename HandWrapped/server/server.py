import requests
import http.server

class Server:
    def __init__(self, someApp, router=None):
        self.app = someApp
        self.router = router

    def spinUp(self, ip, port):
        self.server = http.server.HTTPServer((ip, port), self.router)
        self.server.handle_request()
        self.server.shutdown()
