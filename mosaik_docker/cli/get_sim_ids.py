from ..util.config_data import ConfigData


def get_sim_ids( setup_dir ):
    '''
    Get IDs of all running (status 'UP') and finished (status 'DOWN') simulations of a simulation setup.

    :param setup_dir: path to simulation setup (string)
    :return: return dict with simulation IDs in the following format:
        {
            'up': [string] # IDs of running simulations
            'down': [string] # IDs of finished simulations
        }
    '''
    # Retrieve simulation setup configuration.
    config_data = ConfigData( setup_dir )

    sim_ids_up = config_data['sim_ids_up']
    sim_ids_down = config_data['sim_ids_down']

    status = dict( up = sim_ids_up, down = sim_ids_down )

    return status


def main():

    import argparse
    import sys

    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Get IDs all of running (status \'UP\') and finished (status \'DOWN\') simulations of a simulation setup.'
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

        sim_ids = get_sim_ids( args.setup_dir )

        sim_ids_up = sim_ids['up']
        sim_ids_down = sim_ids['down']

        msg = 'running:\n' + '\t{}\n'*len( sim_ids_up ) + 'finished:\n' + '\t{}\n'*len( sim_ids_down)
        print( msg.format( *sim_ids_up, *sim_ids_down ) )

        sys.exit( 0 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 3 )
