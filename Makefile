all: test

test:
	nosetests --with-coverage --cover-package pyramid_sacrud_pages --cover-erase --with-doctest --nocapture
