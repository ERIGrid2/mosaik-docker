********************
Python API reference
********************

Package *mosaik-docker* provides the following Python methods.
They can be accessed via package ``mosaik_docker.cli``:

.. code-block:: python

    from mosaik_docker.cli import *


Methods for handling simulation setups
======================================

``create_sim_setup``
--------------------

Create an empty simulation setup in a new directory.

.. code-block:: python

    create_sim_setup( name, dir = '.', id = None )

**Parameters**:

* ``name``: name of the simulation setup (string)
* ``dir``: directory to put the generated simulation setup (string, default: ``'.'``)
* ``id``: unique ID for the simulation setup (string, default: ``None``)

**Return value**: on success, return absolute path to created simulation setup directory (string)


``configure_sim_setup``
-----------------------

Configure an existing simulation setup.

.. code-block:: python

    configure_sim_setup( 
        setup_dir,
        docker_file,
        scenario_file,
        extra_files = [],
        extra_dirs = [],
        results = []
        )

**Parameters**:

* ``setup_dir``: directory of the simulation setup (string, default: ``'.'``)
* ``docker_file``: name of the Dockerfile used for building the simulation orchestrator image (string)
* ``scenario_file``: name of the mosaik scenario file (string)
* ``extra_files``: additional files to be added to the simulation orchestrator image (list of strings)
* ``extra_dirs``: additional directories to be added to the simulation orchestrator image (list of strings)
* ``results``: list of paths of result files or folders, i.e., files or folders produced by the simulation that should be retrieved after the simulation has finished (list of strings)
 
**Return value**: on success, return absolute path to simulation setup config file (string)
	

``check_sim_setup``
-------------------

Check if simulation setup is valid.

.. code-block:: python

    check_sim_setup( setup_dir )

**Parameters**:

* ``setup_dir``: path to simulation setup (string)

**Return value**: return dict with status of setup check in the following format:

.. code-block:: python

    {
        'valid': boolean # flag indicating if setup is valid
        'status': string # detailed status message
    }


``build_sim_setup``
-------------------

Build simulation setup as preparation for running the simulation.
This includes building the Docker image of the mosaik orchestrator.
  
.. code-block:: python

    build_sim_setup( setup_dir, out_stream = print ):

**Parameters**:

* ``setup_dir``: path to simulation setup (string)
* ``out_stream``: output from the build process to stderr will be piped to this stream (callable)

**Return value**: return dict with status of build process:

.. code-block:: python

    {
        'valid': flag indicating if build succeded (boolean)
        'status': detailed status message (string)
    }

``delete_sim_setup``
--------------------

Delete a simulation setup, including all associated Docker images and containers.

.. code-block:: python

    delete_sim_setup( setup_dir )

**Parameters**:

* ``setup_dir``: path to simulation setup (string)

**Return value**: return dict with status of build process:

.. code-block:: python

    {
        'valid': flag indicating if deletion succeded (boolean)
        'status': detailed status message (string)
    }


Methods for handling simulations
================================

``start_sim``
-------------

Start a new simulation.

.. code-block:: python

    start_sim( setup_dir, id = None )

**Parameters**:

* ``setup_dir``: path to simulation setup (string)
* ``id``: ID of new simulation (string, default: ``None``)

**Return value**: on success, return new simulation ID (int)


``cancel_sim``
--------------

Cancel a simulation (stop simulation container).

.. code-block:: python

    cancel_sim( setup_dir, id )

**Parameters**:

* ``setup_dir``: path to simulation setup (string)
* ``id``: either ``'all'`` or ID of running simulation container (string)

**Return value**: on success, return ID of cancelled simulation (int)


``clear_sim``
-------------

Delete containers of finished simulations.

.. code-block:: python

    clear_sim( setup_dir, id )

**Parameters**:

* ``setup_dir``: path to simulation setup (string)
* ``id``: either ``'all'`` or ID of simulation container to be cleared (string)

**Return value**: on success, return list of cleared simulation IDs (list of string)


``get_sim_status``
------------------

Get status of all simulations of a mosaik-docker setup.
Updates the simulation setup information about which containers are running (status *UP*) or finished (status *DOWN*) if it is not up to date.

.. code-block:: python

    get_sim_status( setup_dir )

**Parameters**:

* ``setup_dir``: path to simulation setup (string)

**Return value**: return dict with status information for all simulations of a mosaik-docker simulation setup in the following format:

.. code-block:: python

    {
        'up': { string: string } # running simulation IDs and status
        'down': { string: string } # finished simulation IDs and status
    }


``get_sim_results``
-------------------

Retrieve the results of finished simulations.

.. code-block:: python

    get_sim_results( setup_dir, id, overwrite = False )

**Parameters**:

* ``setup_dir``: path to simulation setup (string)
* ``id``: either 'all' or ID of finished simulation container (string)
* ``overwrite``: overwrite previously retrieved results (boolean, default: ``False``)

**Return value**: on success, return ID(s) of simulation(s) for which results have been retrieved (string)


Utility methods
===============

Get IDs of all running (status *UP*) and finished (status *DOWN*) simulations of a simulation setup.

``get_sim_ids``
---------------

.. code-block:: python

    get_sim_ids( setup_dir )

**Parameters**:

* ``setup_dir``: path to simulation setup (string)

**Return value**: return dict with simulation IDs in the following format:

.. code-block:: python

    {
        'up': [string] # IDs of running simulations
        'down': [string] # IDs of finished simulations
    }


``get_sim_setup_root``
----------------------

Check if the specified directory (or any parent directory) contains a simulation setup configuration.

.. code-block:: python

    get_sim_setup_root( dir )

**Parameters**:

* ``dir``: directory path to check (string)

**Return value**: return the following dict:

.. code-block:: python

    {
        'valid': boolean # flag indicating if this directory (or any parent directory) contains a simulation setup configuration
        'dir': string # directory containing a simulation setup configuration if 'valid', otherwise empty
    }
