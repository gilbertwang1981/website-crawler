import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('SalmansaffronConfig.yaml', 'r') as file:
    salmansaffronConfig = yaml.load(file)
