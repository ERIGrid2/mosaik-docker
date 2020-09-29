Prerequisites
=============

You will need `Python <https://python.org>`_ (tested with version >= 3.6) to install the extension.
For the extension to work properly, you will also need a working installation of `Docker Engine <https://docs.docker.com/engine/install/>`_.

Installation
============

The package is available via the official `Python Package Index <https://pypi.org/project/mosaik-docker/>`_.
Install it from the command line:

.. code-block:: bash

    pip install mosaik-docker

Troubleshoot
============

In case you get error messages similar to the following one:

..
	Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.40/containers/json: dial unix /var/run/docker.sock: connect: permission denied

Check if the user has been `added to group <https://docs.docker.com/engine/install/linux-postinstall/>`_ ``docker``.