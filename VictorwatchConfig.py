import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('VictorwatchConfig.yaml', 'r') as file:
    victorwatchConfig = yaml.load(file)
