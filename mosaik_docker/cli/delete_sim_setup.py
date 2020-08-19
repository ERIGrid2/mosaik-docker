import pathlib
import shutil

from .cancel_sim import cancel_sim
from .clear_sim import clear_sim
from .._config import ORCH_IMAGE_NAME_TEMPLATE
from ..util.execute import execute
from ..util.config_data import ConfigData


def delete_sim_setup( setup_dir ):
    '''
    Delete a simulation setup, including all associated Docker images and containers.

    :param setup_dir: path to simulation setup (string)
    :return: return dict with status of build process:
        {
            'valid': flag indicating if deletion succeded (boolean)
            'status': detailed status message (string)
        }
    '''

    try:
        # Cancel all running simulations.
        cancel_sim( setup_dir, 'all' )

    except Exception as err:
        return dict( 
            valid = False, 
            status = 'cancelling running simulations failed:\n{}'.format( err )
        )

    try:
        # Clear all finished simulations.
        clear_sim( setup_dir, 'all' )

    except Exception as err:
        return dict( 
            valid = False, 
            status = 'clearing finished simulations failed:\n{}'.format( err )
        )


    try:
        # Retrieve simulation setup configuration.
        config_data = ConfigData( setup_dir )
        sim_setup_id = config_data['id'].strip()

        # Specify name of mosaik orchestrator image.
        orch_image_name = ORCH_IMAGE_NAME_TEMPLATE.format( sim_setup_id.lower() )
    
        execute( [
            'docker', 'image', 'rm', # Remove Docker image.
            orch_image_name # Specify image name.
        ] )

    except Exception as err:
        return dict( 
            valid = False, 
            status = 'remove orchestrator image failed:\n{}'.format( err )
        )

    try:
        setup_dir_path = pathlib.Path( setup_dir ).resolve()
        shutil.rmtree( setup_dir_path )
        
    except Exception as err:
        return dict( 
            valid = False, 
            status = 'deleting simulation setup failed:\n{}'.format( err )
        )

    return dict( 
        valid = True, 
        status = 'deletion of simulation setup succeeded: {}'.format( setup_dir_path ) 
    )


def main():

    import argparse
    import sys

    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Delete a simulation setup, including all associated Docker images and containers.'
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
        delete_status = delete_sim_setup( args.setup_dir )

        print( delete_status['status'] )
        if True == delete_status['valid']:
            sys.exit( 0 )
        else:
            sys.exit( 1 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 3 )