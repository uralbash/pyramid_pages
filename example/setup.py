from setuptools import setup

version = '1.0'

setup(
    name='pyramid_pages_example',
    version=version,
    py_modules=['pyramid_pages_example'],
    entry_points="""
[paste.app_factory]
main = pyramid_pages_example:main
    """,
    install_requires=[
        "zope.sqlalchemy",
    ],
)
