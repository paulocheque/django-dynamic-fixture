VERSION=1.9.0

clean:
	clear
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	env/bin/python setup.py clean --all
	rm -rf *.egg
	rm -rf *.egg-info/
	rm -rf *.log
	rm -rf ~*
	rm -rf data/
	rm -rf dist/
	rm -rf .eggs/

prepare:
	clear ; python3.5 -m venv env
	#clear ; virtualenv env -p python3.5

deps:
	clear
	env/bin/pip install -r requirements.txt
	env/bin/pip install -r requirements-dev.txt

shell:
	clear ; env/bin/python

test:
	clear ; time env/bin/python manage.py test

test2:
	clear ; time env/bin/python setup.py test

tox:
	clear ; time tox

push: test
	clear ; git push origin master

compile:
	env/bin/python -OO -m compileall .

lib:
	clear ; env/bin/python setup.py clean --all
	clear ; env/bin/python setup.py test
	clear ; env/bin/python setup.py build

register:
	clear ; env/bin/python setup.py clean --all
	clear ; env/bin/python setup.py sdist
	clear ; env/bin/python setup.py register

publish: clean test
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

tag:
	git tag ${VERSION}
	git push origin ${VERSION}

reset_tag:
	git tag -d ${VERSION}
	git push origin :refs/tags/${VERSION}
