What You Need To Do After Installing Ubuntu 10.10
#################################################
:desc: A quick little ramble about installing ubuntu
:date: 2010-10-03 02:32
:tags: linux, overkill

Every six months these articles become popular. I've been using Ubuntu
10.10 (Maverick Meerkat) for a few months now and I thought I'd share
what I thought.

For most users
--------------

**Step 1:**

Install Ubuntu 10.10

**Step 2:**

Install the little extras you might want, such as Thunderbird, Galeon,
etc.

**Step 3:**

Enjoy!

For cli users
-------------

**Step 3:**

::

    apt-get install aptitude
    aptitude purge vim-tiny
    aptitude install vim

**Step 4:**

Enjoy!

For psychotic users like me
---------------------------

**Step 1:**

Grab Alternate CD

Install "Command Line" system

**Step 2:**

Strip the crap out of it - bare essential packages only!

**Step 3:**

TOO MANY PACKAGES! Get them out.

No, you don't need that, prove to me you can't boot or network without
it..

**Step 4:**

Get rid of vim-tiny; bring in vim and aptitude.

**Step 5:**

Tell aptitude not to bring in suggested/recommended packages.

Now just install the bare minimum system you need

**Step 6:**

Create a chroot; hop into it.

Install what you need for compiling things.

**Step 7:**

Grab the kernel source, trim down until there's almost nothing there.

Install that kernel to your system and remove all the other kernel
stuff.

I like monolithic because now I have no need for copying modules.

I also trimmed it to the point where I don't need initramfs/initrd.

**Step 8:**

Looks good? Now trim it some more.

**Step 9:**

Tweak the crap out of openbox and anything else you need.

**Step 10:**

Enjoy!

Just for the heck of it, I decided to post my .config. I usually get
asked for it when I mention a stripped down kernel.

Attachments:

|image0| `kernel.config`_

.. _kernel.config: /files/uploads/kernel.config
.. |image0| image:: /files/icons/application-octet-stream.png
