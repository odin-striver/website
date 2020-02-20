Light Weight Firefox Notes
##########################
:desc: Some firefox tweaks to help out productivity
:date: 2010-07-17 22:55
:tags: kiss

Lately I've been cumulating a very large list of things I need to do.
It's been getting harder and harder to keep track of what I need to do.
If I make a nice simple text file and a command to open up vim with my
notes then I wind up adding notes but never checking them. That helps
but it's not enough. There's a lot of really heavy note taking options
out there. You could make your home page go to Google Notebook. That's
definitely not light weight.

I got fed up with these very heavy and cumbersome options. Instead, I
wanted something that was magic and instant. I don't want to wait to
load things. What do we come up with then?

I started thinking about what applications I use the most. Firefox,
irssi, claws-mail, the terminal. That covers most of it. With Firefox I
open up new tabs all the time. BINGO! All I need to do is put my notes
in that new tab before I press Ctrl+L or Ctrl+K. Simple right? Yes.

Here's how I did it:

First of all, we need to make a file for our notes. We'll place this in
/home/YOUR\_NAME/.notes. This leading dot (.) on the notes file will
make it a hidden file. This will initially be a hidden file. I'd rather
apply some pretty formatting. In this file I added the following text.

~/.notes

::

    <style> body { background-color: #BAD6AB; color: #000000; } </style><body><center><h1> Notes </h1>

It's not W3C compliant and honestly I don't really care. For this
purpose there's not really any sensible way to do it without using a
second file. That adds weight that I don't want.

Now we need to make this file our home page. I'm assuming you replaced
YOUR\_NAME with your actual user name above. We'll do that again. In
Firefox, go to Edit > Preferences. Under th

e General tab you will see a Startup box. In the "When Firefox starts:"
drop down pick Show my home page." In the "Home Page:" text box type
"file:///home/YOUR\_NAME/.notes" without the quotes. Now when you open
Firefox, this file will be displayed.

This still isn't simple or easy though. We definitely want to make it
easy to enter notes. Let's do this. I use rxvt and dash because they're
as light as you can get without being pieces of crap. I also use
Openbox. I added a section to my rc.xml file that looks like this.

~/.config/openbox/rc.xml

::

    <keybind key="W-n">
        <action name="Execute">
            <execute>rxvt --geometry 100x1+300+300 +sb -fn 9x15 -bg black -fg grey -T Notes -e /bin/dash -c 'read -p "Note: " note && echo "&lt;p&gt;$note&lt;/p&gt;" >> ~/.notes'</execute>
        </action>
    </keybind>

I broke this onto a few lines for readability. The non-broken command is
a few lines down.

This runs the command when I press Win+n. The important thing to take
away from this is the section between the execute tags. It is the
shortcut that you need to run.

::

    rxvt --geometry 100x1+300+300 +sb -fn 9x15 -bg black -fg grey -T Notes -e /bin/dash -c 'read -p "Note: " note && echo "<p>$note</p>" >> ~/.notes'

This will give you a very nice little pop up that lets you type in a
note, press enter, and done. Remember that you need to have both rxvt
and dash installed. Try it out and then open your home page in Firefox.
You should be very pleased with the result. If you don't think it's
pretty - then change the style tags to whatever you want.

That's great. How often you actually open your home page could change
this though. If you're like me, it's very rare. I do open a lot of new
tabs though. There is an addon called `New Tab Homepage`_ that does a
very simple task. When you open a new tab, it loads your home page. I'm
very surprised this isn't an option built into Firefox. Ctrl+T and you
see your notes.

There you have it. An in-your-face and drop-dead-easy but also
super-fast-and-light way to keep you on top of what you need to do. I
haven't tried this out for too long so we'll se how it stands up in the
long run.

.. _New Tab Homepage: https://addons.mozilla.org/en-US/firefox/addon/777/
