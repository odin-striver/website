Persistent SSH
##############
:desc: Ensuring work isn't lost when an ssh session disconnects
:date: 2010-08-11 22:19
:tags: ssh

It's time for another post. Recently I've had issues with dropping
network connections or wanting to connect and keep working on the same
thing from other systems. Most of you probably already know the answer.
You screen.

Sounds easy enough. My issue is that I'm incredibly lazy. I don't want
to SSH into the system AND start screen AND detach AND reattach. That's
just asking way too much of someone like me.

Here's the very simple solution. In my ~/.bashrc file I appended this
section of code.

::

    ssh() {command ssh "$1" -Xt screen -aAdr -RR work bash}

This makes a function called SSH. Bash always uses a function over a
command if the two collide. So running ssh will call this function
instead of calling the command(app) /usr/bin/ssh. If you want to not use
the function

but use SSH you have two options. The first option is call the function
something else. Either s(), sshw(), or something\_else().

Recursion can happen. The "command" command is a BASH built-in function
if I recall correctly. This command breaks the function calls so it will
call /usr/bin/ssh (found from $PATH) rather than ssh(). Simple enough
to understand but not so easy to explain. I hope I did OK with that.

The next part of this is the $1. This is the first parameter passed to
the ssh command. Example being "ssh foo.com" will insert foo.com in
place of $1.

The rest of this is pretty simple. You establish the SSH connection and
call screen. If screen is running an instance named work it will attach
to that and boot the other connection. If the instance isn't named
doesn't exist

then it gets created. Then "bash" following is just the command executed
on the new instance. I have a similar command that has irssi at the end.

While writing this I was thinking about the need for using ssh to
connect to another server. Maybe you want to do something entirely
different. The answer is pretty simple. The function is designed so you
only pass one

parameter to it. So any additional parameters means you're doing
something different.

To make it simple I just came up with this function instead.

::

    ssh() {
        if [[ "$2" == "" ]]; then
            command ssh "$1" -Xt screen -aAdr -RR work bash
        else
            command ssh $@
        fi
    }

If you only pass the server you're connecting to into the ssh command,
it will work with screen. If you pass it with more than one parameter it
just runs /usr/bin/ssh with the parameters you used.

It's so simple but putting the pieces together can be a bit of a pain
the first time. I hope this will help someone else that may have a
similar use case.
