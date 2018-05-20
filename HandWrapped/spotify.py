from datetime import datetime
from calendar import timegm
import json

from ruamel.yaml import YAML
import requests as r

def getUnixFrom(str):
    return timegm(datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%fZ').timetuple())


def getAfterValue(res):
    plays = (getUnixFrom(tracks['played_at']) for tracks in res['items'])
    return sorted(plays)[-1]


def updateAfter(configPath, after):
    with open(configPath, 'r+') as f:
        config = yaml.load(f)
        config['app']['spotify']['after'] = after
        YAML.dump(config, f)

def recentlyPlayed(access_token, after, limit):
    url = 'https://api.spotify.com/v1/me/player/recently-played'
    headers = {
        'authorization': 'Bearer ' + access_token,
        'accept': 'application/json'
    }
    params = {
        'limit': limit,
        'after': after
    }
    res = r.get(url=url, headers=headers, params=params)
    return json.loads(res.text) if res.status_code == 200 else None
