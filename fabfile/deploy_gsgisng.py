import os
from os.path import join as j
from fabric.api import *
from fabric.contrib.files import upload_template

CLONE_URL='https://github.com/Gigaroby/gsgisng.git'

def template(name):
    my_path = os.path.dirname(__file__)
    print j(my_path, '..', 'templates', name)
    return j(my_path, '..', 'templates', name) 

@roles('web')
@task
def create_site():
    name = env.site_name
    with cd('/www'):
        run('tools/CreateSite -s \"{0}\"'.format(name))
        with cd(name):
            conf_file = 'conf/{0}.conf'.format(name) 
            run('rm -f {0}'.format(conf_file))
            upload_template(template('skelhttps.txt'), conf_file, {'site_name': name})
            run('mkdir django')
            with cd('django'):
                run('git clone -q {0} gsgisng'.format(CLONE_URL))
                upload_template(template('wsgi_template.txt'),
                        'gsgisng/gsgisng/wsgi.py', {'site_name': name})
                run('virtualenv --system-site-packages .venv')
                with cd('gsgisng'), prefix('source ../.venv/bin/activate'):
                    run('pip install -r requirements.txt -q --log=pip-log.txt')

@roles('web')
@task
def install_site():
    name = env.site_name
    with cd('/www/{0}/django/gsgisng'.format(name)),\
            prefix('source ../.venv/bin/activate'), \
            shell_env(PYTHONPATH='$PYTHONPATH:gsgisng/'):
        run('django-admin.py --settings=gsgisng.settings.production collectstatic')
        run('django-admin.py --settings=gsgisng.settings.production syncdb')
        run('django-admin.py --settings=gsgisng.settings.production migrate')


@roles('web')
@task
def restart_apache():
    run('sudo service httpd graceful')
    run('sudo service httpd restart')
