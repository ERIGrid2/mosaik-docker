import pathlib

from ..util.config_data import ConfigData


def get_sim_setup_root( dir ):
    '''
    Check if the specified directory (or any parent directory) contains a simulation setup configuration.

    :param dir: directory path to check (string)
    :return: return the following dict:
        {
            'valid': boolean # flag indicating if this directory (or any parent directory) contains a simulation setup configuration
            'dir': string # directory containing a simulation setup configuration if 'valid', otherwise empty
        }
    '''
    # Resolve the path.
    dir_path = pathlib.Path( dir ).resolve( strict = True )

    if not dir_path.is_dir():
        raise RuntimeError( 'not a directory path: {}'.format( dir_path ) )

    # Iterate through all parent directories and check if they contain a simulation setup configuration.
    for p in [ dir_path, *dir_path.parents ]:
        try:
            # Retrieve simulation setup configuration.
            config_data = ConfigData( p )

            return dict( valid = True, dir = str( p ) )
        except: # Exception as err:
            #print( err )
            pass

    # Nothing found.
    return dict( valid = False, dir = '' )


def main():

    import argparse
    import sys

    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Check if the specified directory (or any parent directory) contains a simulation setup configuration.'
    )

    parser.add_argument(
        'dir',
        nargs = '?',
        default = '.',
        metavar = 'DIR',
        help = 'folder path (default: current working directory)'
    )

    args = parser.parse_args()

    try:
        setup_root = get_sim_setup_root( args.dir )

        if True == setup_root['valid']:
            print( setup_root['dir'] )
            sys.exit( 0 )
        else:
            print( 'This directory is not part of a simulation setup: {}'.format( pathlib.Path( args.dir ).resolve() ) )
            sys.exit( 1 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 3 )