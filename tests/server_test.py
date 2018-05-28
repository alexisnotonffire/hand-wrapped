import pytest
import server.server as server
import app

config = {
    'name': 'lovingly-tested',
    'author': 'testor',
    'description': 'carefully described or something',
    'spotify': {
        'redirect_uri': 'http://localhost',
        'client_id': 'test_id',
        'client_secret': 'test_secret',
        'scope': [
            'test-shit',
            'test-shitter',
            'test-shittest'
        ]
    }
}

@pytest.fixture
def testAppFixture(config):
    import app
    return app.App(config)


@pytest.fixture
def testServerFixture(testApp):
    import app
    import server.server as server
    import server.route as route
    import multiprocessing as mp

    return server.Server(testApp, route.Handler)


class TestServer:

    def testServerInit(self, testApp=testAppFixture):
        testServer = server.Server(testApp)
        assert testServer.app == testApp

    @pytest.mark.skip
    def testSpinUp(self, testServer=testServerFixture, testApp=testAppFixture):
        assert testServer(testApp).spinUp(6868)
