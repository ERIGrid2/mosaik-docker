from ..util.config_data import ConfigData
from ..util.execute import execute_and_capture_output
from ..util.flatten_list import flatten_list


def get_sim_status( setup_dir ):
    '''
    Get status of all simulations of a mosaik-docker setup.
    Updates the simulation setup information about which containers are running (status UP) or finished (status DOWN) if it is not up to date.

    :param setup_dir: path to simulation setup (string)
    :return: return dict with status information for all simulations of a mosaik-docker simulation setup in the following format:
        {
            'up': { string: string } # running simulation IDs and status
            'down': { string: string } # finished simulation IDs and status
        }
    '''

    # Retrieve simulation setup configuration.
    config_data = ConfigData( setup_dir )
    sim_ids_up = config_data['sim_ids_up']
    sim_ids_down = config_data['sim_ids_down']

    # Check if any simulation with status 'running' has already finished.
    sim_ids_stopped = _diff_status( sim_ids_up, 'running' )
    if 0 != len( sim_ids_stopped ):
        # Update sim setup config accordingly.
        for id in sim_ids_stopped:
            del sim_ids_up[ sim_ids_up.index( id ) ]
            sim_ids_down.append( id )

        # Save simulation setup configuration.
        config_data.write()

    # Retrieve status information from Docker.
    sim_status_up = _retrieve_status( sim_ids_up )
    sim_status_down = _retrieve_status( sim_ids_down )

    return dict(
        up = sim_status_up,
        down = sim_status_down
        )


def _diff_status( ids, status ):
    '''
    Check if Docker containers are in a specified status.
    Returns list of Docker container names that are not in the specified status.

    :param ids: list simulation IDs (Docker container names)
    :param status: supposed status of Docker containers
    :return: list of container names that are not in the supposed status
    '''
    # Define filter for simulations IDs (container names).
    id_filter = [ [ '--filter', 'name={}'.format( id ) ] for id in ids ]

    # Define filter for status.
    status_filter = [ '--filter', 'status={}'.format( status ) ]

    # Retrieve container names (as string).
    out = execute_and_capture_output( [
        'docker', 'ps', # List containers.
        '--no-trunc', # Do not truncate output.
        '--all', # Show all containers (default shows just running).
        *flatten_list( id_filter ), # Filter output based on conditions provided.
        *status_filter, # Filter output based on conditions provided.
        '--format', '{{.Names}}' # Only output container names.
    ] )

    # Parse string to list.
    confirmed_status = out.split( '\n' )

    # Return list of container names that are not in the specified status.
    status_diff = [ id for id in ids if id not in confirmed_status ]
    return status_diff


def _retrieve_status( ids ):
    '''
    Retrieve status information of Docker containers.

    :param ids: list of simulation IDs (Docker container names)
    :return: dict of container status information
    '''
    if 0 == len( ids ):
        return {}

    # Define filter for IDs.
    id_filter = [ [ '--filter', 'name={}'.format( id ) ] for id in ids ]

    # Retrieve container status (as string).
    out = execute_and_capture_output( [
        'docker', 'ps', # List containers.
        '--no-trunc', # Do not truncate output.
        '--all', # Show all containers (default shows just running).
        *flatten_list( id_filter ), # Filter output based on conditions provided.
        '--format', '{{.Names}}:{{.Status}}' # Only output conatainer name and status.
    ] )

    # Parse string to dict.
    status_dict = { s[0]: s[1] for s in [ o.split( ':', 1 ) for o in out.split( '\n' ) ] }

    return status_dict


def main():

    import argparse
    import sys

    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Get status of all simulations of a mosaik-docker setup. Updates the simulation setup information about which containers are running (status UP) or finished (status DOWN) if it is not up to date.'
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

        status = get_sim_status( args.setup_dir )

        sims_up = status['up']
        sims_down = status['down']

        msg = 'running:\n' + '\t{}\n'*len( sims_up ) + 'finished:\n' + '\t{}\n'*len( sims_down )
        str_sims_up = [ '{}: {}'.format( x[0], x[1] ) for x in sims_up.items() ]
        str_sims_down = [ '{}: {}'.format( x[0], x[1] ) for x in sims_down.items() ]
        print( msg.format( *str_sims_up, *str_sims_down ) )

        sys.exit( 0 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 3 )
