# cdse_config.py

from sentinelhub import SHConfig

def get_config():
    config = SHConfig()
    config.sh_client_id = '' #replace with your own client id
    config.sh_client_secret = '' #replace with your own client secret
    config.sh_auth_base_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE'
    config.sh_token_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'
    config.sh_base_url = 'https://sh.dataspace.copernicus.eu'
    return config
