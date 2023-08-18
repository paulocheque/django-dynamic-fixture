from pathlib import Path
from setuptools import setup, find_packages

VERSION = '4.0.0'

tests_require = []

install_requires = []

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(name='django-dynamic-fixture',
      url='https://github.com/paulocheque/django-dynamic-fixture',
      author="paulocheque",
      author_email='paulocheque@gmail.com',
      keywords='python django testing fixture',
      description='A full library to create dynamic model instances for testing purposes.',
      long_description_content_type='text/markdown',
      long_description=long_description,
      license='MIT',
      classifiers=[
          'Framework :: Django',
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: Implementation :: PyPy',
      ],

      version=VERSION,
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='pytest',
      extras_require={'test': tests_require},

      entry_points={ 'nose.plugins': ['queries = queries:Queries', 'ddf_setup = ddf_setup:DDFSetup'] },
      packages=find_packages(),
)

