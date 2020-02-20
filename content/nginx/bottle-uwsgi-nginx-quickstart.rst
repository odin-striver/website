Bottle + UWSGI + Nginx Quickstart
=================================
:desc: A basic setup with bottlepy and nginx
:date: 2013-08-06
:tags: bottle, nginx, uwsgi, python

Nginx is pretty sweet, that's a rather obvious statement from me. There are
already many nginx forks and contributions back to the original. I also happen
to have quite a spot in my heart for `Bottle`_. In my eyes, it's a framework
that pretty much lets you forget you're working with the web. You get to write
your application as if the web didn't exist and then tack on the templating.

.. _`Bottle`: http://bottlepy.org/docs/dev/

Maybe it's not *that* easy, but it's worth checking out! I'm going to take you
through the process of getting this amazing stack going. Let's get started!

Installing Stuff
~~~~~~~~~~~~~~~~

I'm going to be assuming the use of Debian. It's easy enough to adjust.

::

    aptitude install uwsgi uwsgi-plugin-python python-bottle nginx

Your First Bottle Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I tend to start with a basic structure::

    /var/www/webapp/
        plugins/
            __init__.py
        static/
            css/
            files/
            images/
            js/
        views/
            base.tpl
            page.tpl
        app.py

Whether I have anything in the directories or not, they exist. It's just how I
make sure I keep things consistent across applications.

A basic skeleton of app.py will look something like this:

.. code-block:: python

    #!/usr/bin/python
    '''
    A basic bottle app skeleton
    '''

    import bottle

    app = application = bottle.Bottle()

    @app.route('/static/<filename:path>')
    def static(filename):
        '''
        Serve static files
        '''
        return bottle.static_file(filename, root='./static')

    @app.route('/')
    def show_index():
        '''
        The front "index" page
        '''
        return 'Hello'

    @app.route('/page/<page_name>')
    def show_page(page_name):
        '''
        Return a page that has been rendered using a template
        '''
        return template('page', page_name=page_name)

    class StripPathMiddleware(object):
        '''
        Get that slash out of the request
        '''
        def __init__(self, a):
            self.a = a
        def __call__(self, e, h):
            e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
            return self.a(e, h)

    if __name__ == '__main__':
        bottle.run(app=StripPathMiddleware(app),
            server='python_server',
            host='0.0.0.0',
            port=8080)

I realize there's a bit going on here, but it's not a minimal skeleton. This
shows you how to serve static content, a basic text only front page, and a
templated page. While you're testing, you don't want that slash unless the main
page is being requested. Browsers seem to like adding that. It's not an issue
when we get to deployment because uwsgi will take car of that for you.

Notice that bottle.run() only happens when you run app.py. It won't run when
you launch it as an application with uwsgi. This chunk is also the only place
that we call StripPathMiddleware. If you have no need for development, then you
can remove the last two chunks of code.

Try it out!::

    python app.py

You'll see the application start running. Go to example.com:8080/. Neat, huh?

The Templating System
~~~~~~~~~~~~~~~~~~~~~

Bottle has a bunch of templating options. For now, we're only going to touch
the most basic option.

views/page.tpl::

    You are visiting {{page_name}}!
    %rebase base

views/base.tpl:

.. code-block:: html

    <!DOCTYPE html>
    <html lang="en" dir="ltr">
        <head>
            <title>My Site!</title>
        </head>
        <body>
            <div id="pagebody">
                %include
            </div>
        </body>
    </html>

This is obviously *very* basic, but it will get you started. Check out the
`Bottle Docs`_ for more information. The templating options are endless!

.. _`Bottle Docs`: http://bottle.readthedocs.org/en/latest/

Now that you have this done, restart app.py and visit example.com:8080/page/foo.
You should be seeing a rather blank looking page that says "You are visiting
foo" with the title "My Site!"

Adding UWSGI
~~~~~~~~~~~~

Now that we have a very basic bottle application, it's time to fit it into the
stack. The built in web server that bottle offers is very slow. It's for
development only. Don't ever expect to use it in production.

::

    app = application = bottle.Bottle()

This little gem is more magic than you think. Don't forget it!

The UWSGI configuration is pretty simple. See the `UWSGI Docs`_ for more
details information.

.. _`UWSGI Docs`: http://projects.unbit.it/uwsgi

Edit /etc/uwsgi/apps-available/bottle.ini:

.. code-block:: ini

    [uwsgi]
    socket = /run/uwsgi/app/bottle/socket
    chdir = /var/www/bottle
    master = true
    plugins = python
    file = app.py
    uid = www-data
    gid = www-data

Then add a symlink from apps-enabled::

    ln -s /etc/uwsgi/apps-available/bottle.ini /etc/uwsgi/apps-enabled/bottle.ini

And restart the service::

    service uwsgi restart

At this point you'll see a socket file created at /run/uwsgi-bottle.socket.
That's great, but we need to actually make use of it.

Adding Nginx
~~~~~~~~~~~~

I prefer using the conf.d/ directory for my configurations. You can do as you
wish on your server.

Edit /etc/nginx/conf.d/bottle.conf:

.. code-block:: nginx

    upstream _bottle {
        server unix:/run/uwsgi/app/bottle/socket;
    }

    server {
        listen [::]:80;
        listen 80;
        server_name deb.ngx.cc;
        root /var/www/bottle;

        location / {
            try_files $uri @uwsgi;
        }

        location @uwsgi {
            include uwsgi_params;
            uwsgi_pass _bottle;
        }
    }

In our bottle application, we defined a route for static content. However, it's
better to have nignx serve this data so that we can avoid making python do any
work. That's why we use try_files in the location block. You want that in your
bottle application for development, but when we deploy, it won't actually get
used.

Then restart the service::

    service nginx restart

You'll now be able to access your bottle application from the internet through
nginx.

Final Thoughts
~~~~~~~~~~~~~~

This was a very brief tutorial. It's meant only to get you jump started into
having a usable bottle+uwsgi+nginx stack that you can expand on to fit your
environment/needs. If you feel any parts need additional explanation, please
let me know!
