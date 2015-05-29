all: test

test:
	nosetests --with-coverage --cover-package pyramid_pages --cover-erase --with-doctest --nocapture
