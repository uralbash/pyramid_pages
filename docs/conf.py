# -*- coding: utf-8 -*-
from docutils.parsers.rst import directives
from sphinx.directives.code import CodeBlock

directives.register_directive('no-code-block', CodeBlock)

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'https://docs.python.org/3': None,
    'http://docs.sqlalchemy.org/en/latest/': None,
    'http://sqlalchemy-mptt.readthedocs.org/en/master/': None
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'pyramid_pages'
copyright = u'2014, uralbash'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'pyramid_pagesdoc'

html_theme_options = {
    'travis_button': True,
    'github_button': True,
    'github_user': 'uralbash',
    'github_repo': 'pyramid_pages',
}
