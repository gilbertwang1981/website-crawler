import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('SmartberryConfig.yaml', 'r') as file:
    smartberryConfig = yaml.load(file)
