from fabric.api import env
from deploy_gsgisng import *

env.key_filename='~/.ssh/geoweb'
env.roledefs = {
    'web': ['user@geoweb'],
    'sql': ['geopg'],
    'monitor': ['geomonitor'],
    'wps': ['georun'],
}
