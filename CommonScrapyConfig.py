import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('CommonScrapyConfig.yaml', 'r') as file:
    commonScrapyConfig = yaml.load(file)
