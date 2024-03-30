import yaml

yaml_file_path = "scrapper.yaml"

with open(yaml_file_path, "r") as file:
    config = yaml.safe_load(file)

print(config)
