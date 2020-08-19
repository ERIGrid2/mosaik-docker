from .starter import start_dockerimage, start_dockerfile

from mosaik.simmanager import StarterCollection

# Add new simulation starters.
s = StarterCollection()
s['dockerimage'] = start_dockerimage
s['dockerfile'] = start_dockerfile