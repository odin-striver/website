Simple IP Echo
##############
:desc: A nice and simple whatismyip service with nginx
:date: 2010-10-31 09:18
:tags: nginx

OK! We all know Nginx is amazing and extremely light. I've been having
the need lately to quickly get the IP address of a location. There's
"whatismyip.com" but that's an ugly bloat. Look at how much you download
to just get a small string of numbers.

To get around this a lot of people run their own website that displays
the IP address. This is usually done by passing the connection from
Apache to HTTP which has code similar to the following in it.

.. code-block:: nginx

    <?php
    print(getenv(REMOTE_ADDR))
    ;?>

That seems simple and light enough. Why add PHP into the mix though.
It's very much so an added bloat. Apache is enough of a bloat without
adding the extra bloat of PHP.

Let's use a real web server and just let the web server do it. The
following is my Nginx configuration file.

.. code-block:: nginx

    server {
        server_name ip.lustfield.net;
        location = / {
            default_type text/plain;
            echo $remote_addr;
        }
    }

I don't think there's a single possible way to get a faster and more
light weight response. Nginx doesn't do any processing aside from seeing
that it's right domain and returning the remote address as plain text.

It's just SO simple and SO pretty.
