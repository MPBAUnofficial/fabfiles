from fabric.api import env
from deploy_gsgisng import *

env.hosts = ['geoweb']
env.user='user'
env.key_filename='~/.ssh/geoweb'
