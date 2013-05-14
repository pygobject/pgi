# -*- coding: utf-8 -*-

import sys, os

sys.path.insert(0, os.path.abspath('../pgi/'))
import const

source_suffix = '.rst'
master_doc = 'index'
project = u'PGI'
copyright = u'2013, Christoph Reiter'
version_tuple = const.VERSION
if version_tuple[-1] == -1:
    version_tuple = version_tuple[:-1]
version = '.'.join(map(str, version_tuple))
release = version
exclude_patterns = ['_html', '_latex']
pygments_style = 'tango'
html_theme = 'pyramid'

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
}

latex_documents = [
    ('index', 'pgi.tex', project, '', 'howto'),
]
