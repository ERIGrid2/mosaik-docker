from cookiecutter.main import cookiecutter
import pathlib

from ..util.create_unique_id import create_unique_id


def create_sim_setup( name, dir = '.', id = None ):
    '''
    Create an empty simulation setup in a new directory.

    :param name: name of the simulation setup (string)
    :param dir: directory to put the generated simulation setup (string, default: '.')
    :param id: unique ID for the simulation setup (string, default: None)
    :return: on success, return absolute path to created simulation setup directory (string)
    '''

    if not isinstance( name, str ):
        raise TypeError( 'Parameter \'name\' must be of type \'str\'' )

    if not isinstance( dir, str ):
        raise TypeError( 'Parameter \'dir\' must be of type \'str\'' )

    try:
        dir_path = pathlib.Path( dir ).resolve( strict = True )
    except Exception as err:
        raise FileNotFoundError( '\'{}\' is not a valid directory name'.format( dir ) )

    if pathlib.Path( dir_path, name ).is_dir():
        raise FileExistsError( 'Directory \'{}\' already exists'.format( pathlib.Path( dir_path, name ).resolve( strict = False ) ) )

    if not id == None and not isinstance( id, str ):
        raise TypeError( 'Parameter \'id\' must be of type \'str\'' )

    if id == None:
        id = create_unique_id()

    # Path to cookiecutter template directory.
    template_path = pathlib.Path( 
        pathlib.Path( __file__ ).parent,
        '..', 
        'sim_setup_template' 
        ).resolve( strict = True )

    # Create dict with template parameters.
    template_params = {
        'directory_name': name,
        'id': id
        }

    # Create project from the cookiecutter template.
    cookiecutter(
        str( template_path ),
        output_dir = dir,
        no_input = True,
        extra_context = template_params
        )

    # On success, return name of created simulation setup directory.
    return pathlib.Path( dir_path, name ).resolve()


def main():

    import argparse
    import sys

    # Command line parser.
    parser = argparse.ArgumentParser(
        description = 'Create an empty simulation setup in a new directory.'
    )

    parser.add_argument(
        'name', 
        metavar = 'NAME',
        help = 'name of the new simulation setup'
    )

    parser.add_argument(
        'dir',
        nargs = '?',
        default = '.',
        metavar = 'DIR',
        help = 'directory to put the generated simulation setup (default: current working directory)'
    )

    parser.add_argument(
        '--id', 
        action = 'store',
        default = None,
        metavar = 'ID',
        help = 'unique ID for the new simulation setup'
    )

    args = parser.parse_args()

    try:
        sim_setup_dir = create_sim_setup( args.name, args.dir, args.id )

        print( 'Created new simulation setup: {}'.format( sim_setup_dir ) )
        sys.exit( 0 )

    except Exception as err:

        print( str( err ) )
        sys.exit( 3 )
