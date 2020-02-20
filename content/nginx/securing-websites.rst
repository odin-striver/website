Securing Websites
#################
:desc: An attempt to make php less broken
:date: 2010-08-11 22:19
:tags: websites, nginx, php, overkill

Building a secure setup is extremely hard. There's an old saying that's
basically "build an idiot-proof system and the world will build a better
idiot." That works two ways. If you build a hacker-proof system then
you'll find better hackers. Loosely defined use of the term hacker of
course.

So, how does one make a secure web server. The easiest would be to use
something like Nginx and server only static content with hundreds of
layers of strong security to get to altering those files with only one
fully trustworthy person able to pass through all of the layers and a
system of ensuring only correct content exists with no possible local
access.

Moving over to the real world, I came up with my own system. For
starters, my company operates on a limited budget. Most of our servers
operate on 1.5GB RAM or less. We only have one system with more, and
it's not our production system.

My company does Drupal / Pressflow website development and hosting as
well as graphic design. This means we use PHP. The problem is that PHP
has exec(). You can forbid the use of this but what you end up with is a
few things that won't work. In our case, it's Drush. That's irritating
enough by itself. If a person can touch your source code you basically
need to assume they can run anything on the shell.

Fighting this is in some ways trivial and in some ways not. The simple
is the concept that all you need to do is restrict what the user account
can do and touch. The part that's not trivial is everything else. You
need to consider how the user will be separated from the system and how you
will interact with that users data.

My solution came in a few ways. The first step is to not allow PHP to
execute exec(). That one still bites but I definitely need to do it. The
next was file system permissions. I don't care if anyone can read static
content, but I don't want them reading PHP of other users. Partly
because this includes settings.

The solution here was to lock down home directory permissions. I run one
instance of PHP for each website as the user that owns the website. Of
source that's bound to a socket. I also include a periodic script that
rechecks permissions to make sure a user didn't change them. Because
only that user can read any PHP data, the connection strings are locked
down pretty tight. One site broken into won't inherently mean access to
all websites.

Let's go back to the source here. Keeping a server secure means locking
down the users. I don't want them accessing 100's of commands and files
that they have no use for. Every additional application available,
there's an additional point of attack. So we need to eliminate this. You
can take the route of hardening the system beyond imagination and to the
point where your admin tasks suffer. This sounds icky to me.

My thought, is to simply put the users in a jail. What's the best way is
a hard question to ask. I went a few ways. The first part in the path I
took was using debootstrap to build a chroot environment. Trust me,
trimming down a larger environment is MUCH easier than building up a
barely functional bare bones system. You get a much smaller system this
way though.

I used debchroot and jailkit. The former is in the repositories but the
latter isn't. I loved this project so I setup some auto builds in
Launchpad. Check out the PPA in Launchpad `for jailkit`_.

If you want to build a very minimal system you can follow these
commands.

NOTE!! I found that a reboot after installing the package and after
running the basic commands can save you from having very severe issues.

::

    # Basic System
    mkdir /jailjk_init -v /jail
    basicshelljk_init -v /jail
    netutilsjk_init -v /jail
    sshjk_init -v /jail jk_lsh
    # Extras (add bash)
    jk_cp -v -f /jail $(which bash)
    # Extras (add su)
    jk_cp -v -f /jail $(which su)
    # Extras (add nano)
    jk_cp -v -f /jail $(which nano)

That looks amazingly easy, and it works. This issue is that it's too
minimal for doing most things. What I did was start with a chroot
bootstrap. Here's what I did BEFORE jk\_init.

::

    debootstrap lenny /jail

When that's done we want to strip it down.

::

    chroot /jailapt-get remove foo

It's really that simple. You can add applications the same way.

Now that you have your environment setup, you need to move users into
it. This is just too easy. A caution would be to not move your own
account into this or you could lose access to the entire parent system.

::

    jk_jailuser -m -s /bin/bash -j /jail USER

This will move the user into the jail and setup their shell to am
application that will put them in the chroot when they log in. The -s
/bin/bash sets their shell inside of the chroot to bash. Otherwise they
get

a shell that basically forbids interactive logins. The -m moves their
home directory in the jail. Make sure they're not logged in when you do
this.

If you want more help, then look at `the guide`_ that I followed to
understand jailkit. There's even more help available at the `jailkit
website`_.

You can read the users data outside of the jail at /jail/home/user. Easy
enough. In fact, I just pointed my web server (nignx) at the new
location. This is pretty spiffy in that it's easy to do and really gives
you a more

secure system because the users have no direct access to the parent
system. If you really want to get mean you could set the users shell to
/bin/rbash inside of the jail. I don't really see the point though.

In my book, this is a much more secure setup. Nginx only reads static
content and PHP runs as the user and can't touch anything else. Even
allowing exec() we can feel much more comfortable in what the user is
able

to touch. I still hate that exec() though. At this point, it's the users
only direct path into our main system.

So.. in php.ini let's find "disable\_functions = " and add "exec" to the
end. After restarting the PHP processes we will have eliminated the
worry of exec(). In my case I need it. Largely in part from bad code and
other

developers using what amounts to being the wrong tool for the job. For
now, it's a battle that I'll need to admit defeat on. Coming up, a bit
battle with thousands of lines of code. Reworking a whole PHP project to
something

that is better suited for the job. Perhaps it's time to learn python.

Sometimes I need to run things as the user. These things are often not
available inside of the jail. Things like PHP. I don't want the user to
see that PHP is even available except for the .php files. There's a
simple way

to do this. Rather than explain the whole thing, I'll just show.

::

    sudo -n -u $user -s -- $command

It looks simple, but it's another thing that took some painful work.
Basically, this allows me to do something as the user from outside of
the jail. There are a few itty bitty tweaks that need to take place but
I have had no issues with it once working.

In the end it comes down to this. My setup won't work for everyone. If I
gave you my Nginx and PHP configs, you probably couldn't use it. I'm
commonly referred to as crazy or insane and this is a fact I won't
dispute.

Running so many websites on 1GB of RAM is a feat in itself. However,
making a secure and locked down server is possible. It's not that hard.
If there's any documentation to what you're doing, it's trivial. Yes,
selinux did go through my head. No, I've not said no to it yet. It's
just an annoying pain that I don't feel like dealing with yet.

What do you do to harden your server? I'd love to know. I'm doing
something that's apparently not done and poorly documented. Hopefully
this will throw a bone in the direction of someone else fighting the
same thing. There's so many things you can do. However, most of them
require that you heavily modify your OS. I'm happy to have found a
system that doesn't require this on nearly the same level.

.. _for jailkit: https://launchpad.net/%7Ejailkit/+archive/ppa
.. _the guide: http://www.marthijnvandenheuvel.com/2010/03/10/how-to-create-a-chroot-ssh-user-in-ubuntu/
.. _jailkit website: http://olivier.sessink.nl/jailkit/
