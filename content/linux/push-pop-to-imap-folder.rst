Push POP to IMAP Folder
#######################
:desc: Getting POP email pushed to a specific folder on an IMAP server
:date: 2008-12-30 19:10
:tags: email

This is for anybody with multiple email accounts that wants to
consolidate. My solution here requires and number of POP email accounts
and one IMAP account.

I don't even want to begin thinking about the time it took me to come up
with this solution. Hopefully it can save somebody 10 or more hours of
digging and scripting.

My method works like this.

1. Synchronize IMAP account with local Maildir copy
#. Download POP emails
#. Push emails to Maildir local copy
#. Synchronize local Maildir copy with IMAP account

The first synchronization is to prevent any little issues that could pop
up.

First and foremost, I assume you are working on a Linux system. No
exceptions. I also assume a system that uses Apt.

You'll need to install a couple tools that are most likely not installed
by default.

sudo aptitude install getmail4 procmail offlineimap

I did my best to keep everything in a nice central directory which you
need to create as well.

::

    mkdir ~/.synmail

The first thing we need to do is create a file in here called pushmail.
Rather than showing you all the text, you can just download this script.
It's attached as pushmail at the bottom of this post. Download it to
~/.synmail/pushmail You will need to make sure it's executable as well.
Just a note, make sure there is no period on the end.

::

    chmod +x ~/.synmail/pushmail

The first file our pushmail script will use is for offlineimap. In order
for this application to work, we need to create our very own IMAP
directory.

::

    mkdir ~/.synmail/imap

Now we need to create the offlineimap configuration file.

::

    vim ~/.synmail/offlineimap.conf

Rather than go through all the details of setting this up, I just
uploaded my copy. It is listed as offlineimap.conf. There isn't puch
point in discussing all the various options because there is an
excellent fully commented explation of everything sitting on your
computer. Just follow these commands to get the copy.

::

    cp /usr/share/doc/offlineimap/examples/offlineimap.conf.gz ~/
    gunzip ~/offlineimap.conf.gz

The next file our pushmail script needs is the getmail file. Our script
expects this file in a very specific way. It's basically just
prefix-getm. I have two gmail accounts so I use gm1-getm and gm2-getm. I
uploaded a copy of my gm1-getm file. The values should make sense. If
they don't you shouldn't be reading this. This file goes to
~/.synmail/gm1-getm

The only line that might be confusing is the arguments line. The reason
we have the " " added in is because of the way parameters are passed to
procmail. This caused me a lot of headaches and you're probably better
off leaving it alone. The next part is the path to your procmail
configuration.

Now that we're on that page, it's time to talk about our procmail
configuration. This file will have the same prefix as the one before it.
I obviously called mine gm1-proc. Go figure, I uploaded my copy. Not
only that, but I didn't have to hide passwords or anything. That's
because this file is ONLY a delivery agent.

When you look at this file, notice that there is a line called DEFAULT.
This line is the reason we need different configurations for each
account. That "FODLER" part at the end is what folder our files will be
going into. Unfortunately, we can't leave it at that. Because of the way
Maildir works, we need to add the /new at the end. I'm not saying
Maildir sucks, and it really doesn't make this any harder.

I probably don't need to note that you need to save this file just like
the getmail configuration. Mine is at ~/.synmail/gm1-proc.

Hurray, we now should have everything in place that we need to in order
to run this setup successfully. You've probably noticed that our
passwords show up a couple times. I don't like it either. We can have a
password input file and a few other methods to keep things secure, but
none of it is really worth it. Instead, I just like to make it readable
and writable to only my user. Not only do I suggest it, it's in the
script you got from me.

Keep It Private:

::

    chmod +x 0700 $HOME/.synmail

Now that we have that cleared up, it's time to test this puppy out. I
have been using the prefix gm1, replace gm1 with whatever you have been
using.

::

    cd $HOME/.synmail/
    ./pushmail gm1

The rest will be done for you. What happens is that the script takes
your prefix input and uses this to find the other configuration files
you created. This is why you need to keep the prefix the same, and
follow my naming convention. If you don't like it, then the script is
yours, do with it whatever you want. I love open source.

When you're running this script, you will notice that it probably takes
an insanely long time to go through. You might say to yourself that
there's no way this is acceptable if it's going to happen every time.
However, after the first run you'll realize that in fact it was just
pulling down every single email you had on your IMAP server. If you look
at it closely enough, you'll find that there's more files around than
what you expected would be there.

So, you'll see offlineimap making a copy of the current state of your
IMAP data. Then you'll see getmail retrieving your POP emails. procmail
will be running behind the scenes to sort your mail. And then you'll see
offlineimap doing it's last sync with your newer emails going out to
your server.

BONUS: You can also use this local copy of your IMAP data if your IMAP
server is ever offline or you won't have internet access. I would
suggest being careful with it because of the nature of these scripts.

That's the primary intention of offlineimap in the first place.

BONUS 2: I've modified the pushmail script to be able to do ALL files in
the directory in one shot. PLEASE DO NOT run this before you've verified
ALL of your other settings work. Don't leave any extra -getm or -proc
files. If you looks at the script, it'll be obvious why.

Attachments:

|image0| `pushmail`_

|image0| `pushmail-all`_

|image0| `offlineimap.conf`_

|image0| `gm1-getm`_

|image0| `gm1-proc`_

.. _pushmail: /files/uploads/pushmail
.. _pushmail-all: /files/uploads/pushmail-all
.. _offlineimap.conf: /files/uploads/offlineimap.conf
.. _gm1-getm: /files/uploads/gm1-getm
.. _gm1-proc: /files/uploads/gm1-proc

.. |image0| image:: /files/icons/application-octet-stream.png
