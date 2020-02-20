64bit Java / Flash Deathroll
============================
:desc: Getting java and flash to work on a 64 bit Linux server
:date: 2009-09-10 16:43
:tags: java, flash

I think Linux users can safely agree that Flash and Java make web usage into a
battle ground. Many of us choose to blame the issue on the distribution we use.
When we favor our distribution too much we'll point fingers at Sun or Adobe. If
we use the FOSS versions we'll point fingers at the respective maintainers.

The sad truth is that I'm writing this not really knowing where the blame lies.
However, I'm not sure that it even matters. I don't care whose fault it is, I
just want it to work.

How can we fix this plaguing problem? For starters, I think we need to get back
to our roots. Rather than rely on the repositories, lets roll back to pulling
the vanilla packages. For me, this worked like absolute perfection.

Note that I'm using 64bit and this is where most issues are. Following this with
32bit is nearly the exact same except for the obvious changes.

To get ‘vanilla' 64bit java:

Download 64bit java tarball from http://www.java.com/.

As Root::

    # Remove old java
    aptitude purge sun-java6-jdk sun-java6-bin sun-java6-jre sun-java6-plugin
    # Create the directory
    mkdir -p /opt/java/66
    # Move the downloaded package to the new directory
    mv ~/jre-6u17-linux-x64.bin /opt/java/64
    # Make the file executable
    chmod +x ~/jre-6u17-linux-x64.bin
    # Execute the binary file / Unpacks java
    /opt/java/64/jre-6u17-linux-x64.bin
    Do you agree to the above license terms? [yes or no] yes
    # Install the java option
    update-alternatives --install "/usr/bin/java" "java" "/opt/java/64/jre1.6.0_17/bin/java" 1
    # Set the Java option
    update-alternatives --set java /opt/java/64/jre1.6.0_17/bin/java

As User::

    # Create the plugins directory if it doesn't exist
    mkdir ~/.mozilla/plugins
    # Force the creation of a symbolic link to the installed java
    ln -sf /opt/java/64/jre1.6.0_17/lib/amd64/libnpjp2.so ~/.mozilla/plugins/

Now you need to get flash working:

Download the latest flash player from http://labs.adobe.com/downloads/flashplayer10_64bit.html

As root::

    # Remove old flash
    aptitude purge flashplugin-nonfree flashplugin-installer
    rm -f /usr/lib/mozilla/plugins/*flash*
    rm -f ~/.mozilla/plugins/*flash*
    rm -f /usr/lib/firefox/plugins/*flash*
    rm -f /usr/lib/firefox-addons/plugins/*flash*
    rm -rfd /usr/lib/nspluginwrapper

As User::

    # Unpack flash
    tar zxf libflashplayer-10.0.32.18.linux-x86_64.so.tar.gz
    # Create plugins directory if it doesn't exist
    mkdir ~/.mozilla/plugins
    # Move flash to plugins directory
    mv libflashplayer.so ~/.mozilla/plugins/

Now to test that it works...

* Test Java: http://java.com/en/download/installed.jsp
* Test Flash: http://www.adobe.com/shockwave/welcome
* Test Flash Note: Ignore the "Adobe Shockwave Player"

NOW! What does this mean? It sure doesn't prove that Adobe or Sun are against
Linux. I really don't think we suspected Sun of that. It could possibly prove
that our distributions aren't keeping up on these issues. Considering the vast
number of distributions with the issue, I don't think that's really the case
either. I would point fingers at those that maintain the packages but I know
some of them personally and I can guarantee flash/java are important to them.

Where does that leave us? It leaves us with a whole massive list of suspects.
Each and every package installed on a system could be causing part of the
problem. GTK+ update caused many issues and I can see that being part of the
existing issue. However, I doubt it's the only reason.

Thousands of bugs have been created in the issue queues among the bug trackers
for many distributions as well as many different packages.

I have no doubt the issue will be resolved at some point. Adobe and Sun have
proven to be taking an active role in this support. It's just up to us to track
down and destroy the remainder of issues. Our big up side is that the companies
aren't against our success. As opposed to multimedia companies because of that
dang DRM crap that they worship…
