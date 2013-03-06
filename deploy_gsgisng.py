from fabric.api import *
from fabric.contrib.files import upload_template

CLONE_URL='https://github.com/Gigaroby/gsgisng.git'

env.hosts = ['geoweb']
env.user='user'
env.key_filename='~/.ssh/geoweb'

@task
def create_site():
    name = env.site_name
    with cd('/www'):
        run('tools/CreateSite -s \"{0}\"'.format(name))
        with cd('{0}'.format(name)):
            upload_template('skelhttps.txt', 'conf/{0}.conf'.format(name), {'site_name': name})
            run('mkdir django')
            with cd('django'):
                run('git clone -q {0} gsgisng'.format(CLONE_URL))
                upload_template('wsgi_template.txt', 'gsgisng/gsgisng/wsgi.py', {'site_name': name})
                run('virtualenv --system-site-packages .venv')
                with cd('gsgisng'), prefix('source ../.venv/bin/activate'):
                    run('pip install -r requirements.txt -q --log=pip-log.txt')

@task
def install_site():
    name = env.site_name
    with cd('/www/{0}/django/gsgisng'.format(name)),\
            prefix('source ../.venv/bin/activate'), \
            shell_env(PYTHONPATH='$PYTHONPATH:gsgisng/'):
        run('django-admin.py --settings=gsgisng.settings.production collectstatic')
        run('django-admin.py --settings=gsgisng.settings.production syncdb')
        run('django-admin.py --settings=gsgisng.settings.production migrate')


@task
def restart_apache():
    sudo('service httpd graceful')
    sudo('service httpd restart')
