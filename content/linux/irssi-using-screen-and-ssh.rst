Irssi Using Screen And SSH
##########################
:desc: A basic irssi, screen, ssh setup
:date: 2008-12-30 19:14
:tags: irc, ssh

I know this concept sound simple. You SSH into a server and restore a
screen session running irssi. However, I wouldn't be writing about it if
I didn't have a way to make it more efficient.

I'll explain the benefits as we go along.

First we need to get you into your server. I suggest setting up a shared
key between you and your server. There's plenty of guides out there
about shared keys.

::

    ssh server.com

Once in your server you need to install irssi and screen.

sudo aptitude install irssi screen

Set up irssi however you would do it if you were setting if set it up on
your own system. After this you will need to grab some files I've
uploaded.

First make the directory structure

::

    mkdir -p ~/.irssi/scripts/autorun

notify.pl is a modified version that pops up nice little message bubbles
on your desktop. It can be downloaded using subversion from
http://code.google.com/p/irssi-libnotify/source/checkout or directly
from my site.

awayproxy.pl handles hilights when you are away. It's very well
commented and easy to follow.

screen\_away.pl handles your away status when you connect and disconnect
from screen.

::

    wget -O ~/.irssi/scripts/notify.pl http://michael.lustfield.net/files/uploads/notify.pl.txt
    wget -O ~/.irssi/scripts/awayproxy.pl http://scripts.irssi.org/scripts/awayproxy.pl
    wget -O ~/.irssi/scripts/screen_away.pl http://scripts.irssi.org/scripts/screen_away.pl

We'll make symbolic links to make these run on irssi startup.

::

    cd ~/.irssi/scripts/autorun
    ln -s ../notify.pl
    ln -s ../awayproxy.pl
    ln -s ../screen_away.pl

Now that you've setup everything on the server, it's time to start
things on your client. This is pretty much just a single command that
you can place in a menu item.

::

    rxvt -bg black -fg green -sr -T irssi -n irssi -e ssh server.com -Xt screen -aAdr -RR irssi irssi

I use rxvt since it loads incredibly fast and is light weight.

::

    rxvt - The terminal emulator I run
    -bg black - Makes the background black
    -fg green - Makes the text green
    -sr - Places the scrollbar on the right side
    -T irssi - Gives the window a title
    -n irssi - Gives the window a name
    -e - Everything after this is the command we're running in the terminal
    ssh - The command that we're running
    server.com - The server you're connecting to
    -Xt - Combined (order matters)
    -X - Enable X forwarding (for the notify.pl script)
    -t screen - The command we're running on the server after ssh connects
    -a - Include all capabilities possible in the session
    -A - Handles changing window sizes
    -dr - Reattach a session and if necessary detach it first
    -RR - Reattach a session and if necessary detach or create it
    irssi - The first occurance is the name we're giving this screen session
    irssi - The second occurance is the command we're running inside of screen

This is a VERY long command that we're running. Hopefully I explained
all the parts correctly and efficiently enough that you can use and
modify it to fit your exact needs.

Attachments:

|image0| `notify.pl`_

.. _notify.pl: /files/uploads/notify.pl
.. |image0| image:: /files/icons/text-plain.png
