all: test

test:
	nosetests --with-coverage --cover-package sacrud_pages --cover-erase --with-doctest
