Power Friendly Memo Script
##########################
:desc: Create quick little memos/notes
:date: 2008-12-30 19:08
:tags: kiss

I've been bragging recently about how many obstacles I've overcome with
Linux as a whole. There's many things I've been doing to Ubuntu to make
it extremely fast and flexible for my uses. I also happen to be one of
those people that forgets absolutely everything.

I very frequently decide I'm going to do something later that isn't
something big and forget about it, or forget about a homework
assignment. I've tried using those note taking and memo apps. I found
that tomboy was pretty good. Unfortunately, not good enough.

I decided to go through and figure out a very simple way to take memos
or quick little notes that wouldn't eat up any extra memory or waste any
extra battery.

The isn't a small app that you can download but it can be set up very
easily. I don't know how to do key binding in anything other than
OpenBox but I'm sure a few quick Google searches will answer things
pretty quick. I'll try to do a search and list some of my finds. later
on.

First off, you'll need to make the script. I keep all of my scripts
inside of ~/.bin/ unless I want them system usable, in which case I use
/usr/local/sbin/ for most things.

So, open up your favorite text editor and create ~/.bin/memo. Add the
following text to this file.

::

    #!/bin/bash
    echo "Enter a short memo followed by Enter."
    read memo
    echo "$memo" >> ~/memo

I know it's short but also very efficient. Now you need to make the
script executable. Do this with chmod +x ~/.bin/memo.

Now we need to be able to call this script, otherwise it's not very
useful to us. You can either call it from the terminal. If you have
~/.bin in your PATH variable you can just call it by typing memo. You
can add it to your path variable with PATH="$PATH:~/.bin".

I prefer to call it using a hothey. I use Alt+F6. Not for any particular
reason other that Alt+F2 and Alt+F4 are being used.

Open up ~/.config/openbox/rc.xml. Please, don't attempt this if you
don't have a very minimal understanding of XML.

Find the tag. You will want to add a level directly below this. I
actually put mine right above . Add the following text to the XML file.

::

    xterm -T Memo -geometry 63x2+450+336 -e /bin/bash -l -c /home/michael/.bin/memo

Save the file and reload OpenBox. You should now be able to Press Alt+F6
and have a box pop up in your screen that you can take a memo with. Type
some text in and press enter. This text will be tagged to the end of
~/memo.

I personally have a --- UNSORTED --- line at the end of the file.
Whenever I go into the file, I can take anything below that line and
sort things out.

The -geometry option for xterm can be kind of tricky to figure out. You
will probably need to mess with it to fit your screen.

::

    -geometry AxB+C+D . A=Width \| B=Height \| C=From Left \| D=From Top

Hope this can help you as much as it helped me.
