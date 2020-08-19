from .._config import ORCH_IMAGE_NAME_TEMPLATE
from ..util.config_data import ConfigData
from ..util.create_unique_id import create_unique_id
from ..util.execute import execute


def start_sim( setup_dir, id = None ):
    '''
    Start a new simulation.

    :param setup_dir: path to simulation setup (string)
    :param id: ID of new simulation (string, default: None)
    :return: on success, return new simulation ID (int)
    '''

    if not id == None and not isinstance( id, str ):
        raise TypeError( 'Parameter \'id\' must be of type \'str\'' )

    if id == None:
        id = create_unique_id()

    # Retrieve simulation setup configuration.
    config_data = ConfigData( setup_dir )

    sim_setup_id = config_data['id'].strip()
    config_data_orch = config_data['orchestrator']
    scenario_file = config_data_orch['scenario_file'].strip()

    sim_ids_up = config_data['sim_ids_up']
    sim_ids_down = config_data['sim_ids_down']

    if id in sim_ids_up or id in sim_ids_down:
        raise RuntimeError( 'Simulation ID \'{}\' has already been used'.format( id ) )

    # Define Docker image name.
    docker_image_name = ORCH_IMAGE_NAME_TEMPLATE.format( sim_setup_id.lower() )

    execute( [
        'docker', 'run', # Docker run command.
        '--detach', # Run container in background.
        #'--rm', # '-it', # Only for debugging.
        '--name', id, # Specify container name as simulation id.
        '--env', 'SCENARIO_FILE={}'.format( scenario_file ), # Specify scenario file.
        docker_image_name # Specify the Docker image.
    ] )

    # Update sim setup config.
    sim_ids_up.append( id )

    # Save simulation setup configuration.
    config_data.write()

    # On success, return new simulation ID.
    return id


def main():

    import argparse
    import sys

    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Start a new simulation.'
    )

    parser.add_argument(
        'setup_dir',
        nargs = '?',
        default = '.',
        metavar = 'SETUP_DIR',
        help = 'path to simulation setup directory (default: current working directory)'
    )

    parser.add_argument(
        'id',
        nargs = '?',
        default = None,
        metavar = 'ID',
        help = 'simulation ID (Docker container name)'
    )

    args = parser.parse_args()

    try:
        sim_id = start_sim( args.setup_dir, args.id )

        print( 'Started new simulation with ID = {}'.format( sim_id ) )
        sys.exit( 0 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 3 )
