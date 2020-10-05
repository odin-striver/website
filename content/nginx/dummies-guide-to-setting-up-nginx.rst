Dummies Guide to Setting Up Nginx
#################################
:desc: An introduction to the basics of nginx
:date: 2011-07-25 02:41
:tags: nginx, administration

Nginx is one of those things that many people want to try but don't.
Why? Because it's scary. Well... Nginx itself isn't scary, but all of
the poor guides out there make it a nightmare. The first step in making
Nginx work for you is to not follow 95% of the guides found on Google.
That sounds backward from what you usually hear and I do hate giving
that advice. While many of the guides out there will get you going most
of the time in most situations, they tend to be suboptimal. Many of
these configurations tend to focus on reproducing how Apache does
things. Fortunately, they are not the same thing and are in fact quite
different. Even the guide in the Linode Library will yield poor results
(which is uncommon for them).

So where should you go for help? Kind of easy actually. Nginx has a
fantastic wiki for most of your questions at http://wiki.nginx.org/.
There is an Nginx support channel (#nginx on irc.freenode.net) as well.
Once you know what tends to be wrong in most examples you'll be able to
start using Google. The reason being that most of the advanced stuff you
find floating around is usually pretty solid. The issue is just that
people get so excited by Nginx that when they see it's power they want
to say something before they fully understand what's going on.

My aim here isn't to provide a dead simple solution for everything you
will ever want to do with Nginx. Consider this more like a guide to the
basics. Let's get started.

I use Debian and Ubuntu, you may have to alter things to fit your
distribution.

Installing Stuff
~~~~~~~~~~~~~~~~

A very common use case for web servers is PHP based Content Management
Systems. A majority of the time, people settle on MySQL as their
database. I'll also assume you want a self managed PHP system as you
would get in Apache with mod\_php. Do you also want the latest and
greatest version of Nginx and PHP?

If your distribution does not have php5-fpm as an available package
(think pre-ubuntu\_11.04) you will want the new stuff. This is in a nice
spiffy Personal Package Archive (PPA) which is maintained by the Nginx
community. To add these PPA's for the latest and greatest:

::

    aptitude install python-software-properties
    add-apt-repository ppa:nginx/stable
    echo 'deb http://packages.dotdeb.org squeeze all' >> /etc/apt/sources.list
    wget http://www.dotdeb.org/dotdeb.gpg -O- | sudo apt-key add -
    aptitude update

Note: If you'd like to use only PHP5 from dotdeb, which is probably a
good idea, then copy the preferences.txt attachment to
/etc/apt/preferences. This will make dotdeb the lowest priority except
for php5\* which will be the highest priority.

GREAT! Access to some super neat stuff. Let's get it all installed!

aptitude install nginx-light mysql-server php5-mysql php5-fpm php-apc

You'll get asked for a root password for MySQL. Pick something secure
and don't forget it. At this point you have everything installed that
you need. You just don't have it configured yet. We don't \_have\_ to
stop these services while we're working on them but we should.

::

    /etc/init.d/php5-fpm stop
    /etc/init.d/mysql stop
    /etc/init.d/nginx stop

Configuring Stuff
~~~~~~~~~~~~~~~~~

We may as well start with MySQL since it's the easiest. Edit the file
/etc/mysql/my.cnf. Add this stuff to the very bottom.

::

    default-storage-engine = innodb
    innodb_buffer_pool_size = 128M
    innodb_log_file_size = 10M # May need to purge (rm)
    /var/lib/mysql/ib_logfile*
    innodb_flush_method = O_DIRECT
    innodb_file_per_table = 1
    innodb_flush_log_at_trx_commit = 2
    innodb_log_buffer_size = 1M
    innodb_additional_mem_pool_size = 20M
    # num cpu's/cores x2 is a good base line for
    innodb_thread_concurrency
    innodb_thread_concurrency = 8
    innodb_open_files = 1024
    ignore-builtin-innodb
    innodb_file_per_table
    plugin-load=innodb=ha_innodb_plugin.so;innodb_trx=ha_innodb_plugin.so;innodb_locks=ha_innodb_plugin.so;innodb_lock_waits=ha_innodb_plugin.so;innodb_cmp=ha_innodb_plugin.so;innodb_cmp_reset=ha_innodb_plugin.so;innodb_cmpmem=ha_innodb_plugin.so;innodb_cmpmem_reset=ha_innodb_plugin.so

I'd rather not go into detail about each piece here. I'll sum it up this
way... It won't save you any RAM. In fact, this will use additional RAM.
It will, however, make thing faster and more efficient. It's kind of a
"MySQL Magic Sauce" I cooked up over some time that I have yet to find
issues with.

Now for that PHP tuning. PHP-FPM works great out of the box. However,
it's configured with defaults that are a little less than optimal. For
starters, it uses a TCP socket as opposed to a UNIX socket. The TCP
socket is more universal, but not more efficient. It is also configured
to use dynamic processes which are not ideal either. Lastly, it is setup
with huge amounts of RAM allocated to each PHP process. This is fine
consiering all of the horribly inefficent PHP apps out there. If you're
running something sane, then it's just crazy. Below, I included the
lines that I changed in /etc/php5/fpm/pool.d/www.conf.

::

    listen = /var/run/php5-fpm.sock
    listen.allowed_clients = 127.0.0.1
    listen.owner = www-data
    listen.group = www-data
    listen.mode = 0660
    user = www-data
    group = www-data
    pm = static
    pm.max_children = 10
    pm.max_requests = 1000
    php_admin_value[memory_limit] = 32M

Now, we move onto Nginx configuration. The best part of this is that the
most common cases already have templates for you. The default install
comes with a default configuration file in /etc/nginx/sites-enabled/.
Quite simply, this file should just be deleted if you have a clue what
you're doing. It's useful because it's loaded with comments, examples,
and links.

I personally prefer keeping site configs in /etc/nginx/conf.d/<site>.conf.
Others prefer keeping configs in /etc/nginx/sites-available/ and then
creating a symlink to it from /etc/nginx/sites-enabled/. Either option
yields the exact same result. The only thing you should not do is keep
everything in the same file. It creates a maintenance nightmare.

Let's say you're wanting to run a Drupal and you unpacked into
/var/www/drupal/. Go to http://wiki.nginx.org/Drupal. Copy/paste that
configuration example to your configuration file. Edit the line that
says 'root /var/www/drupal6;' and point it to where you unpacked Drupal
(/var/www/drupal). You will also want to edit the line that says
'server\_name domain.tld;'. This should be the domain name that will be
used to access your site.

Well... Let's see....

We installed the packages, configured them, tuned a few things, grabbed
the source for a CMS, set it up, ect. What now? Let's fire it all up.

::

    /etc/init.d/php5-fpm start
    /etc/init.d/mysql start
    /etc/init.d/nginx start

Of course you still need to create a database and user to access that
database as well as configure your CMS or whatever it may be. This
should give you an excellent start to your server.

Further reading can be found on the Nginx Wiki. You definitely want to
check out this resource before consulting other resources.

* http://wiki.nginx.org/Pitfalls
* http://wiki.nginx.org/Configuration

My server is a Linode VPS. I use their smallest plan because I can't peg
the resources it offers.

My advertisement... My VPS provider of choice has become `Linode`_. The smallest
option is more than powerful enough for running this blog, multiple irssi
sessions, and my development environment. If you use my referral link and remain
an active customer, I get a small bonus.

Attachments:

|image0| `preferences.txt`_

.. _Linode: https://www.linode.com/?r=f29487efde244dc3e6af5c243803d9aef307e013
.. _preferences.txt: /files/uploads/preferences.txt

.. |image0| image:: /files/icons/text-plain.png
