Creating Your Own Bazaar Server
###############################
:desc: Set up a basic bazaar (bzr) server
:date: 2009-10-31 23:02
:tags: bazaar, vcs

By now we've all heard about the Bazaar (bzr) version control system. If
you're a coder then you're well aware of what a version control system
is and why it's helpful. If you code on Launchpad you're equally aware
how incredibly awesome this system is.

Rather than discuss how incredible bazaar is, I'd like to explain how to
set up a production level deployment for a bzr server. If you're curious
what makes bazaar great, just try it out. You can use
https://staging.launchpad.net/ to create branches for playing around.

To deploy a low level and basic setup you only need to run this command
on your server:

sudo aptitude install openssh-server bzr

That's really all there is to it. You can now push an existing code
branch to your server using the following command:

::

    bzr push bzr+ssh://yourserver.com/~/branch

That's only a basic deployment. What I like doing is having branches
where multiple people can work on the same branch. This first thing I do
is create a directory that this whole thing will be based in. I like to
do this on its own partition for obvious reasons. For me this always
exists at /bazaar. I then use the following:

# Get into the branch directory

::

    cd /bazaar

# Create a directory for branch content

::

    mkdir bzr

# Make a nice short directory name to this

::

    cd /
    ln -s /bazaar/bzr

Now anyone with the right permissions (root) can push to the server
using bzr push bzr+ssh://yourserver.com/bzr/branch. However, we
don't want to give everyone root access. Instead of doing this, I issue
the following:

# Create a generic bzr group

::

    groupadd bzr

# Assign group to branches


::

    chown root:bzr /bazaar/bzr

Now anyone in the bzr group can push to this. However, we're working in
teams of users. The user that makes the commit will be the only one that
can manage this branch. I guess it's time to learn about the "sticky
bit." This little bit allows us to retain the group that owns the
directory. The sticky bit doesn't seem to like retaining the owner but
that becomes irrelevant because it's the groups we care about.

# Set generic permissions

::

    chmod 770 /bazaar/bzr

# Set the sticky bit

::

    chmod +s /bazaar/bzr

Now it's time to give a user permission to work with these branches.

::

    usermod -a -G bzr username

You should be ready to rock now. If you create a branch and decide that
only a handful of users should be able to access it, this is easy.
Something could be a highly secret piece of code that is the "bread and
butter" to a massive project you are undertaking.

# Create new group

::

    groupadd bzr-special

# Set permissions on branch

::

    chown -R root:bzr-special /bzr/branch

# Add users to the special group

::

    usermod -a -G bzr-special username

Heck Ya! That was easy enough wasn't it? It really is once you've gone
through the hassle of picking out these little things. It's actually
amazingly easy if you have a guide. I wasn't able to find this guide and
I hope this will help others trying to do the same thing.

What's next? I'd suggest pulling the loggerhead source and setting it
up. This is a great tool for seeing revision changes. I'd like to see a
way to send an email diff on branch changes but this may be too hard
without created a chopped down version of Launchpad.
