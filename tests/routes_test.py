import pytest
from io import BytesIO as io
import http.client as client
import http.server as server

# Internal
import app
from server.route import Handler

# External
import requests

@pytest.fixture
def goodReq():
    req = """GET /spotify?code=test_token HTTP/1.1
        Host: localhost:9898
        Accept: application/json

        """
    return req

@pytest.fixture
def badReq():
    return \
    """GET /literally-anything?code=test_token HTTP/1.1
    Host: localhost:9898
    Accept: application/json


    """

# TODO: make this shit work
@pytest.mark.skip
class TestRoutes(object):
    def testRedirect(self, goodReq):
        r = Handler.do_GET(goodReq)
        assert r.status_code == 200

    def test404(self, badReq):
        r = Handler.do_GET(badReq)
        assert r.status_code == 404
