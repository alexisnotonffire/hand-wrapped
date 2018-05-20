import base64
import requests as req

class Auth:
    def __init__(self, auth):
        try:
            self.__dict__ = auth
        except (KeyError):
            raise TypeError

def buildSpotifyInitialAuthRequest(app):
    params = {
        'client_id': app.spotify['client_id'],
        'response_type': 'code',
        'redirect_uri': app.spotify['redirect_uri'],
        'scope': app.spotify['scope'],
        'show_dialog': False
        }
    r = req.Request(
        'GET',
        'https://accounts.spotify.com/authorize/?',
        params=params
        ).prepare()
    return r.url

def buildSpotifyAuthRequest(app, access_token):
    req = {}
    rawClient = app.spotify['client_id'] + ':' + app.spotify['client_secret']

    client = base64.b64encode(
            rawClient.encode('utf-8')
        ).decode('utf-8')

    req['headers'] = {
        'Authorization': 'Basic ' + client,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    req['params'] = {
        'redirect_uri': app.spotify['redirect_uri'],
        'grant_type': 'authorization_code',
        'code': access_token
    }
    return req, client

def buildSpotifyAuthRefreshRequest(app):
    req = {}
    req['headers'] = {
        'Authorization': 'Basic ' + app.spotify['client'],
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    req['params'] = {
        'grant_type': 'refresh_token',
        'refresh_token': app.spotify['refresh_token']
    }
    return req

def spotifyRefresh(app, update):
    if set(update) != set([
        'token_type', 'scope', 'expires_in', 'access_token', 'refresh_token'
    ]):
        raise TypeError("update response does not match API docs")
    app.spotify.update(update)
