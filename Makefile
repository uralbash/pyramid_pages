all: test

test:
	nosetests --with-coverage --cover-package ps_pages --cover-erase --with-doctest --nocapture
