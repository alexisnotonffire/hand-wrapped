from ruamel.yaml import YAML

with open('./../config.yaml') as f:
    config = YAML().load(f)

config['app']['spotify']['code'] = 'test123'
with open('./../config.yaml', 'w') as f:
    YAML().dump(config, f)
