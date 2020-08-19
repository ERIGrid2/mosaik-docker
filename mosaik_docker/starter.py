from mosaik.simmanager import make_proxy
from mosaik.exceptions import ScenarioError

import os
import sys
import shlex
import subprocess



def start_dockerimage(world, sim_name, sim_config, sim_id, sim_params):
    """
    ...
    """
    print('###### start_dockerimage ######')
    replacements = {
        'addr': '%s:%s' % (world.config['addr'][0], world.config['addr'][1]),
        'python': sys.executable,
    }
    cmd = sim_config['dockerimage'] % replacements
    if 'posix' in sim_params.keys():
        posix = sim_params.pop('posix')
        cmd = shlex.split(cmd, posix=posix)
    else:
        cmd = shlex.split(cmd, posix=(os.name != 'nt'))
    cwd = sim_config['cwd'] if 'cwd' in sim_config else '.'

    # Make a copy of the current env. vars dictionary and update it with the
    # user provided values (or an empty dict as a default):
    env = dict(os.environ)
    env.update(sim_config.get('env', {}))

    kwargs = {
        'bufsize': 1,
        'cwd': cwd,
        'universal_newlines': True,
        'env': env,  # pass the new env dict to the sub process
    }
    try:
        proc = subprocess.Popen(cmd, **kwargs)
    except (FileNotFoundError, NotADirectoryError) as e:
        # This distinction has to be made due to a change in python 3.8.0.
        # It might become unecessary for future releases supporting
        # python >= 3.8 only.
        if str(e).count(':')==2:
            eout = e.args[1]
        else:
            eout = str(e).split('] ')[1]
        raise ScenarioError('Simulator "%s" could not be started: %s'
                            % (sim_name, eout)) from None

    proxy = make_proxy(world, sim_name, sim_config, sim_id, sim_params,
                       proc=proc)
    return proxy
	

def start_dockerfile(world, sim_name, sim_config, sim_id, sim_params):
    """
    ...
    """
    print('###### start_dockerfile ######')
    addr = sim_config['connect']
    try:
        host, port = addr.strip().split(':')
        addr = (host, int(port))
    except ValueError:
        raise ScenarioError('Simulator "%s" could not be started: Could not '
                            'parse address "%s"' %
                            (sim_name, sim_config['connect'])) from None

    proxy = make_proxy(world, sim_name, sim_config, sim_id, sim_params,
                       addr=addr)
    return proxy