Keeping IT DRY
==============
:desc: Keeping Information Technology DRY (Don't Repeat Yourself)
:date: 2013-08-07
:status: hidden

Acronyms!

* IT: Information Technology
* DRY: Don't Repeat Yourself

The concept of "DRY" was first written about in the book The Pragmatic
Programmer, but it wasn't new then. You have more than likely heard someone
tell you something like, "Listen now, because I'm not repeating myself!"

Why don't we like repeating ourselves? Easy! Doing something twice means you've
wasted effort. When it comes to coding and scripting, if you need to update
that bit, you have to update it twice. When you explain something, you have to
explain it twice.

When you keep your IT DRY it means that you don't repeat tasks. If something
needs to be done with repetition, you write a script. If you could have two
scripts that do nearly the same thing, you combine them and make it use a
parameter to differentiate what is happening.

Example::

    /usr/local/sbin/backup-script-linux
    /usr/local/sbin/backup-script-aix
    /usr/local/sbin/backup-script-windows

    vs.

    /usr/local/sbin/backup-script -t linux
    /usr/local/sbin/backup-script -t aix
    /usr/local/sbin/backup-script -t windows

See the difference? If backup-script ever needs to be changed because some
reporting server ever moved, then you get to update it either three times in
the individual scripts, or once in the single script that accepts a parameter.

That's a rather trivial example. Do you SSH into many servers every day and
start or resume screen or tmux every time you get in? That's another chance for
automation! Make those start or resume automatically every time.

The trick for that...

In ~/.bash_aliases (.bashrc), I have something like this::

    ssh() {
        if [[ "$2" ]]; then
            command ssh $@;
        else
            command ssh "$1" -t screen -A -d -RR work bash
        fi
    }

This is rather simplified from what I actually use, but this works for the use
case I specified.


The Point
~~~~~~~~~

The IT world should NEVER repeat itself. That's the general point of this blog.
If I get frequent requests for help on a topic, I'll write the post rather than
continue to explain the same thing repeatedly. That's the point/goal of my this
site.

::

    Keep your IT DRY!
