import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('FakhruddinsouqConfig.yaml', 'r') as file:
    fakConfig = yaml.load(file)
