from .._config import DOCKER_HOST_DEFAULT

def get_default_docker_host():
    '''
    Return the URL to the default daemon socket to connect to when running docker.
    '''
    return DOCKER_HOST_DEFAULT
