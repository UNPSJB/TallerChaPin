# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Taller ChaPin'
copyright = '2022, Matías Barea, Ramiro Canario'
author = 'Matías Barea, Ramiro Canario'

html_title = 'Documentación de Taller ChaPin'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_favicon = './_static/logos/favicon.png'
html_theme_options = {
    "light_logo": "logos/logo-light.png",
    "dark_logo": "logos/logo-dark.png",
}

extensions = ['rst2pdf.pdfbuilder']
pdf_documents = [('index', u'rst2pdf', u'Documentación de Taller ChaPin', u'Matías Barea, Ramiro Canario'),]
