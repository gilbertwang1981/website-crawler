import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('PlatoledConfig.yaml', 'r') as file:
    platoledConfig = yaml.load(file)
