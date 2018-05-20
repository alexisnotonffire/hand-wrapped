import app
import auth
import pubsub
import spotify
import bigquery
import server.route as route
import server.server as server

import time
import json
import webbrowser
from multiprocessing import Process as mp

import requests as r
from ruamel.yaml import YAML

if __name__ == '__main__':
    configLocation = './../config.yaml'
    config = app.createConfigFrom(configLocation)

    # If there isn't a code, we must get one
    if config['app']['spotify']['code'] == None:
        handWrapped = app.App(config)
        srv = mp(
            target=server.Server(handWrapped, route.Handler).spinUp,
            args=('localhost', 9898,)
            )
        srv.start()
        print("server running")
        webbrowser.open(auth.buildSpotifyInitialAuthRequest(handWrapped), new=2)

    # Wait until the code has been stored in the config
    # FIXME: currently storage of code isn't automatic
    while config['app']['spotify']['code'] == None:
        suspense = 1
        print('waiting' + '.'*suspense%3, flush=True)
        suspense +=1
        config = app.createConfigFrom(configLocation)
        sleep(0.5)

    url = 'https://accounts.spotify.com/api/token'
    if config['app']['spotify'].get('refresh_token') == None:
        print('asking nicely for some tokens')
        config = app.createConfigFrom(configLocation)
        handWrapped = app.App(config)
        access_token = config['app']['spotify']['code']
        req, client = auth.buildSpotifyAuthRequest(handWrapped, access_token)
        tokens = r.post(url=url, headers=req['headers'], data=req['params'])
        if tokens.status_code == 200:
            print('initial tokens received')
            tokens = json.loads(tokens.text)
            with open(configLocation, 'w') as f:
                config['app']['spotify']['client'] = client
                config['app']['spotify'].update(tokens)
                YAML().dump(config, f)

            print('initial tokens loaded')
        else:
            print('these tokens aint shit')
            print(json.loads(tokens.text))
            raise TypeError
            exit()
    else:
        print('updating the tokens')
        handWrapped = app.App(config)
        req = auth.buildSpotifyAuthRefreshRequest(handWrapped)
        tokens = r.post(url=url, headers=req['headers'], data=req['params'])
        if tokens.status_code == 200:
            print('tokens received')
            tokens = json.loads(tokens.text)
            with open(configLocation, 'w') as f:
                config['app']['spotify'].update(tokens)
                YAML().dump(config, f)
            print('tokens loaded')


    print('asking nicely for my history')
    tracks = spotify.recentlyPlayed(
        config['app']['spotify']['access_token'],
        config['app']['spotify']['after'],
        50
    )['items']
    status = bool(tracks)
    print('tracks received!') if status else print('something fucked up')

    messageList = pubsub.schemaForce(tracks)
    print('prepped for pubsub')
    pubsub.pubMessage(messageList, 'spotify-playback')
    waitfor = pubsub.subMessage('playback')

    # TODO: Forgive me father for I have sinned.
    time.sleep(15)


    # loadJob = bigquery.BigQueryLoader(
    #             'EU', 'handWrappedDev', 'Playback', './tempStore.json'
    # )
    # loadJob.run()
