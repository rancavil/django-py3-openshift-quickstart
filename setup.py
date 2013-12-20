from setuptools import setup

setup(name='YourAppName', version='1.0',
      description='OpenShift Python-3.3 / Django-1.6 Community Cartridge based application',
      author='Your Name', author_email='admin@example.org',
      url='https://pypi.python.org/pypi',

      #  Uncomment one or more lines below in the install_requires section
      #  for the specific client drivers/modules your application needs.
      install_requires=['Django<=1.6',
			'CherryPy', # If you want serve Django through CherryPy
			'static3',  # If you want serve the static files in the same server
                        #  'mysql-connector-python',
                        #  'pymongo',
                        #  'psycopg2',
      ],
     )
