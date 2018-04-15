import pytest

config = {
    'redirect_uri': 'http://localhost',
    'client_id': 'test_id',
    'client_secret': 'test_secret',
    'scope': [
        'test-shit',
        'test-shitter',
        'test-shittest'
    ]
}

class testApp():

    app = App(config)
    def testAuthAgainst():
        app.authAgainst('name', 'url', {'auth': {'token': 123, 'refresh': 123}})
        assert app.allowedAt['name'] == {
            'authURL': 'url','auth': {'token': 123, 'refresh': 123}
        }


class testAuth(object):

    app = App(config)
    def testAuthInit():
        with TypeError:
            Auth({'not': 'an app'})

    # def testGoogleInitialURL():
    #     assert buildGoogleInitialURL() ==


class testSpotifyAuth(object):

    app = App(config)
    def testBuildSpotifyInitialURL():
        assert app.buildSpotifyInitialURL() == 'http://localhost/authorize?response_type=code&redirect_uri=http%3A%2F%2Flocalhost&scope=test-shit%20test-shitter%20test-shittest'

    def testSpotifyRefresh():
        update = {
            'access_token': 'newToken',
            'token_type': 'Bearer',
            'scope': '',
            'expires_in': '3600',
            'refresh_token': 'newRefresh'
        }
        spotifyRefresh(app, update)
        assert app.allowedAt['spotify']['refresh_token'] == 'newRefresh'

    def testGoodRequest(object):
        spotifyAuth(object)

    def testNoConnection():
        auth = Auth('http://there.is.no/connection?here=ever', app)
        with pytest.raises(ConnectionError) as noConnection:
            spotifyAuth()
        assert noConnection.message == 'no response from server'

    def testBadRequest():
        with pytest.raises(HttpException) as badRequest:
            spotifyAuth({ })
        assert badRequest.message == 'bad request'

# TODO: write google auth tests
# class testGoogleAuth(object):
#
#     def testGoodRequest():
#         assert False
#
#     def testTokenRefresh():
#         assert False
#
#     def testNoConnection():
#         assert False
#
#     def testBadRequest():
#         assert False
#
