VERSION=3.1.3

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
	#clear ; env/bin/python -i -c "from ddf import *"
	clear ; env/bin/python manage.py shell
	# from ddf import *

# Python code tasks

compile:
	env/bin/python -OO -m compileall .

test:
	# Run specific test:
	# TESTS=django_dynamic_fixture.tests.FILE::CLASS::METHOD make test
	clear ; env/bin/pytest --create-db --reuse-db --no-migrations ${TESTS}
	# clear ; time env/bin/tox --parallel all -e django111-py27
	# clear ; time env/bin/tox --parallel all -e django20-py37

testfailed:
	clear ; env/bin/pytest --create-db --reuse-db --no-migrations ${TESTS} --last-failed

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
	# TESTS=django_dynamic_fixture.tests.FILE::CLASS::METHOD make test_postgres
	clear ; env/bin/pytest --reuse-db --no-migrations --ds=settings_postgres ${TESTS}

test_mysql:
	# TESTS=django_dynamic_fixture.tests.FILE::CLASS::METHOD make test_mysql
	clear ; env/bin/pytest --reuse-db --no-migrations --ds=settings_mysql ${TESTS}

cov:
	clear ; env/bin/pytest --create-db --reuse-db --no-migrations -v --cov=django_dynamic_fixture --cov-report html
	open htmlcov/index.html

coveralls:
	clear ; env/bin/coveralls debug --verbose

coveralls_publish:
	clear ; env/bin/coveralls --verbose

clear_github_img_cache:
	curl -X PURGE https://camo.githubusercontent.com/95b7e3529338697ecffdf67add40931d066a35e1/68747470733a2f2f636f766572616c6c732e696f2f7265706f732f7061756c6f6368657175652f646a616e676f2d64796e616d69632d666978747572652f62616467652e7376673f6272616e63683d6d6173746572

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
	# Fixing Python 3 Certificates
	# /Applications/Python\ 3.7/Install\ Certificates.command
	#
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
