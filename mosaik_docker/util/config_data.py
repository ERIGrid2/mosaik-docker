import json
import pathlib

from .._config import CONFIG_FILE_NAME


class ConfigData:
    '''
    This class handles access to simulation setup configuration data.
    '''

    # Constructor.
    def __init__( self, setup_dir ):

        if not ( isinstance( setup_dir, str ) or isinstance( setup_dir, pathlib.Path ) ):
            raise TypeError( 'Parameter \'setup_dir\' must be of type \'str\' or \'pathlib.Path\'' )

        try:
            setup_dir_path = pathlib.Path( setup_dir ).resolve( strict = True )
        except Exception as err:
            raise RuntimeError( 'not a valid directory: {}\n{}'.format( setup_dir, err ) )

        # Load sim setup configuration.
        try:
            self.__sim_setup_file_path = pathlib.Path( setup_dir_path, CONFIG_FILE_NAME ).resolve( strict = True )
        except Exception as err:
            raise RuntimeError( 'not a valid simulation setup: {}\n{}'.format( setup_dir_path, err ) )

        with open( self.__sim_setup_file_path ) as sim_setup_file:
            try:
                self.__config_data = json.load( sim_setup_file )
            except Exception as err:
                raise Exception( 'Invalid JSON format: {}\n{}'.format( self.__sim_setup_file_path, str( err ) ) )


    def __setitem__( self, index, value ):
        '''
        For setting a configuration value.
        '''
        self.__config_data[index] = value


    def __getitem__( self, index ):
        '''
        For retrieving a configuration value.
        '''
        return self.__config_data[index]


    def __contains__( self, item ):
        '''
        Returns a boolean value depending on whether the configuration contains the specified item or not.
        '''
        return item in self.__config_data


    def write( self ):
        '''
        Save configuration.
        '''
        with open( self.path, 'w' ) as sim_setup_file:
            json.dump(
                self.__config_data,
                sim_setup_file,
                indent = 2,
                separators = ( ',', ': ' ) )
            sim_setup_file.write( '\n' )


    @property
    def path( self ):
        '''
        Absolute path to configuration file.
        '''
        return self.__sim_setup_file_path


    @property
    def data( self ):
        '''
        Configuration data as dict.
        '''
        return self.__config_data
