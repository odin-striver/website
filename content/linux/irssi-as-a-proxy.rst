Irssi As A Proxy
################
:desc: Using Irssi as an IRC proxy
:date: 2008-12-30 19:13
:tags: irc

Irssi has a fairly nice proxy feature. It's probably the best proxy I've
ever used. Unfortunately, it has a few flaws and is very under
documented.

I gave up on ever having a decent proxy and switched to the screen
option but I still want to explain this feature so it's decently
documented somewhere.

To setup the server you need to first install irssi and screen. Edit
your configuration the same as you normally would to connect to any
other server.

You want to proxy to load my default so edit ~/.irssi/startup and add
the line "/LOAD PROXY".

You can either edit the configuration file yourself IF you know what
you're doing or you can use the commands to do it. People seem to screw
this up a lot so I won't show it. The irssi group seem to advise against
as well.

Set a password with

::

    /SET irssiproxy_password PASSWORD

You need to set a different port for each network in the configuration.

::

    /SET irssiproxy_ports Freenode=7001 Bitlbee=7002

You need to make sure to save the settings.

::

    /SAVE ALL

Create a directory called scripts and then autorun underneath it.

::

    mkdir -p ~/.irssi/scripts/autorun

Put the `awayproxy.pl`_ and `proxy\_backlog.pl`_ scripts in the scripts
directory. You want to make these run at launch time so just make a
symlink to them in the autorun.

::

    cd ~/.irssi/scripts/autorun
    ln -s ../awayproxy.pl
    ln -s ../proxy\_backlog.pl

Edit the awayproxy file. It's very well commented. The other file is a
drop in tool. It's not pretty or elegant, but it fixes the fact that
irssi proxy doesn't have a backlog viewer available.

Now you need to setup a task to launch this on your server. We'll add
this to the boot process. Edit /etc/rc.local

Add this line replacing USER with your user name.

::

    sudo -H -u USER screen -d -m -S irssi-proxy irssi

Breaking down the command

::

    sudo ; runs command as user
    -H ; sets the home directory to the users
    -u ; sets the command to act as USER
    screen ; the command sudo is executing
    -d -m ; starts screen detached. This solves a lot of issues later.
    -S ; starts the screen session with the irssi-proxy ID.
    irssi ; the command we're launching

If you want to connect to this screen session from your server to see if
the proxy connection is missing something - like PM's - just log in and
do "``screen -r irssi-proxy``" That big long command that we did made it
possible to only need that little line to connect.

What did you say? You want to connect to it now? I'm afraid that's
beyond the scope of this.... :P

On your client. Create an alias command. I used

::

    BL = "CTCP -proxy- IRSSIPROXY BACKLOG SEND";

We need to create a network

::

    /NETWORK ADD Proxy

Then add a server to it

::

    /SERVER ADD -auto -network Proxy proxy.server.com 7001 PASSWORD

- Remember that you have different ports for each proxy network

Make sure to save the settings

::

    /SAVE ALL

-----

Hurray, all should be set up and well. Just run irssi on your local
system and it should connect to the proxy.

If it isn't working for you just comment a request for help or email me
and I'll be glad to help you.

If you need help I'd suggest finding some place other than their
channel. It tends to be full of RTFM ass holes and pricks. Especially
when you ask something they don't know the answer to. It's best to find
another channel of people that use it and just ask there instead.

.. _awayproxy.pl: http://scripts.irssi.org/scripts/awayproxy.pl
.. _proxy\_backlog.pl: http://wouter.coekaerts.be/irssi/scripts/proxy_backlog.pl
