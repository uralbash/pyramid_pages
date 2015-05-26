from setuptools import setup

version = '1.0'

setup(
    name='ps_pages_example',
    version=version,
    py_modules=['ps_pages_example'],
    entry_points="""
[paste.app_factory]
main = ps_pages_example:main
    """,
)
