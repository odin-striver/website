Getting a Perfect SSL Labs Score
################################
:desc: Obtaining a perfect ssllabs score
:date: 2015-01-19 16:45
:tags: nginx, ssl, ssllabs, tls

|ssllabs_100.png|

Running web servers is both fun and infuriating. We get to do some really neat
and fun things, sure. We also have an ever changing battlefield. When we sleep,
the other guys are wide awake. Keeping a web server secure is tough.

Just one of the many battles in this war is SSL. If you have a website that
either provides or accepts private data, you /should/ already know that SSL is
not an option, it's a requirement. I say should because that's proven to not be
an obvious fact.

If you're on this page, then you know that you need or want SSL and are looking
for the best configuration settings. Congratulations, I already like you better.

Obviously, I'll only be discussing Nginx since it's the only real web server. ;)

Certificate
-----------

This section is easy to get 100% on.

* Make sure your cert and chain are in the correct order.
* Don't use SHA1 (use SHA256) for the signature algorithm.
* Use a well known/trusted CA.

SSL Labs is pretty good about being descriptive about any issues here.

Protocol Support
----------------

The best place to start with securing your website is protocol support. It's a
given that you shouldn't be using SSLv2. It should also be a given that you
should no longer be using SSLv3. The recent POODLE vulnerability pretty much put
the final knife in it.

This means you should only support the TLS protocols.

.. code-block:: nginx

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

This is reasonably secure. However, we want a "perfect" score. This will give
you a score of 95. Disabling TLSv1.0 gives you a 97. Disabling TLSv1.1 gives you
that last bit to 100.

So, if you want a perfect score, you'll use this.

.. code-block:: nginx

    ssl_protocols TLSv1.2;

Key Exchange
------------

By default, Nginx will use the default DHE (Ephemeral Diffie-Hellman) paramaters
provided by openssl. This uses a weak key that gets lower scores. The best thing
to do is build your own. You can create a 2048 bit key, but let's go ahead and
toss 4096 at it.

First, you need to build the file. I'm going to assume you keep SSL files in
/etc/nginx/ssl.

::

    openssl dhparam -out /etc/nginx/ssl/dhparam.pem 4096

Then in your Nginx configuration, you'll need this.

.. code-block:: nginx

    ssl_dhparam ssl/dhparam.pem;

Cipher Strength
---------------

This one especially is ever changing. What's best today, may not be so hot
tomorrow. Here, you'll have a battle between high security and compatibility.
Keeping with the topic of this post, we care about security only.

.. code-block:: nginx

    ssl_ciphers AES256+EECDH:AES256+EDH:!aNULL;
    ssl_prefer_server_ciphers on;

SSL Stapling
------------

SSL Stapling doesn't exactly make you any more secure, but it does help the
client significantly. In short, you help the client by telling them they can
use your server for OCSP information for your domain instead of letting the
browser make the request to an often unreliable resource.

.. code-block:: nginx

    ssl_stapling on;
    ssl_stapling_verify on;

SSL Sessions
------------

Maintaining SSL Sessions is definitely a good thing for everyone if you expect
the user to be on your website for more than a single page view. These are
rather trivial settings.

.. code-block:: nginx

    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

Extra: ssl_ecdh_curve
---------------------

It turns out, some openssl implementations don't provide a nice default for nginx
to inherit, so it becomes a good idea to specify this manually. (Thanks James
from Penn State)

.. code-block:: nginx

    ssl_ecdh_curve secp384r1;

It has been suggested x25519 is a more secure but slightly less compatible option.

HTTP Headers
------------

We'll also want to add a few headers.

.. code-block:: nginx

    add_header Strict-Transport-Security "max-age=31536000; includeSubdomains";
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;

They don't help you're score, but they're quite helpful.

Gzip
----

Some attacks are possible because of gzip being enabled on SSL requests. In
most cases, the best action is to simply disable gzip for SSL requests.

SSL Blocks:

.. code-block:: nginx

    gzip off;

Putting it Together
-------------------

The command to run::

    openssl dhparam -out /etc/nginx/ssl/dhparam.pem 4096

The Nginx configuration:

.. code-block:: nginx

    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_protocols TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_ciphers AES256+EECDH:AES256+EDH:!aNULL;
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_dhparam ssl/dhparam.pem;
    ssl_ecdh_curve secp384r1;

    add_header Strict-Transport-Security "max-age=31536000; includeSubdomains";
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;

In any server block listening for SSL:

.. code-block:: nginx

    server {
        listen 443 ssl;
        # gzip should not be used with ssl
        gzip off;
    }

It's not hard once you know the super-duper magic sauce. Just remember that you
are sacrificing compatibility for the sake of security. Enjoy!

.. |ssllabs_100.png| image:: /files/uploads/ssllabs_100.png
 :width: 100%
