Blog With Pelican and Nginx
===========================
:desc: Setting up an elegant blog using pelican and nginx
:date: 2013-08-08
:tags: nginx, pelican, blog

I used to be a big lover of Drupal as a blogging platform. It's incredibly easy
and trivial to deploy a new site with it and it comes with everything needed to
write a blog. It's also incredibly easy to extend and with little work the whole
SEO buzz stuff is pretty much already there. I've found that Wordpress makes it
pretty hard for search engines to handle your content, but it is almost strictly
a blogging platform.

I've come to the realization that working on these platforms is just a pain in
the bum. I don't want to have to go out to a website, even if my own, to write
the the entry. Sure, you can load up an editor and write it in there, but that's
just another hassle.

On top of that, when any page is accessed, the platform has to render that page
which is usually rather slow because it has to grab everything from a database
and then assemble it. Adding cache can help substantially, but it's still not
usually all that fast.

So, I don't like these platforms anymore. As much as I was sold on them in the
past, I just can't justify them anymore. Well, if I don't want to render the
pages with every request and caching isn't enough, there's always static
content.

Static content is great because it's fast. However, if you're creating all of
the content by hand, you get to repeat yourself rather frequently. You get to
make sure all your pages stay in sync. Yuck!

In Comes Pelican
~~~~~~~~~~~~~~~~

Pelican is a python application that's rather neat. You get to write your blog
content with restructuredtext or markdown. You have to set it up initially, but
once you're done, you can just keep writing away and never worry about what's
actually rendered. There's not really much to it. The best part is that because
of how it works, you can use plugins to generate pre-gzipped pages and serve
those when the browser will accept gzip encoding.


Getting Started
~~~~~~~~~~~~~~~

I'm going to explain how I utilize pelican for the very blog that you're reading
right now.


First, you need to install pelican.

::

    aptitude install python-pelican

If you're still with me, then great! You should have no troubles with the rest!

Next up, the directory structure::

    mkdir -p /var/www/myblog/{content,plugins}
    touch /var/www/myblog/plugins/__init__.py

Followed by getting some themes others have contributed::

    git clone https://github.com/getpelican/pelican-themes.git /var/www/myblog/themes

We'll follow that by grabbing two plugins that I personally find mandatory::

    wget https://raw.github.com/getpelican/pelican-plugins/master/sitemap/sitemap.py -O /var/www/myblog/plugins/sitemap.py
    wget https://github.com/getpelican/pelican-plugins/blob/master/gzip_cache/gzip_cache.py -O /var/www/myblog/plugins/gzip_cache.py

Now we need to write a configuration file.

vim /var/www/myblog/pelicanconf.py

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*- #
    from __future__ import unicode_literals

    AUTHOR = u'michael'
    SITENAME = u'Michael Lustfield'
    SITEURL = 'http://michael.lustfield.net'
    PAGE_DIR = 'content/pages'
    WITH_FUTURE_DATES = False
    RELATIVE_URLS = False
    TIMEZONE = 'America/Chicago'
    DEFAULT_LANG = u'en'
    TYPOGRIFY = False
    THEME = './themes/syte'

    FEED_RSS = 'rss.xml'
    CATEGORY_FEED_RSS = '%s/rss.xml'
    CATEGORY_FEED_ATOM = None

    ARTICLE_URL = '{category}/{slug}'
    ARTICLE_SAVE_AS = '{category}/{slug}.htm'

    GOOGLE_ANALYTICS = '< YOUR GA CODE >'

    PLUGINS=['plugins.sitemap', 'plugins.gzip_cache']
    SITEMAP = {
        'format': 'xml',
        'priorities': {
            'articles': 0.5,
            'indexes': 0.5,
            'pages': 0.5
        },
        'changefreqs': {
            'articles': 'monthly',
            'indexes': 'daily',
            'pages': 'monthly'
        }
    }

    DEFAULT_PAGINATION = 10

This is almost the exact configuration I use for my blog. I use a different
theme and have the GOOGLE_ANALYTICS variable filled in. Beyond that, this is it.

Some notes about this...

* The content will generate links without the .htm
* The pages will be generated with the .htm extension
* There is a subdirectory created for each category
* All the posts in that category wind up under that directory
* There is an rss.xml file generated under each subdirectory for that category
* There is still an /rss.xml file generated
* The "slug" (name of the file without the extension) will be used for the URI

I choose to put .htm files on the file system because that makes sense. However,
it doesn't let me use pretty permalinks. I don't want .html in every request.
When we get to the nginx part, we'll tell it to see if the requested file exists
on the file system with either .htm or .html extension first.

Writing Content
~~~~~~~~~~~~~~~

A blog is useless without content. The Pelican docs have a `Getting Started`_
page that explains writing content. I'm just going to go through the basics.

.. _`Getting Started`: http://docs.getpelican.com/en/3.2/getting_started.html#writing-content-using-pelican

Figure out the categories you want. These should be generic and sensible. For
my blog, I have linux, nginx, rambling, and misc. You should always have a
misc category, even if it's not used. You'll also want a directory for pages
that aren't part of your blog.

So...

::

    mkdir /var/www/myblog/content/{linux,nginx,rambling,misc,pages}

So, let's say we want to write a blog about Linux and grafiti.

::

    vim /var/www/myblog/content/linux/linux-and-grafiti.rst

Yay, we're now writing a blog post in the linux category about linux and
grafiti. The blog entry will look like this:

.. code-block:: restructuredtext

    Linux, Grafiti, and You
    =======================
    :date: 2013-12-05
    :tags: linux, grafiti

    Some content written with restructuredtext...

That's all there is to writing content! Se the `Getting Started`_ page in the
Pelican docs to get further details.

Publishing Content
~~~~~~~~~~~~~~~~~~

Run the command::

    pelican -s /var/www/myblog/pelicanconf.py

and your content will be generated in output/.

Want to update your content? It's the same command. You can put that in a
cron task if you like. If you put it in cron, you'll probably want to add the
-q flag as well.

Making Nginx Serve Content
~~~~~~~~~~~~~~~~~~~~~~~~~~

First, we need to install Nginx::

    aptitude install nginx-light

If you have a default server block, it's only there as an example. Feel free to
get rid of it::

    rm /etc/nginx/sites-enabled/default

Now we need to write a configuration file for the blog.

vim /etc/nginx/conf.d/myblog.conf:

.. code-block:: nginx

    server {
        
        listen [::]:80;
        listen 80;

        server_name example.com;
        root /var/www/myblog/output;

        location = / {
            # Instead of handling the index, just
            # rewrite / to /index.html
            rewrite ^ /index.html;
        }

        location / {
            # Serve a .gz version if it exists
            gzip_static on;
            # Try to serve the clean url version first
            try_files $uri.htm $uri.html $uri =404;
        }

        location = /favicon.ico {
            # This never changes, so don't let it expire
            expires max;
        }

        location ^~ /theme {
            # This content should very rarely, if ever, change
            expires 1y;
        }
    }

The gzip_static directive tells nginx that if the file should be served gzipped
that we may, and do, have the file already gzipped and to use that instead. It
means that nginx doesn't need to use any extra CPU to serve gzipped data.

From above, we generate links without the .htm extension, but we generate the
files with them. That's just a way to make the request pretty. Our try_files
directive makes it possible to do that.

Go ahead and restart nginx::

    service nginx restart

Go check out your new blog! It's all static content and serving it is fast. :D
