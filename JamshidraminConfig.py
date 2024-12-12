import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('JamshidraminConfig.yaml', 'r') as file:
    jamshidraminConfig = yaml.load(file)
