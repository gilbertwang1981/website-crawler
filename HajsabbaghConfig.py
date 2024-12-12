import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('HajsabbaghConfig.yaml', 'r') as file:
    hajsabbaghConfig = yaml.load(file)
