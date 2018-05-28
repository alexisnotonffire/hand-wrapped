import pytest
import os

# internal
import app
import spotify

#external
import yaml

@pytest.fixture
def testAppFixture():
    return app.App(
        {
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


@pytest.fixture
def testResponseFixture():
    return {
        'items': [
            { 'played_at':'2016-11-13T20:44:04.589Z' },
            { 'played_at':'2016-12-13T20:44:04.589Z' }
        ]
    }


class TestSpotify:

    def testSpotifyAfterValue(self, testResponseFixture):
        res = testResponseFixture
        assert spotify.getAfterValue(res) == 1481661844



    def testSpotifyAfterUpdate(self, tmpdir):
        tmpConf = tmpdir.mkdir('conf').join('config.yaml')
        with open(str(tmpConf), 'w') as f:
            yaml.dump({'app': {'spotify': {'after': 0}}}, f)
        spotify.updateAfter(str(tmpConf), 1)
        with open(str(tmpConf), 'r') as f:
            config = yaml.load(f)
        assert config['app']['spotify']['after'] == 1
