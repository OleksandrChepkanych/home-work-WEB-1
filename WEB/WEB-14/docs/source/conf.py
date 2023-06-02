import sys
import os

sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../..'))

project = 'Portal APP'
copyright = '2023, Olexandr'
author = 'Olexandr'


extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []


html_theme = 'nature'
html_static_path = ['_static']
