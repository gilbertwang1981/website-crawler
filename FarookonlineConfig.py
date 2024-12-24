import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('FarookonlineConfig.yaml', 'r') as file:
    farookonlineConfig = yaml.load(file)
