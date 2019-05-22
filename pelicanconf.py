#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Miles Lucas'
SITENAME = 'Miles Lucas'
SITEURL = 'https://mileslucas.github.io'

PATH = 'content'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('Instagram', 'https://instagram.com/mileslucas_'),
          ('Twitter', 'https://twitter.com/mileslucas_'),)

DEFAULT_PAGINATION = 3

THEME = 'pelican-themes/Flex'

COPYRIGHT_YEAR = 2019

# AUTHORS_BIO = {
#   "mileslucas": {
#     "name": "Miles Lucas",
#     "cover": "",
#     "image": "",
#     "github": "mileslucas",
#     "gitlab": "mileslucas",
#     "location": "Iowa",
#     "bio": "An Iowan boy who got stuck looking up at the stars."
#   }
# }

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True