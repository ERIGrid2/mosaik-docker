from ..util.config_data import ConfigData
from ..util.execute import execute


def clear_sim( setup_dir, id ):
    '''
    Delete containers of finished simulations.

    :param setup_dir: path to simulation setup (string)
    :param id: either 'all' or ID of simulation container to be cleared (string)
    :return: on success, return list of cleared simulation IDs (list of string)
    '''

    if not isinstance( id, str ):
        raise TypeError( 'Parameter \'id\' must be of type \'str\'' )

    # Retrieve simulation setup configuration.
    config_data = ConfigData( setup_dir )
    sim_ids_down = config_data['sim_ids_down']

    if 'all' == id.lower():
        rm_ids = list( sim_ids_down )
    else:
        rm_ids = [ id ]
        if id not in sim_ids_down:
            raise RuntimeError( 'No finished simulation (status \'DOWN\') with ID \'{}\''.format( id ) )

    if 0 != len( rm_ids ):
        execute( [
            'docker', 'rm', # Remove container.
            '--volumes', # Remove anonymous volumes associated with the container.
            *rm_ids # Simulation ID (Docker container name).
        ] )

    if 'all' == id.lower():
        sim_ids_down.clear()
    else:
        del sim_ids_down[ sim_ids_down.index( *rm_ids ) ]

    # Save simulation setup configuration.
    config_data.write()

    # On success, return cleared simulation ID.
    return rm_ids


def main():

    import argparse
    import sys

    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Delete containers of finished simulations.'
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
        help = 'remove all simulation containers'
    )

    args = parser.parse_args()

    try:
        id = 'all' if ( True == args.all ) else args.id
        sim_ids = clear_sim( args.setup_dir, id )

        print( 'Cleared simulation(s) with ID = {}'.format( ' '.join( sim_ids ) ) )
        sys.exit( 0 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 3 )
