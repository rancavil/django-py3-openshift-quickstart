Django 1.6 and Python 3 on OpenShift
====================================

This git repository helps you get up and running quickly w/ a Django 1.6 and
Python 3.3 installation on OpenShift.  The Django project name used in this
repo is 'openshift' but you can feel free to change it.  Right now the
backend is sqlite3 and the database runtime is found in
`$OPENSHIFT_DATA_DIR/db.sqlite3`.

Before you push this app for the first time, you will need to change
the [Django admin password](#admin-user-name-and-password).
Then, when you first push this
application to the cloud instance, the sqlite database is copied from
`wsgi/openshift/db.sqlite3` to $OPENSHIFT_DATA_DIR/ with your newly 
changed login credentials. Other than the password change, this is the 
stock database that is created when `python manage.py syncdb` is run with
only the admin app installed.

On subsequent pushes, a `python manage.py syncdb` is executed to make
sure that any models you added are created in the DB.  If you do
anything that requires an alter table, you could add the alter
statements in `GIT_ROOT/.openshift/action_hooks/alter.sql` and then use
`GIT_ROOT/.openshift/action_hooks/deploy` to execute that script (make
sure to back up your database w/ `rhc app snapshot save` first :) )

With this you can install Django 1.6 with Python 3.3 on OpenShift.

Running on OpenShift
--------------------

Create an account at http://openshift.redhat.com/

Install the RHC client tools if you have not already done so:
    
     sudo gem install rhc

Create a python-3.3 application

     rhc app create djangopy3 python-3.3

Or create the application python-3.3 with the admin web console.

     https://www.openshift.com/

Connect into your OpenShift account and Add Application and select Python 3.3.

Create the Python application with the name djangopy3.

Add this upstream repo

     cd djangopy3
     git remote add upstream -m master git://github.com/rancavil/django-py3-openshift-quickstart.git
     git pull -s recursive -X theirs upstream master

####Note:
If you want to use the Redis-Cloud with Django see [the wiki](https://github.com/rancavil/django-py3-openshift-quickstart/wiki/Django-1.6-with-Redis-Cloud) 

Then push the repo upstream

     git push

Here, the [admin user name and password will be displayed](#admin-user-name-and-password), so pay
special attention.
	
That's it. You can now checkout your application at:

     http://djangopy3-$yournamespace.rhcloud.com

Admin user name and password
----------------------------
As the `git push` output scrolls by, keep an eye out for a
line of output that starts with `Django application credentials: `. This line
contains the generated admin password that you will need to begin
administering your Django app. This is the only time the password
will be displayed, so be sure to save it somewhere. You might want 
to pipe the output of the git push to a text file so you can grep for
the password later.

When you make:

      git push

In the console output, you must find something like this:

     remote: Django application credentials:
     remote: 	user: admin
     remote: 	SY1ScjQGb2qb

Or you can go to SSH console, and check the CREDENTIALS file located 
in $OPENSHIFT_DATA_DIR.

     cd $OPENSHIFT_DATA_DIR
     vi CREDENTIALS

You should see the output:

     Django application credentials:
     		 user: admin
     		 SY1ScjQGb2qb

After, you can change the password in the Django admin console.

Django project directory structure
----------------------------------

     django3/
          .gitignore
          .openshift/
               README.md
               action_hooks/  (Scripts for deploy the application)
                    build
                    post_deploy
                    pre_build
                    deploy
                    secure_db.py
               cron/
               markers/
          setup.py   (Setup file with de dependencies and required libs)
          wsgi.py (This file execute Django over on WSGI for testing)
          README.md
          requirements.txt (for additionals packages dependencies)
          libs/ (Adicional libraries)
     	  data/	(For not-externally exposed wsgi code)
          wsgi/	(Externally exposed wsgi goes)
               application (Script to execute the application on wsgi)
               openshift/  (Django project directory)
                    __init__.py
                    manage.py
                    openshiftlibs.py
                    openshiftstaticfiles.py (lib to use static files on the same server)
                    settings.py
                    urls.py
                    views.py
                    templates/
                         home/
                            home.html (Default home page, change it)
               static/ (Public static content gets served here)

From HERE you can start with your own application.

Important
---------

Django doesn't recommend use of its static file (like css, js) on production server for a number of reasons.

For use Django on wsgi and serve the static files in the same server, it is necesary use the additional package static3.
You can install it in the setup.py

On OpenShift, Django is served through wsgi, like cherrypy, this package can be installed with setup.py

     from setuptools import setup

     import os

     # Put here required packages or
     # Uncomment one or more lines below in the install_requires section
     # for the specific client drivers/modules your application needs.
     packages = ['Django<=1.6',
                 'static3',  # If you want serve the static files in the same server
                  #  'mysql-connector-python',
                  #  'pymongo',
                  #  'psycopg2',
     ]

     if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
           packages.append('django-redis-cache')
           packages.append('hiredis')

     setup(name='YourAppName', version='1.0',
           description='OpenShift Python-3.3 / Django-1.6 Community Cartridge based application',
           author='Your Name', author_email='admin@example.org',
           url='https://pypi.python.org/pypi',
           install_requires=packages,
     )

