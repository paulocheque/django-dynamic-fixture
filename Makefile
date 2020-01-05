VERSION=3.0.0

# Python env tasks

clean:
	clear
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	rm -rf *.egg
	rm -rf *.egg-info/
	rm -rf *.log
	rm -rf ~*
	rm -rf data/
	rm -rf dist/
	rm -rf .eggs/

prepare:
	clear ; python3 -m venv env

os_deps:
	brew install gdal
	env/bin/pip install --upgrade pip

deps:
	clear
	env/bin/pip install --upgrade pip
	env/bin/pip install -r requirements.txt
	env/bin/pip install -r requirements-dev.txt

shell:
	# clear ; env/bin/python -i -c "from ddf import *"
	clear ; env/bin/python manage.py shell

# Python code tasks

compile:
	env/bin/python -OO -m compileall .

test:
	# Run specific test:
	# TESTS=pytest django_dynamic_fixture.tests.FILE::CLASS::METHOD make test
	clear ; env/bin/pytest --create-db --reuse-db --no-migrations ${TESTS}
	# clear ; time env/bin/tox --parallel all -e django111-py27
	# clear ; time env/bin/tox --parallel all -e django20-py37

config_postgres:
	psql -U postgres -c "create extension postgis"
	# set up postgresql
	psql -U postgres -c "create role cacheops login superuser"
	# postgis django backend requires these to exist
	psql -U postgres -c "create database cacheops"
	psql -U postgres -c "create database cacheops_slave"
	# create db and user
	psql -c "CREATE DATABASE ddf;" -U postgres
	psql -c "CREATE USER ddf_user WITH PASSWORD 'ddf_pass';" -U postgres
	psql -c "ALTER USER ddf_user CREATEDB;" -U postgres
	psql -c "ALTER USER ddf_user WITH SUPERUSER;" -U postgres

test_postgres:
	# TESTS=pytest django_dynamic_fixture.tests.FILE::CLASS::METHOD make test_postgres
	clear ; env/bin/pytest --reuse-db --no-migrations --ds=settings_postgres ${TESTS}

test_mysql:
	# TESTS=pytest django_dynamic_fixture.tests.FILE::CLASS::METHOD make test_mysql
	clear ; env/bin/pytest --reuse-db --no-migrations --ds=settings_mysql ${TESTS}

cov:
	# TESTS=pytest django_dynamic_fixture.tests.FILE::CLASS::METHOD make cov
	clear ; env/bin/pytest --create-db --reuse-db --no-migrations --cov=django_dynamic_fixture ${TESTS}

coveralls:
	clear ; env/bin/coveralls

code_style:
	# Code Style
	clear ; env/bin/pylint ddf django_dynamic_fixture ddf_setup queries

code_checking:
	# Code error checking
	clear ; env/bin/python -m pyflakes ddf django_dynamic_fixture ddf_setup queries

code_feedbacks:
	# PEP8, code style and circular complexity
	clear ; env/bin/flake8 ddf django_dynamic_fixture ddf_setup queries

doc:
	clear ; cd docs ; make clean html ; open build/html/index.html

tox:
	clear ; time env/bin/tox --parallel all

build: clean prepare os_deps deps test

# Python package tasks

setup_clean:
	clear ; env/bin/python setup.py clean --all

setup_test:
	clear ; time env/bin/python setup.py test

lib: setup_clean setup_test
	clear ; env/bin/python setup.py build

register: setup_clean setup_test
	clear ; env/bin/python setup.py sdist
	clear ; env/bin/python setup.py register

publish: setup_clean setup_test
	# http://guide.python-distribute.org/quickstart.html
	# python setup.py sdist
	# python setup.py register
	# Create a .pypirc file in ~ dir (cp .pypirc ~)
	# python setup.py sdist upload
	# Manual upload to PypI
	# http://pypi.python.org/pypi/THE-PROJECT
	# Go to 'edit' link
	# Update version and save
	# Go to 'files' link and upload the file
	clear ; env/bin/python setup.py clean sdist upload

# Git tasks

push: tox doc
	clear ; git push origin `git symbolic-ref --short HEAD`

tag:
	git tag ${VERSION}
	git push origin ${VERSION}

reset_tag:
	git tag -d ${VERSION}
	git push origin :refs/tags/${VERSION}
