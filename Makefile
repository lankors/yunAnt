.PHONY: help

help:
	@echo 'Command:'
	@echo 'install    install the package.'
	@echo 'pack       pack the package only in local.'
	@echo 'upload     upload package to official pypi site.'
	@echo 'clean      clean package files.'

install:
	python setup.py install

pack:
	python setup.py sdist --formats=gztar

upload:
	python setup.py sdist --formats=gztar register upload

clean:
	rm -rf dist lazyxml.egg-info build
	find . -name '*.py[co]'|xargs rm -f