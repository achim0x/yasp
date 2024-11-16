# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Customize to your source code location
sys.path.insert(0, os.path.abspath('../../src/yasp_dbHandler'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'YASP - Yet another Stock Performance Analysis'
copyright = '2024, Achim Brunner'
author = 'Achim Brunner'
release = 'V0.1.0'
version = release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',  # extension for python docstring
              'sphinx.ext.napoleon',  # extension to support google docstring style
              'sphinx_favicon',  # extension to support favicon for html output
              'sphinx.ext.viewcode',  # view code in documentation
              'sphinx.ext.autosummary',  # crawls python files to extract content
              'sphinxcontrib.plantuml',  # plantuml support
              'myst_parser',  # markdown support
              'sphinx.ext.todo']  # support todo lists

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Display todos by setting to True
todo_include_todos = True

# Add path to your local plantuml jar file here. Latest Version can be downloaded here:
# https://plantuml.com/de/download
plantuml = ['java', '-jar', 'C:/Program Files/doxygen/bin/plantuml.jar']

# myst settings
myst_heading_anchors = 3
myst_fence_as_directive = ["plantuml"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autosummary_generate = True  # Automatically generate summaries
napoleon_google_docstring = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = "_static/0xAB_800r.png"

html_theme_options = {
    'logo_only': False,
    'style_nav_header_background': '#0C2C40'
}

# Add favicon
favicons = [
    {"rel": "icon", "href": "favicon.ico", "type": "image/svg+xml"},
    {"rel": "icon", "sizes": "32x32", "href": "0xAB_32r.png", "type": "image/png"},
]
