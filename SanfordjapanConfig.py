import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('SanfordjapanConfig.yaml', 'r') as file:
    sanfordjapanConfig = yaml.load(file)
