***************************
Using package mosaik-docker
***************************

Overview
========

Package *mosaik-docker* eases the deployment of the `mosaik co-simulation framework <https://mosaik.offis.de/>`_ with `Docker <https://docs.docker.com/>`_.
A typical *mosaik-docker* workflow contains the following steps:

1. **Create a simulation setup**: A *simulation setup* is a directory that contains all necessary scripts and configuration files. Package *mosaik-docker* provides a command to create a "bare" simulation setup that needs be adapted to your application. To do so, you need to provide the following:

  * Provide the *mosaik scenario file* for your co-simulation.
  * Provide the *Dockerfile(s)* for the *mosaik sim manager* (and optionally also other simulators).

2. **Configure simulation setup**: Specify the mosaik scenario file and Dockerfile(s) to be used for your simulation setup. You can also add additional input files or folder and specify output files.

3. **Check and build simulation setup**: Check if your simulation setup is valid and build the Docker images for running the simulations.

4. **Run simulations and check their status**: You can start / stop new simulation runs and check their current execution status.

5. **Retrieve simulation results**: After a simulations has successfully finished, you can retrieve its results.


In the following, these steps are explained in more detail.
For each step, the required commands (for the command line terminal) are explained.
If you want to use *mosaik-docker* via its graphical user interface, you can find more information `here <https://mosaik-docker.readthedocs.io/projects/jupyter/en/latest/usage.html#using-jupyterlab-s-graphical-user-interface>`_.


Create a simulation setup
=========================

A *simulation setup* is a directory that contains all necessary scripts and configuration files.
Package *mosaik-docker* provides the ``create_sim_setup`` command to create a template for a simulation setup that can be adapted to your needs (see `here <https://mosaik-docker.readthedocs.io/en/latest/cli-reference.html#create-sim-setup>`_ for details):

>>> create_sim_setup MySimSetup
Created new simulation setup: /home/user/MySimSetup

This will create a new directory to which you have to add the following:

* a mosaik scenario that

  #. starts the simulators
  #. instantiates models within the simulators
  #. connects the model instances of different simulators to establish the data flow between them

* a Dockerfile for running sim manager (i.e., the mosaik orchestrator that executes the scenario)
* Dockerfiles for running the simulators (optional)
* input files and/or folders (optional)

Examples of a *monolithic simulation setup* (the mosaik sim manager and all simulators run in the same Docker container) and a *distributed simulation setup* (the mosaik sim manager and the simulators run in individual Docker containers) can be found `here <https://github.com/ERIGrid2/mosaik-docker-demo>`_.


Configure simulation setup
==========================

The configuration for the simulation setup is stored in file ``mosaik-docker.json``.
All required information to run a dockerized mosaik simulation is stored in this file (mosaik scenario file, Dockerfile(s), input files and/or folder, output files).
Package *mosaik-docker* provides the ``configure_sim_setup`` command for the configuration of simulation setups (see `here <https://mosaik-docker.readthedocs.io/en/latest/cli-reference.html#configure-sim-setup>`_ for details):

>>> configure_sim_setup --scenario-file main.py --docker-file dockerfiles/Dockerfile_main --extra-file demo_lv_grid.json --result demo.hdf5
Updated simulation configuration file: /home/user/MySimSetup/mosaik-docker.json

**NOTE**: 
It is highly recommended to NOT edit this configuration file by hand, but use the commands provided my *mosaik-docker*!


Check and build simulation setup
================================

You can use command ``check_sim_setup`` check if your simulation setup is valid (see `here <https://mosaik-docker.readthedocs.io/en/latest/cli-reference.html#check-sim-setup>`_ for details):

>>> check_sim_setup
simulation setup is valid: /home/user/MySimSetup

Once your setup seems to be fine, you can use command ``build_sim_setup`` to build the Docker images for running your simulation (see `here <https://mosaik-docker.readthedocs.io/en/latest/cli-reference.html#build-sim-setup>`_ for details):

>>> build_sim_setup 
Sending build context to Docker daemon    701kB
Step 1/11 : FROM mosaik/orch-base:v1
 ---> b239b8430a38
Step 2/11 : ARG SCENARIO_FILE
 ---> Using cache
 ---> 8df59427a94c
Step 3/11 : ARG EXTRA
 ---> Using cache
 ---> 57355196ae2a
Step 4/11 : RUN pip install mosaik-csv==1.0.3
 ---> Using cache
 ---> 5f98b074eccc
Step 5/11 : RUN pip install mosaik-hdf5==0.3
 ---> Using cache
 ---> 96daeb62dee8
Step 6/11 : RUN pip install mosaik-householdsim==2.0.3
 ---> Using cache
 ---> 821122dc1287
Step 7/11 : RUN pip install mosaik-pypower==0.7.2
 ---> Using cache
 ---> 06dea0bd92ca
Step 8/11 : RUN pip install networkx==2.4
 ---> Using cache
 ---> c8fdf48dfd2e
Step 9/11 : COPY $SCENARIO_FILE .
 ---> Using cache
 ---> 15f73891d199
Step 10/11 : COPY $EXTRA .
 ---> 2e3050d9fe48
Step 11/11 : ENTRYPOINT python $SCENARIO_FILE
 ---> Running in a428eddbdfba
Removing intermediate container a428eddbdfba
 ---> 90db1e9de30b
Successfully built 90db1e9de30b
Successfully tagged mosaik/orch/my-sim-setup:latest
building simulation setup succeeded: /home/user/MySimSetup


Run simulations and check their status
======================================

Once the Docker images have been successfully built, you can use command ``start_sim`` to start new simulation runs (see `here <https://mosaik-docker.readthedocs.io/en/latest/cli-reference.html#start-sim>`_ for details):

>>> start_sim 
ddf4398dacaa0208ac6a0b4c7c4c482a981aa7fa7d458fca578eb31728f0e735
Started new simulation with ID = d150f4

Use command ``get_sim_status`` to check the current execution status of your simulations (see `here <https://mosaik-docker.readthedocs.io/en/latest/cli-reference.html#get-sim-status>`_ for details):

>>> get_sim_status 
running:
        d150f4: Up 1 second
finished:
        766540: Exited (0) 18 seconds ago


Retrieve simulation results
===========================

After a simulation has successfully finished, you can use command ``get_sim_results`` to retrieve the corresponding results (see `here <https://mosaik-docker.readthedocs.io/en/latest/cli-reference.html#get-sim-results>`_ for details):

>>> get_sim_results --id 766540
Retrieved results for simulation(s) with ID = 766540
