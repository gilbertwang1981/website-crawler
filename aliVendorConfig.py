import ruamel.yaml


yaml = ruamel.yaml.YAML(typ='rt')

with open('aliVendor.yaml', 'r') as file:
    aliVendorConfig = yaml.load(file)
