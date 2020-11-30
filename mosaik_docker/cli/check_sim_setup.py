import pathlib

from ..util.config_data import ConfigData


def check_sim_setup( setup_dir ):
    '''
    Check if simulation setup is valid.

    :param setup_dir: path to simulation setup (string)
    :return: return dict with status of setup check in the following format:
        {
            'valid': boolean # flag indicating if setup is valid
            'status': string # detailed status message
        }
    '''
    setup_dir = pathlib.Path( setup_dir ).resolve( strict = True )

    # Retrieve simulation setup configuration.
    config_data = ConfigData( setup_dir )

    err = '"{}" is missing in configuration file'

    if not 'id' in config_data:
        return dict( valid = False, status = err.format( 'id' ) )
    elif not 'orchestrator' in config_data:
        return dict( valid = False, status = err.format( 'orchestrator' ) )
    elif not 'sim_ids_up' in config_data:
        return dict( valid = False, status = err.format( 'sim_ids_up' ) )
    elif not 'sim_ids_down' in config_data:
        return dict( valid = False, status = err.format( 'sim_ids_down' ) )

    config_data_orch = config_data['orchestrator']
    if not 'scenario_file' in config_data_orch:
        return dict( valid = False, status = err.format( 'orchestrator.scenario_file' ) )
    elif not 'docker_file' in config_data_orch:
        return dict( valid = False, status = err.format( 'orchestrator.docker_file' ) )
    elif not 'extra_files' in config_data_orch:
        return dict( valid = False, status = err.format( 'orchestrator.extra_files' ) )
    elif not 'extra_dirs' in config_data_orch:
        return dict( valid = False, status = err.format( 'orchestrator.extra_dirs' ) )
    elif not 'results' in config_data_orch:
        return dict( valid = False, status = err.format( 'orchestrator.results' ) )

    try:
        pathlib.Path( setup_dir, config_data_orch['scenario_file'] ).resolve( strict = True )
    except Exception as err:
        return dict( valid = False, status = 'scenario file missing\n{}'.format( err ) )
        
    try:
        pathlib.Path( setup_dir, config_data_orch['docker_file'] ).resolve( strict = True )
    except Exception as err:
        return dict( valid = False, status = 'Dockerfile missing\n{}'.format( err ) )

    try:
        for file in config_data_orch['extra_files']:
            if not pathlib.Path( setup_dir, file ).resolve( strict = True ).is_file():
                raise Exception( 'not a file: {}'.format( file ) )
    except Exception as err:
        return dict( valid = False, status = 'extra file not found\n{}'.format( err ) )

    try:
        for dir in config_data_orch['extra_dirs']:
            if not pathlib.Path( setup_dir, dir ).resolve( strict = True ).is_dir():
                raise Exception( 'not a directory: {}'.format( dir ) )
    except Exception as err:
        return dict( valid = False, status = 'extra directory not found\n{}'.format( err ) )

    return dict( valid = True, status = 'simulation setup is valid: {}'.format( setup_dir ) )


def main():

    import argparse
    import sys

    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Check if simulation setup is valid.'
    )

    parser.add_argument(
        'setup_dir',
        nargs = '?',
        default = '.',
        metavar = 'SETUP_DIR',
        help = 'path to simulation setup directory (default: current working directory)'
    )

    args = parser.parse_args()

    try:
        setup_status = check_sim_setup( args.setup_dir )

        print( setup_status['status'] )
        if True == setup_status['valid']:
            sys.exit( 0 )
        else:
            sys.exit( 1 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 3 )