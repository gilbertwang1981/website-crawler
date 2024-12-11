import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('aliWangWang.yaml', 'r') as file:
    aliWangWangConfig = yaml.load(file)
