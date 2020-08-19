import pathlib

from ..util.config_data import ConfigData
from ..util.execute import execute, execute_and_capture_output


def get_sim_results( setup_dir, id, overwrite = False ):
    '''
    Retrieve the results of finished simulations.

    :param setup_dir: path to simulation setup (string)
    :param id: either 'all' or ID of finished simulation container (string)
    :param overwrite: overwrite previously retrieved results (boolean, default: False)
    :return: on success, return ID(s) of simulation(s) for which results have been retrieved (string)
    '''

    if not isinstance( overwrite, bool ):
        raise TypeError( 'Parameter \'overwrite\' must be of type \'bool\'' )
        
    # Retrieve simulation setup configuration.
    config_data = ConfigData( setup_dir )
    sim_ids_down = config_data['sim_ids_down']
    config_data_orch = config_data['orchestrator']
    results = config_data_orch['results']

    if 'all' == id.lower():
        cp_ids = sim_ids_down
    else:
        cp_ids = [ id ]
        if id not in sim_ids_down:
            raise RuntimeError( 'No finished simulation (status \'DOWN\') with ID \'{}\''.format( id ) )


    for cp_id in cp_ids:
    
        # Retrieve working directory of Docker container.
        sim_working_dir = execute_and_capture_output( [
            'docker', 'inspect', # Return low-level information on Docker objects.
            '--format={{.Config.WorkingDir}}', # Only return the container's working directory.
            cp_id # Specify simulation ID (container name).
        ] )
    
        # Create local results folder, where all results are copied to.
        results_dir_path = pathlib.Path( setup_dir, cp_id ).resolve( strict = False )
        try:
            results_dir_path.mkdir( exist_ok = False )
        except FileExistsError:
            if ( False == overwrite ):
                raise RuntimeWarning( 'Results directory already exists: {}'.format( results_dir_path ) )
    
        # Copy each result file or folder from the container to the local results folder.
        for res in results:
            if pathlib.Path( res ).is_absolute():
                res_path = '{}:{}'.format( cp_id, res )
            else:
                res_path = '{}:{}/{}'.format( cp_id, sim_working_dir, res )
    
            execute( [
                'docker', 'cp', # Copy files/folders between a container and the local filesystem.
                res_path, # Specify container name (simulation ID) and file/folder to be copied.
                str( results_dir_path ) # Specify destination folder.
                ] )

    # On success, return the simulation ID(s).
    return cp_ids


def main():

    import argparse
    import sys

    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Retrieve the results of finished simulations.'
    )

    parser.add_argument(
        'setup_dir',
        nargs = '?',
        default = '.',
        metavar = 'SETUP_DIR',
        help = 'path to simulation setup directory (default: current working directory)'
    )

    group = parser.add_mutually_exclusive_group( required = True )

    group.add_argument(
        '--id', 
        action = 'store',
        metavar = 'ID',
        help = 'simulation ID (Docker container name)'
    )

    group.add_argument(
        '--all',
        action = 'store_true',
        help = 'retrieve results from all finished simulation containers'
    )

    parser.add_argument(
        '--overwrite',
        action = 'store_true',
        help = 'overwrite previously retrieved results'
    )

    args = parser.parse_args()

    try:
        id = 'all' if ( True == args.all ) else args.id
        sim_ids = get_sim_results( args.setup_dir, id, args.overwrite )

        print( 'Retrieved results for simulation(s) with ID = {}'.format( ' '.join( sim_ids ) ) )
        sys.exit( 0 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 3 )
