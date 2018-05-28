import pytest
from os import environ as env

# Internal
import app
import auth

##### Auth Flow #####
# read app config
#   -> create App object
#   -> create spotify auth endpoint
#   -> create spotify app code request body from App
#   -> transform app code response to auth request
#   -> transform auth response into Auth object
#       -> add Auth to App

@pytest.fixture
def testAppFixture():
    return app.App(
        {
            'name': 'lovingly-tested',
            'author': 'testor',
            'description': 'carefully described or something',
            'alert': None
            'spotify': {
                'redirect_uri': 'http://localhost',
                'client_id': 'test_id',
                'client_secret': 'test_secret',
                'scope': [
                    'test-shit',
                    'test-shitter',
                    'test-shittest'
                ],
                'after': 0
            },
            'google': {
                'token': 'boop',
                'project': 'testing-world',
                'dataset': 'TestingData',
                'table': 'Testback'
            }
        }
    )

@pytest.fixture
def AppWithSpotifyAuth(testAppFixture):
    testAppFixture.spotify.update(
        {
            'client': 'id:secret',
            'grant_type': 'authorization_code',
            'code': '0',
            'redirect_uri': 'http://localhost',
            'access_token': '1',
            'refresh_token': '2'
        }
    )
    return testAppFixture

# Apps have an 'authAgainst' method to add a named Auth object to App['name']
class TestApp():
    @pytest.mark.parametrize("config", [0,[0],'0',None,{'bad': 'name'}])
    def testApp(self, config):
        with pytest.raises(TypeError):
            testApp = app.App(config)

    @pytest.mark.parametrize("name,auth,exp", [
        ('spotify', {
                        'client': 'id:secret',
                        'grant_type': 'authorization_code',
                        'code': '0',
                        'redirect_uri': 'http://localhost',
                        'access_token': '1',
                        'refresh_token': '2',
                        'after': 0
                    },
                    {
                        'redirect_uri': 'http://localhost',
                        'client_id': 'test_id',
                        'client_secret': 'test_secret',
                        'client': 'id:secret',
                        'grant_type': 'authorization_code',
                        'code': '0',
                        'access_token': '1',
                        'refresh_token': '2',
                        'scope': [
                            'test-shit',
                            'test-shitter',
                            'test-shittest'
                        ],
                        'after': 0
                    })
    ])
    def testAuthAgainstApp(self, name, auth, exp, testAppFixture):
        testApp = testAppFixture
        app.App.authAgainst(testApp, name, auth)
        assert testApp.__getattribute__(name) == exp

    def testInvalidAuthAgainstApp(self):
        testApp = testAppFixture
        with pytest.raises(TypeError) as error:
            app.App.authAgainst(testApp, 'name', {'not': 'valid'})


# Auth object must match a named list
class TestAuth(object):

    @pytest.mark.parametrize("input", [0,[0],'0',None,{'bad': 'name'}])
    def testAuthInitFail(self, input):
        with pytest.raises(TypeError):
            newAuth = auth.Auth(input)


# From App, we should be able to create the correct auth endpoints as well as
# the corresponding request bodies. We will not test the responses.
class TestSpotifyAuth():

    def testBuildSpotifyAuthRequest(self, testAppFixture):
        testApp = testAppFixture
        spotifyAuthRequest = auth.buildSpotifyAuthRequest(testApp, '0')
        assert spotifyAuthRequest == {
            'headers': {
                'Authorisation': 'Basic test_id:test_secret',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            'params': {
                'redirect_uri': 'http://localhost',
                'grant_type': 'authorization_code',
                'code': '0'
            }
        }

    def testBuildSpotifyAuthRefreshRequest(self, AppWithSpotifyAuth):

        testApp = AppWithSpotifyAuth
        spotifyAuthRefreshRequest = auth.buildSpotifyAuthRefreshRequest(testApp)
        assert spotifyAuthRefreshRequest == {
            'headers': {
                'Authorization': 'Basic id:secret',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            'params': {
                'grant_type': 'refresh_token',
                'refresh_token': '2'
            }
        }

    def testSpotifyRefresh(self, AppWithSpotifyAuth):
        testApp = AppWithSpotifyAuth
        update = {
            'token_type': 'Bearer',
            'scope': '',
            'expires_in': '3600',
            'access_token': 'newToken',
            'refresh_token': 'newRefresh'
        }
        auth.spotifyRefresh(testApp, update)
        assert testApp.spotify['access_token'] == 'newToken' \
               and testApp.spotify['refresh_token'] == 'newRefresh'

# Ensure env. is configured for GCP
class TestGoogleAuth:

    # TODO: Test correct roles
    def testGCPCreds(self):
        assert env['GOOGLE_APPLICATION_CREDENTIALS'] != None

    def testGCPProject(self):
        assert env['GoOGLE_CLOUD_PROJECT'] != None
