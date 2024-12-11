import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('aliImageSearch.yaml', 'r') as file:
    aliImageSearchConfig = yaml.load(file)

