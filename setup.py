#from distutils.core import setup
from setuptools import setup, find_packages

# http://guide.python-distribute.org/quickstart.html
# python setup.py sdist
# Create a .pypirc file in ~ dir (cp .pypirc ~)
# python setup.py register
# python setup.py sdist upload
# pip install django-dynamic-fixture
# pip install django-dynamic-fixture --upgrade --no-deps
# Manual upload to PypI
# http://pypi.python.org/pypi/django-dynamic-fixture
# Go to 'edit' link
# Update version and save
# Go to 'files' link and upload the file

VERSION = '1.9.0'

tests_require = [
    'nose>=1.3.6',
    'django-nose>=1.4',
    'coverage==3.7.1',
    'django-coverage>=1.2',
    'tox>=2.0',
    'flake8>=2.4',
    'pyflakes',
    'pylint',
    'jsonfield',
]

install_requires = [
    'six',
]

setup(name='django-dynamic-fixture',
      url='https://github.com/paulocheque/django-dynamic-fixture',
      author="paulocheque",
      author_email='paulocheque@gmail.com',
      keywords='python django testing fixture',
      description='A full library to create dynamic model instances for testing purposes.',
      license='MIT',
      classifiers=[
          'Framework :: Django',
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: Implementation :: PyPy',
      ],

      version=VERSION,
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='runtests.runtests',
      extras_require={'test': tests_require},

      entry_points={ 'nose.plugins': ['queries = queries:Queries', 'ddf_setup = ddf_setup:DDFSetup'] },
      packages=find_packages(),
)

