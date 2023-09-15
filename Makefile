VERSION=4.0.1

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
	rm -rf build/
	rm -rf .eggs/
	rm -rf .tox/
	#rm -rf env/

os_deps:
	brew install gdal

prepare:
	clear ; python3.11 -m venv env

deps:
	clear
	env/bin/python -m pip install --upgrade pip
	env/bin/python -m pip install --upgrade setuptools wheel
	env/bin/pip install -r requirements.txt
	env/bin/pip install -r requirements-dev.txt
	env/bin/pip list

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
	clear ; time env/bin/pytest --create-db --reuse-db --no-migrations ${TESTS}

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
	cp htmlcov/index.html docs/source/_static/coverage.html
	open htmlcov/index.html

code_style:
	# Code Style
	clear ; env/bin/pylint ddf django_dynamic_fixture queries

code_checking:
	# Code error checking
	clear ; env/bin/python -m pyflakes ddf django_dynamic_fixture queries

code_feedbacks:
	# PEP8, code style and circular complexity
	clear ; env/bin/flake8 ddf django_dynamic_fixture queries

code_ruff:
	clear ; env/bin/ruff check .
	#clear ; env/bin/ruff check . --fix

check: code_style code_checking code_feedbacks code_ruff

install_precommit_hooks: code_ruff
	clear ; env/bin/ruff check .
	env/bin/pre-commit install

doc: cov
	clear ; cd docs ; make clean html ; open build/html/index.html

tox:
	#brew update ; brew install pyenv
	#pyenv install 3.8 3.9 3.10 3.11
	#pyenv versions
	#pyenv local 3.7 3.8 3.9 3.10 3.11
	clear ; time env/bin/tox --parallel all

build: clean os_deps prepare deps test cov

# Python package tasks

lib: clean test cov doc
	# 	clear ; env/bin/python setup.py build
	# 	clear ; env/bin/python setup.py sdist
	clear ; env/bin/python -m build
	clear ; env/bin/twine check dist/*

publish: lib
	# Fixing Python 3 Certificates
	# /Applications/Python\ 3.7/Install\ Certificates.command
	# Manual upload to PypI
	# http://pypi.python.org/pypi/THE-PROJECT
	# Go to 'edit' link
	# Update version and save
	# Go to 'files' link and upload the file
	clear ; env/bin/twine upload dist/* --username=UPDATE_ME --password=UPDATE_ME

# Git tasks

push: tox doc
	clear ; git push origin `git symbolic-ref --short HEAD`

tag:
	git tag ${VERSION}
	git push origin ${VERSION}

reset_tag:
	git tag -d ${VERSION}
	git push origin :refs/tags/${VERSION}


# GitHub Action

act:
	#brew install act
	time act --container-architecture linux/amd64 --matrix python_version:3.11 --matrix django_version:4.2

actall:
	time act --container-architecture linux/amd64
