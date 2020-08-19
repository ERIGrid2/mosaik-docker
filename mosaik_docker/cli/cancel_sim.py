from .._config import DOCKER_STOP_WAIT_TIME
from ..util.config_data import ConfigData
from ..util.execute import execute


def cancel_sim( setup_dir, id ):
    '''
    Cancel a simulation (stop simulation container).

    :param setup_dir: path to simulation setup (string)
    :param id: either 'all' or ID of running simulation container (string)
    :return: on success, return ID of cancelled simulation (int)
    '''

    if not id == None and not isinstance( id, str ):
        raise TypeError( 'Parameter \'id\' must be of type \'str\'' )

    # Retrieve simulation setup configuration.
    config_data = ConfigData( setup_dir )

    sim_ids_up = config_data['sim_ids_up']
    sim_ids_down = config_data['sim_ids_down']

    if 'all' == id.lower():
        stop_ids = list( sim_ids_up ) # Deep copy of list!
    else:
        stop_ids = [ id ]

        if not id in sim_ids_up:
            raise RuntimeError( 'No running simulation (status \'UP\') with ID \'{}\''.format( id ) )

        if id in sim_ids_down:
            raise RuntimeError( 'There is already a finished simulation (status \'DOWN\') with ID \'{}\''.format( id ) )

    if 0 != len( stop_ids ):
        execute( [
            'docker', 'stop', # Stop Docker container.
            '--time' , str( DOCKER_STOP_WAIT_TIME ), # Seconds to wait for stop before killing it.
            *stop_ids
        ] )

    # Update sim setup config.
    if 'all' == id.lower():
        sim_ids_up.clear()
        sim_ids_down.extend( stop_ids )
    else:
        del sim_ids_up[ sim_ids_up.index( *stop_ids ) ]
        sim_ids_down.append( *stop_ids )

    # Save simulation setup configuration.
    config_data.write()

    # On success, return cancelled simulation ID.
    return stop_ids


def main():

    import argparse
    import sys

    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Cancel a simulation (stop simulation container).'
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
        help = 'cancel all running simulations'
    )

    args = parser.parse_args()

    try:
        id = 'all' if ( True == args.all ) else args.id
        sim_id = cancel_sim( args.setup_dir, id )

        print( 'Cancelled simulation(s) with ID = {}'.format( ' '.join( sim_id ) ) )
        sys.exit( 0 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 3 )
