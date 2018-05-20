import json
import os
from google.cloud import pubsub

def storeMessages(message):
    print(message.data)
    with open('./tempStore.json', 'a') as f:
        f.write(json.dumps(message.data.decode('utf-8'), ensure_ascii=False) + '\n')

    message.ack()


def pubMessage(messages, topic):
    publisher = pubsub.PublisherClient()
    topic = 'projects/{}/topics/{}'\
                .format(os.getenv('GOOGLE_CLOUD_PROJECT'), topic)

    for message in messages:
        publisher.publish(topic,
            json.dumps(message, ensure_ascii=False).encode('utf-8')
        )


def subMessage(sub):
    subscrip = pubsub.SubscriberClient()
    sub = 'projects/{}/subscriptions/{}'\
                .format(os.getenv('GOOGLE_CLOUD_PROJECT'), sub)
    policy = subscrip.subscribe(sub, storeMessages)
    return policy



def schemaForce(tracks):
    try:
        schema = [
            {
                'Timestamp': item['played_at'],
                'Id': item['track']['id'],
                'Name': item['track']['name'],
                'Duration': item['track']['duration_ms'],
                'Context': item['context']['type'] if item['context'] else None,
                'Artist': [
                    {
                        'Id': artist['id'],
                        'Name': artist['name'],
                        'Genres': [],
                        'HRef': artist['href']
                    }
                    for artist in item['track']['artists']
                ],
                'Album': {
                    'Id': item['track']['album']['id'],
                    'Name': item['track']['album']['name'],
                    'Type': item['track']['album']['album_type'],
                    'Label': None,
                    'Genres': [],
                    'HRef': item['track']['album']['href']
                },
                'HRef': item['track']['href']
            }
            for item in tracks
        ]
        return schema
    except (KeyError, TypeError, AttributeError):
        raise TypeError("schema is borked")


# Ideal object
# {
#     'Timestamp': track['played_at'],
#     'Id': track['id'],
#     'Name': track['name'],
#     'Duration': track['duration'],
#     'Context': track['context']['type'],
#     'Artist': {
#         'Id': track['artists']['id'],
#         'Name': track['artists']['name'],
#         'Genres': [
#
#         ],
#         'HRef': track['href']
#     },
#     'Album': {
#         'Id': track['album']['id'],
#         'Name': track['album']['id'],
#         'Type': track['album']['id'],
#         'Label': track['album']['id'],
#         'Genres': [
#
#         ],
#         'Artists': [
#             {
#                 'Id': artist['id'],
#                 'Name': artist['name'],
#                 'Genres': [
#
#                 ],
#                 'HRef': artist['href']
#             }
#             for artist in album['artists']
#         ],
#         'HRef': album['href']
#     },
#     'HRef': item['href']
# }
