import yaml

def load_config(config_path: str = "config/config.yaml") -> dict:
    """
    Load model, configuration from ../config/config.yaml
    """
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config

load_config()