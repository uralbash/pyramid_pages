import os

from setuptools import setup

version = '1.0'

here = os.path.dirname(os.path.realpath(__file__))


def read(name):
    with open(os.path.join(here, name)) as f:
        return f.read()

setup(
    name='pyramid_pages_example',
    version=version,
    py_modules=['pyramid_pages_example'],
    install_requires=read('requirements.txt'),
    entry_points="""
[paste.app_factory]
main = pyramid_pages_example:main
    """,
)
