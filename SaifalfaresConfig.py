import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('SaifalfaresConfig.yaml', 'r') as file:
    saifalfaresConfig = yaml.load(file)
