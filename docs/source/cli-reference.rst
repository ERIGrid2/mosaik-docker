Commands for handling simulation setups
=======================================

``create_sim_setup``
--------------------

Create an empty simulation setup in a new directory:

::

    create_sim_setup [-h] [--id ID] NAME [DIR]


**Positional arguments**:

* ``NAME``: name of the new simulation setup
* ``DIR``: directory to put the generated simulation setup (default: current working directory)

**Optional arguments**:

* ``-h``, ``--help``: show the help message and exit
* ``--id ID``: unique ID for the new simulation setup


``configure_sim_setup``
-----------------------

Configure an existing simulation setup:

::

    configure_sim_setup [-h] -d DOCKER_FILE -s SCENARIO_FILE \
       [--extra-file EXTRA_FILE] [--extra-dir EXTRA_DIR] \
       [--result RESULT] [SETUP_DIR]

**Positional arguments**:

* ``SETUP_DIR``: path to simulation setup directory (default: current working directory)

**Required named arguments**:

* ``-d DOCKER_FILE``, ``--docker-file DOCKER_FILE``: name of Dockerfile for orchestrator
* ``-s SCENARIO_FILE``, ``--scenario-file SCENARIO_FILE``: name of main mosaik script for orchestrator

**Optional arguments**:

* ``-h``, ``--help``: show the help message and exit
* ``--extra-file EXTRA_FILE``: additional file to be added to the orchestrator Docker image
* ``--extra-dir EXTRA_DIR``: additional directory to be added to the orchestrator Docker image
* ``--result RESULT``: paths of result file or folder, i.e., file or folder produced by the simulation that should be retrieved after the simulation has finished (list of strings)


``check_sim_setup``
-------------------

Check if simulation setup is valid:

::

    check_sim_setup [-h] [SETUP_DIR]

**Positional arguments**:

* ``SETUP_DIR``: path to simulation setup directory (default: current working directory)

**Optional arguments**:

* ``-h``, ``--help``: show the help message and exit


``build_sim_setup``
-------------------

Build simulation setup as preparation for running the simulation. 
This includes building the Docker image of the mosaik orchestrator:

::

    build_sim_setup [-h] [SETUP_DIR]

**Positional arguments**:

* ``SETUP_DIR``: path to simulation setup directory (default: current working directory)

**Optional arguments:**

* ``-h``, ``--help``: show the  help message and exit
  

``delete_sim_setup``
--------------------

Delete a simulation setup, including all associated Docker images and containers:

::

    delete_sim_setup [-h] [SETUP_DIR]

**Positional arguments**:

* ``SETUP_DIR``: path to simulation setup directory (default: current working directory)

**Optional arguments:**

* ``-h``, ``--help``: show the help message and exit


Commands for handling simulations
=================================

``start_sim``
-------------

Start a new simulation:

::

    start_sim [-h] [SETUP_DIR] [ID]


**Positional arguments:**

* ``SETUP_DIR``: path to simulation setup directory (default: current working directory)
* ``ID``: simulation ID (Docker container name)

**Optional arguments:**

* ``-h``, ``--help``: show the help message and exit


``cancel_sim``
--------------

Cancel a simulation (stop simulation containers):

::

    cancel_sim [-h] (--id ID | --all) [SETUP_DIR]

**Positional arguments**:

* ``SETUP_DIR``: path to simulation setup directory (default: current working directory)

**Optional arguments**:

* ``-h``, ``--help``: show the help message and exit
* ``--id ID``: simulation ID (Docker container name)
* ``--all``: cancel all running simulations


``clear_sim``
-------------

Delete containers of finished simulations:

::

    clear_sim [-h] (--id ID | --all) [SETUP_DIR]

**Positional arguments**:

* ``SETUP_DIR``: path to simulation setup directory (default: current working directory)

**Optional arguments**:

* ``-h``, ``--help``: show the help message and exit
* ``--id ID``: simulation ID (Docker container name)
* ``--all``: remove all simulation containers


``get_sim_status``
------------------

Get status of all simulations of a mosaik-docker setup.
Updates the simulation setup information about which containers are running (status *UP*) or finished(status *DOWN*) if it is not up to date:

::

    get_sim_status [-h] [SETUP_DIR]

**Positional arguments**:

* ``SETUP_DIR``: path to simulation setup directory (default: current working directory)

**Optional arguments**:

* ``-h``, ``--help``: show the help message and exit


``get_sim_results``
-------------------

Retrieve the results of finished simulations:

::

    get_sim_results [-h] (--id ID | --all) [--overwrite] [SETUP_DIR]

**Positional arguments**:

* ``SETUP_DIR``: path to simulation setup directory (default: current working directory)

**Optional arguments**:

* ``-h``, ``--help``: show the help message and exit
* ``--id ID``: simulation ID (Docker container name)
* ``--all``: retrieve results from all finished simulation containers
* ``--overwrite``: overwrite previously retrieved results


Utility commands
================

``get_sim_ids``
---------------

Get IDs of all running (status *UP*) and finished (status *DOWN*) simulations of a simulation setup:

::

    get_sim_ids [-h] [SETUP_DIR]

**Positional arguments**:

* ``SETUP_DIR``: path to simulation setup directory (default: current working directory)

**Optional arguments**:

* ``-h``, ``--help``: show the help message and exit


``get_sim_setup_root``
----------------------

Check if the specified directory (or any parent directory) contains a simulation setup configuration:

::

    get_sim_setup_root [-h] [DIR]

**Positional arguments**:

* ``DIR``: folder path (default: current working directory)

**Optional arguments**:

* ``-h``, ``--help``: show the help message and exit
