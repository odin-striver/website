#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'michael'
SITENAME = u'Michael Lustfield'
SITEURL = 'https://michael.lustfield.net'
PATH = 'content'
WITH_FUTURE_DATES = False
RELATIVE_URLS = False
TIMEZONE = 'America/Chicago'
DEFAULT_LANG = u'en'
TYPOGRIFY = False
THEME = './theme'

FEED_RSS = 'rss.xml'
CATEGORY_FEED_RSS = '{slug}/rss.xml'
CATEGORY_FEED_ATOM = None

PAGE_URL = 'pages/{slug}'
CATEGORY_URL = 'category/{slug}'
ARTICLE_URL = '{category}/{slug}'
ARTICLE_SAVE_AS = '{category}/{slug}.html'

GOOGLE_ANALYTICS = '252297868'

STATIC_PATHS = ['CNAME', 'files']

#PLUGINS = ['sitemap', 'gzip_cache', 'sphinxsearch']
PLUGIN_PATHS = ['./plugins']
#TEMPLATE_PAGES = {'search_base.html': 'search_base.html'}
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 1.0,
        'indexes': 0.5,
        'pages': 0.6
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'weekly',
        'pages': 'monthly'
    }
}

DEFAULT_PAGINATION = 10

FOOTER = 'MTecknology - <a href="/pages/keeping-it-dry">Keeping IT DRY</a><br />[<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">license</a>]'
