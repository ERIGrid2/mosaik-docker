import pathlib

from .check_sim_setup import check_sim_setup
from ..util.config_data import ConfigData


def configure_sim_setup( 
        setup_dir,
        docker_file,
        scenario_file,
        extra_files = [],
        extra_dirs = [],
        results = []
        ):
    '''
    Configure an existing simulation setup.

    :param setup_dir: directory of the simulation setup (string, default: '.')
    :param docker_file: name of the Dockerfile used for building the simulation orchestrator image (string)
    :param scenario_file: name of the mosaik scenario file (string)
    :param extra_files: additional files to be added to the simulation orchestrator image (list of strings)
    :param extra_dirs: additional directories to be added to the simulation orchestrator image (list of strings)
    :param results: list of paths of result files or folders, i.e., files or folders produced by the simulation that should be retrieved after the simulation has finished (list of strings)
    :return: on success, return absolute path to simulation setup config file (string)
    '''

    if not isinstance( setup_dir, str ):
        raise TypeError( 'Parameter \'setup_dir\' must be of type \'str\'' )

    if not isinstance( docker_file, str ):
        raise TypeError( 'Parameter \'docker_file\' must be of type \'str\'' )

    if not isinstance( scenario_file, str ):
        raise TypeError( 'Parameter \'scenario_file\' must be of type \'str\'' )

    if not isinstance( extra_files, list ) or not all( isinstance( elem, str ) for elem in extra_files ):
        raise TypeError( 'Parameter \'extra_files\' must be of type \'list of str\'' )

    if not isinstance( extra_dirs, list ) or not all( isinstance( elem, str ) for elem in extra_dirs ):
        raise TypeError( 'Parameter \'extra_dirs\' must be of type \'list of str\'' )

    if not isinstance( results, list ) or not all( isinstance( elem, str ) for elem in results ):
        raise TypeError( 'Parameter \'results\' must be of type \'list of str\'' )

    # Retrieve simulation setup configuration.
    config_data = ConfigData( setup_dir )

    config_data_orch = config_data['orchestrator']
    config_data_orch['docker_file'] = docker_file
    config_data_orch['scenario_file'] = scenario_file
    config_data_orch['extra_files'] = extra_files
    config_data_orch['extra_dirs'] = extra_dirs
    config_data_orch['results'] = results

    # Save simulation setup configuration.
    config_data.write()

    # Check if the new configuration is valid.
    check_setup = check_sim_setup( setup_dir )
    if not check_setup['valid']:
        raise RuntimeError( check_setup['status'] )

    # On success, return absolute path to simulation setup config file.
    return str( config_data.path )


def main():

    import argparse
    import sys

    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Configure an existing simulation setup.'
    )

    parser.add_argument(
        'setup_dir',
        nargs = '?',
        default = '.',
        metavar = 'SETUP_DIR',
        help = 'path to simulation setup directory (default: current working directory)'
    )

    required = parser.add_argument_group( 'required named arguments' )
    
    required.add_argument(
        '-d', '--docker-file', 
        action = 'store',
        required = True,
        metavar = 'DOCKER_FILE',
        help = 'name of Dockerfile for orchestrator'
    )

    required.add_argument(
        '-s', '--scenario-file', 
        action = 'store',
        required = True,
        metavar = 'SCENARIO_FILE',
        help = 'name of main mosaik script for orchestrator'
    )

    parser.add_argument(
        '--extra-file',
        default = [],
        action = 'append',
        metavar = 'EXTRA_FILE',
        help = 'additional file to be added to the orchestrator Docker image'
    )

    parser.add_argument(
        '--extra-dir', 
        default = [],
        action = 'append',
        metavar = 'EXTRA_DIR',
        help = 'additional directory to be added to the orchestrator Docker image'
    )

    parser.add_argument(
        '--result', 
        action = 'append',
        metavar = 'RESULT',
        help = 'paths of result file or folder, i.e., file or folder produced by the simulation that should be retrieved after the simulation has finished (list of strings)'
    )

    args = parser.parse_args()

    try:
    
        sim_config_file = configure_sim_setup( 
            args.setup_dir, 
            args.docker_file,
            args.scenario_file,
            args.extra_file,
            args.extra_dir,
            args.result
        )

        print( 'Updated simulation configuration file: {}'.format( sim_config_file ) )
        sys.exit( 0 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 3 )
