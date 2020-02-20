Perfect Irssi and OpenBox Integration
#####################################
:desc: Set up alerts for irssi on your desktop
:date: 2008-12-30 19:11
:tags: irc, openbox

I think I achieved nearly the perfect Irssi + OpenBox.

There's four steps to my setup. Configuring gnome-terminal, alltray,
irssi, and an image.

First of all, we need to set up irssi. If your'e reading this, I'm
guessing you've already done this. I use murf. You can find themes at
http://irssi.org/themes. Download one, place it in ~/.irssi/ and
execute /theme inside of irssi. You can do /save to save these settings.

To set up gnome-terminal, go to Edit > Current Profile. Go to the
Effects tab. Now choose the Background Image option. I uploaded an image
that somebody gave me that I really liked. Just download it to wherever
you want. Spaces in the path name are usually bad. Once you set the
background image, you will want to change the transparency level. This
is a rather bright image. I turned it down to about 80% opacity. The
image is uploaded as cavechaos.jpg. I keep this file in
~/Pictures/Backgrounds/

Now on to allray. Install it using sudo aptitude install alltray. This
will allow you to run your application in a tiny icon on your tray. I
use pypanel for this. Some people just use docker, but I'm pretty stuck
on pypanel.

Now that we have alltray, we need to add some pretty pictures for it. If
you try to run gnome-terminal inside of alltray right now, you will get
kind of an ugly terminal icon. I prefer something a little more fitting.
I uploaded a copy of irssi.png. I use a very black theme so a black icon
doesn't really work. I inverted the colors and came up with
irssi-invert.png. These images just came from the official irssi.org
site. I keep these in ~/.icons/

Now to bring them all together. I just have a menu entry with the exact
text. Remember where I keep everything and adjust this accordingly.

::

    alltray -s -na -i ~/.icons/irssi-invert.png "gnome-terminal --hide-menubar -t irssi -e irssi"

It looks like a lot, but I'll break it down.

::

    alltray:
        -s - Makes the window shown when it launches rather than hiding it
        -na - Keeps (AllTray) from showing up in the title
        -i - Gives alltray an icon to use in the tray
        " " - Everything inside quotes is what alltray will call

    gnome-terminal:
        --hide-menubat - Keeps the menu hidden.
        Having multiple tabs can affect the way irssi behaves.
        -t - This is the text gnome-terminal passes to the WM for the title
        -e - This is what gnome-terminal will execute.

Problems with this setup:

1. I need to figure out how to make gnome-terminal startup maximized.
#. I need to figure out how to make gnome-terminal startup on screen 2.
#. Gnome-terminal doesn't grab the title and instead uses "Unnamed Window"

Attachments:

|image0| `cavechaos.jpg`_

|image0| `irssi.png`_

|image0| `irssi-invert.png`_

.. _cavechaos.jpg: /files/uploads/cavechaos.jpg
.. _irssi.png: /files/uploads/irssi.png
.. _irssi-invert.png: /files/uploads/irssi-invert.png

.. |image0| image:: files/icons/image-x-generic.png
