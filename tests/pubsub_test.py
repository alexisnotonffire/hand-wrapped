import pytest
import pubsub

@pytest.fixture
def testItemList():
    return {
      "items": [
        {
          "track": {
            "artists": [
              {
                "external_urls": {
                  "spotify": "https://open.spotify.com/artist/5INjqkS1o8h1imAzPqGZBb"
                },
                "href": "https://api.spotify.com/v1/artists/5INjqkS1o8h1imAzPqGZBb",
                "id": "5INjqkS1o8h1imAzPqGZBb",
                "name": "Tame Impala",
                "type": "artist",
                "uri": "spotify:artist:5INjqkS1o8h1imAzPqGZBb"
              }
            ],
            "available_markets": [
              "CA",
              "MX",
              "US"
            ],
            "disc_number": 1,
            "duration_ms": 108546,
            "explicit": false,
            "external_urls": {
              "spotify": "https://open.spotify.com/track/2gNfxysfBRfl9Lvi9T3v6R"
            },
            "href": "https://api.spotify.com/v1/tracks/2gNfxysfBRfl9Lvi9T3v6R",
            "id": "2gNfxysfBRfl9Lvi9T3v6R",
            "name": "Disciples",
            "preview_url": "https://p.scdn.co/mp3-preview/6023e5aac2123d098ce490488966b28838b14fa2",
            "track_number": 9,
            "type": "track",
            "uri": "spotify:track:2gNfxysfBRfl9Lvi9T3v6R"
          },
          "played_at": "2016-12-13T20:44:04.589Z",
          "context": {
            "uri": "spotify:artist:5INjqkS1o8h1imAzPqGZBb",
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5INjqkS1o8h1imAzPqGZBb"
            },
            "href": "https://api.spotify.com/v1/artists/5INjqkS1o8h1imAzPqGZBb",
            "type": "artist"
          },
        },
        {
          "track": {
            "artists": [
              {
                "external_urls": {
                  "spotify": "https://open.spotify.com/artist/5INjqkS1o8h1imAzPqGZBb"
                },
                "href": "https://api.spotify.com/v1/artists/5INjqkS1o8h1imAzPqGZBb",
                "id": "5INjqkS1o8h1imAzPqGZBb",
                "name": "Tame Impala",
                "type": "artist",
                "uri": "spotify:artist:5INjqkS1o8h1imAzPqGZBb"
              }
            ],
            "available_markets": [
              "CA",
              "MX",
              "US"
            ],
            "disc_number": 1,
            "duration_ms": 467586,
            "explicit": false,
            "external_urls": {
              "spotify": "https://open.spotify.com/track/2X485T9Z5Ly0xyaghN73ed"
            },
            "href": "https://api.spotify.com/v1/tracks/2X485T9Z5Ly0xyaghN73ed",
            "id": "2X485T9Z5Ly0xyaghN73ed",
            "name": "Let It Happen",
            "preview_url": "https://p.scdn.co/mp3-preview/05dee1ad0d2a6fa4ad07fbd24ae49d58468e8194",
            "track_number": 1,
            "type": "track",
            "uri": "spotify:track:2X485T9Z5Ly0xyaghN73ed"
          },
          "played_at": "2016-12-13T20:42:17.016Z",
          "context": {
            "uri": "spotify:artist:5INjqkS1o8h1imAzPqGZBb",
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/5INjqkS1o8h1imAzPqGZBb"
            },
            "href": "https://api.spotify.com/v1/artists/5INjqkS1o8h1imAzPqGZBb",
            "type": "artist"
          },
        }
      ],
      "next": "https://api.spotify.com/v1/me/player/recently-played?before=1481661737016&limit=2",
      "cursors": {
        "after": "1481661844589",
        "before": "1481661737016"
      },
      "limit": 2,
      "href": "https://api.spotify.com/v1/me/player/recently-played?limit=2"
    }

# TODO: 
# @pytest.fixture
# def messageTestFixture(message):
#     class Message(String):
#         def __init__(self, message):
#             self.text = message
#
#         def ack(self):
#             return 1
#
#         def nack(self):
#             return 0

class testPubSub(object):

    def testSchemaForce(self, testItemList):
        assert schemaForce(testItemList) == [
            {
                'Timestamp': "2016-12-13T20:44:04.589Z",
                'Id': "2gNfxysfBRfl9Lvi9T3v6R",
                'Name': "Disciples",
                'Duration': 108546,
                'Context': "artist",
                'Artist': {
                    'Id': "5INjqkS1o8h1imAzPqGZBb",
                    'Name': "Tame Impala",
                    'Genres': [

                    ],
                    'HRef': "https://api.spotify.com/v1/artists/5INjqkS1o8h1imAzPqGZBb"
                },
                'Album': {},
                'HRef': "https://api.spotify.com/v1/tracks/2gNfxysfBRfl9Lvi9T3v6R"
            },
            {
                'Timestamp': "2016-12-13T20:42:17.016Z",
                'Id': "2X485T9Z5Ly0xyaghN73ed",
                'Name': "Let It Happen",
                'Duration': 467586,
                'Context': "artist",
                'Artist': {
                    'Id': "5INjqkS1o8h1imAzPqGZBb",
                    'Name': "Tame Impala",
                    'Genres': [

                    ],
                    'HRef': "https://api.spotify.com/v1/artists/5INjqkS1o8h1imAzPqGZBb"
                },
                'Album': {},
                'HRef': "https://api.spotify.com/v1/tracks/2X485T9Z5Ly0xyaghN73ed"
            }
        ]

    def testIncorrectSchemaForce(self):
        with pytest.raises(SchemaError):
            schemaForce({'Name': 'Nuh-uh'})
