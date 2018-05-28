from ruamel.yaml import YAML

class App:
    def __init__(self, config):
        try:
            self.name = config['app']['name']
            self.author = config['app']['author']
            self.description = config['app']['description']
            self.alert = config['app']['alert']
            self.spotify = config['app']['spotify']
            self.google = config['app']['google']
        except (TypeError, KeyError):
            raise TypeError("invalid config")

    def authAgainst(self, name, auth):
        if name not in ('spotify', 'google'):
            raise TypeError("invalid auth type")
        else:
            self.__getattribute__(name).update(auth)


def createConfigFrom(filepath):
    with open(filepath, 'r') as f:
        return YAML().load(f)
