import yaml

# add error checking; where passes are located

# temporary placement to test
CONFIGS = open_yaml_file('conf.yaml')
GOOGLE_CONFIGS = get_google_configs(CONFIGS)

def open_yaml_file(file):
    """
    Opens up the yaml file for parsing

    :file: file name to the yaml file
        :type: str

    :return: dictionary form of the yaml config
        :type: dict
    """
    try:
        with open(file) as f:
            return yaml.full_load(f)
    except yaml.YAMLError:
        pass
        
def get_google_configs(config):
    """
    Retrieves the google configs

    :config: configurations
        :type: dict

    :return: google configs
        :type: dict
    """
    if 'googleConfigs' in config: 
        return config.get('googleConfigs')
    else: 
        pass
    

def get_api_key(config):
    """
    Retrieves api key from the configurations

    :config: configurations
        :type: dict

    :return: api key
        :type: str
    """
    if 'apiKey' in config: 
        return config.get('apiKey')
    else: 
        pass

def get_api_url(config):
    """
    Retrieves url from the configurations

    :config: configurations
        :type: dict
    
    :return: url
        :type: str
    """
    if 'url' in config: 
        return config.get('url')
    else: 
        pass
    
def get_api_path(config, path):
    """
    Retrieve path to api call

    :config: configurations
        :type: dict

    :path: path name
        :type: str

    :return: path
        :type: str
    """
    if path in config:
        return config.get(path)
    else:
        pass
