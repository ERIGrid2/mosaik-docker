# Getting Started ...

## Overview

To set up a dockerized mosaik simulation setup you need to provide the following:

 * add a mosaik scenario that
   1. starts the simulators
   2. instantiates models within the simulators
   3. connects the model instances of different simulators to establish the data flow between them
 * add a Dockerfile for running the mosaik scenario
 * add Dockerfiles for running the simulators (optional)
 * add additional resources, e.g., data files (optional)
 * add a mosaik-docker simulation setup configuration

## Examples
 
Basic examples of using mosaik-docker are available [here](https://github.com/ERIGrid2/mosaik-docker-demo).
