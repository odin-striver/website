Light Weight Ubuntu Kernel
##########################
:desc: Building a light and tiny linux kernel in ubuntu
:date: 2009-12-04 17:36
:tags: kiss, overkill

As a preliminary note: DO NOT follow anything in this and proceed to ask
for help. If you follow this than consider yourself void of ANY support.
Especially from the -kernel channel. They support and develop stock
kernels, not your personal modifications.

Now.. In my quest for a fast boot time into a fully functional system
that is very light weight, I tried out Gentoo. After using Gentoo I
discovered that they're not that "ricer" community everyone claims they
are. In many way's they're the exact opposite. Sure some of them fall
into the ricer category but they're not very common.

One of the biggest aspects of Gentoo is that you compile your own
kernel. This was the most painful parts for me until I finally got the
hang of it. The default Gentoo kernel is minimal and requires you to
enable some extra features before compiling.

I decided to take this to the next step and after getting the kernel to
work spend a massive amount of time trimming out the 'fat' that was
default. By doing this I got a firm understanding of what each piece of
the configuration was and the arrangement inside menuconfig. This is
where I started to take on the ricer nick.

After a while I tired of Gentoo and my short segue neared to an end. I
have continued to hang around their awesome community. They're
incredibly helpful for any distribution and are great to just have a
chat with.

During my return to Ubuntu I took the realization that the existing
kernel is very heavy. Of course part of the appeal of Ubuntu is that it
"just works" for anyone. I really did become a ricer and decided to see
what I could do.

The general process is:

::

    aptitude install git-core
    git clone git://kernel.ubuntu.com/ubuntu/ubuntu-karmic.git
    cd ubuntu-karmic
    git tag -l Ubuntu-*
    git checkout [LatestTag]
    make menuconfig
    # Tweak the crap out of it
    make all modules_install install
    update-grub

To update when a new kernel is released:

::

    cd ubuntu-karmic
    git fetch
    git checkout [LatestTag]
    make all modules_install install

That is the simplest way to deal your own kernel. Don't think you're
smart enough for the KernelTeam though. These guys deal with the kernel
code and work on modifications that are intended to eventually make it
into the mainline kernel tree. It's also not how they suggest packaging
it for further distribution or proper installation.

What you can now do is - as I said above - tweak the crap out of your
kernel. I was able to get my kernel under 2.4MB in size without any
init\*. This is very small and gave a very noticeable change in the
system.

* Many kernel panics
* Could log into system
* Severe overheating
* Couldn't connect to any network
* Couldn't load profile when logging into system
* Unmounted file systems
* No 64bit support (mostly java/flash issues resulted)
* No AppArmor support
* No iptables support
* No encryption support
* Various other issues

Those are just some of the issues I caused for myself. Read that again,
I caused these issues for myself. That means it was my fault and it was
up to me to fix these issues.

I have no time available to me to 'rice' this more but I would like to.
I'll just have to consider that rather than reserving memory for the
kernel, it actually frees memory. I've been happy with the performance
change as well. This will just have to be enough for me.

I'm attaching my kernel configuration for your reference. Keep in mind
that I said this is tweaked for just me. That means that it is almost
guaranteed to not work on your system. Rather, you can just use it to
see some of the changes I made and play with them incrementally.

Attachments:

|image0| `kernel.config`_

.. _kernel.config: /files/uploads/kernel.config

.. |image0| image:: /files/icons/text-plain.png
