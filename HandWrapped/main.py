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
import google.api_core.exceptions as e
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
    print('waiting for code ...')
    while config['app']['spotify']['code'] == None:
        config = app.createConfigFrom(configLocation)
        sleep(1)

    # Get the initial set of tokens for authorisation if None exist
    # Otherwise refresh tokens every time
    url = 'https://accounts.spotify.com/api/token'
    if config['app']['spotify'].get('refresh_token') == None:
        print('asking nicely for some tokens')

        config = app.createConfigFrom(configLocation)
        handWrapped = app.App(config)
        access_token = config['app']['spotify']['code']

        # Ask for tokens. Send alert if anything other than 200 response
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

            r.get(url=config['app']['alert'])
            print('sent failure alert')
            exit()

    else:

        # Ask for tokens. Send alert if anything other than 200 response
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
        else:
            r.get(url=config['app']['alert'])
            print('sent failure alert')

    # Fetch tracks
    print('asking nicely for my history')
    tracks = spotify.recentlyPlayed(
        config['app']['spotify']['access_token'],
        config['app']['spotify']['after'],
        50
    )['items']
    status = bool(tracks)
    notracks = len(tracks)
    if status:
        print(f'{len(tracks)} new tracks received!')
        after = spotify.getAfterValue(tracks)
    elif tracks != None:
        print('nothing new found')
        exit()
    else:
        print('something fucked up')
        r.get(url=config['app']['alert'])
        print('sent failure alert')
        exit()

    # Publish tracks
    if len(tracks) > 0:
        messageList = pubsub.schemaForce(tracks)
        print('prepped for pubsub')
        pubsub.pubMessage(messageList, 'spotify-playback')
        waitfor = pubsub.subMessage('playback')

        # TODO: Forgive me father for I have sinned.
        # Would be top stuff if future.result() worked but it does not.
        time.sleep(15)
        with open('./tempStore.json', 'w') as f:
            for message in pubsub.messages:
                f.write(
                    json.dumps(json.loads(message)) + '\n'
                )

        loadJob = bigquery.BigQueryLoader(
                    'EU', 'handWrappedDev', 'Playback', './tempStore.json'
        )
        loadJob.configureJob()
        print('running the load job')
        try:
            loadJob.run()
            print('data uploaded successfully')
            print('job done, starting cleanup')
            spotify.updateAfter(configLocation, after)
        except e.BadRequest as err:
            r.get(url=config['app']['alert'])
            print(f'sent failure alert: {err}')
            exit()

    print('finished')
