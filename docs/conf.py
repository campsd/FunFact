# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# os.environ['SPHINX_APIDOC_OPTIONS'] = '''members,undoc-members,special-members,\
# inherited-members,show-inheritance'''
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))
import funfact


# Automatically call apidoc
# See https://github.com/rtfd/readthedocs.org/issues/1139
def run_apidoc(_):

    current_dir = os.path.abspath(os.path.dirname(__file__))
    module = os.path.join(current_dir, "..", "funfact")

    apidir = os.path.join(current_dir, "apidoc")
    argv = [
        "--force",
        "--module-first",
        "--no-toc",
        "--separate",
        "-o", apidir,
        module
    ]

    try:
        # Sphinx 1.7+
        from sphinx.ext import apidoc
        apidoc.main(argv)
    except ImportError:
        # Sphinx 1.6 (and earlier)
        from sphinx import apidoc
        argv.insert(0, apidoc.__file__)
        apidoc.main(argv)


# -- enable documentation of __call__
def keep_call(app, what, name, obj, would_skip, options):
    if name in ["__call__", "__add__", "__mul__"]:
        return False
    else:
        return would_skip


# -- connect all the features
def setup(app):
    app.connect('builder-inited', run_apidoc)
    app.connect("autodoc-skip-member", keep_call)


# -- Project information -----------------------------------------------------
project = 'SymFac'
copyright = '2021, LBNL'
author = 'Yu-Hang "Maxin" Tang'

# The full version, including alpha/beta/rc tags
release = funfact.__version__


# -- General configuration ---------------------------------------------------

master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'sphinx_materialdesign_theme'
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []


# -- Extension configuration -------------------------------------------------
