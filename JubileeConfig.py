import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('JubileeConfig.yaml', 'r') as file:
    jubileeConfig = yaml.load(file)
