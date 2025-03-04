import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('TiktokSamplingConfig.yaml', 'r') as file:
    tiktokSamplingConfig = yaml.load(file)
