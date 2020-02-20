Long Term Secure Backups
========================
:date: 2016/05/28
:tags: infrastructure, backups, linux, security
:desc: How to build a low cost and secure backup solution

Not that long ago, I managed to delete all of my physical HV hosts, backup
server, all external backups, and a bit more. The first question that most
people would ask would probably be how that's even possible. That may become
a post by itself; it probably won't, though. What really matters is how I can
keep this from ever happening again?

I sat down for some time to come up with some requirements, some ideas, and
eventually rolled out a backup solution that I feel confident with.


Requirements
------------

To build this backup solution, I first needed to define a set of requirements.

* No server can see backups from other servers
* The backup server can not access other servers
* The backup server must create versioned backups (historical archives)
* No server can access its own historical archive
* All archives must be uploaded to an off-site location
* All off-site backups must enforce data retention
* The backup server must be unable to delete backups from an off-site location
* All off-site backups must be retained for a minimum of three months
* The backup server must keep two years worth of historical archives
* The entire solution must be fully automated
* Low budget
* Can't impact quality of service

Some of these may sound like common sense, but most backup tools, including the
big dollar options, don't meet all of them. In some (way too many) cases, the
backup server is given access to root (or administrator) on most systems.

The Stack
---------

Deciding how this stack should be contructed was definitely the most time
consuming part of this project. I'm going to attempt to lay out what I built
in the order of the direction data flows. Wish me luck!

Server to Backup Server
~~~~~~~~~~~~~~~~~~~~~~~

The obvious choice is SSH. It's a standard, reasonably secure, and very easy.

When people do backups with SSH, the typical decision is to have the backup
server initiate and control backups, which almost always means the backup server
has the ability to log into other servers. This makes your backup server a
substantially higher value target for an attacker. Yes, it's horrible if any
system gets compromised, but this minimizes the impact and aids in recovery.

Scheduling
~~~~~~~~~~

Every server has a backup script that runs on a pseudo-random schedule. Because
the node name will always be the same and checksums are worthless unless they
produce the same value every time, I was able to use the node name to build the
backup schedule.

This boils down to what is essentially:

.. code-block:: sls

    snap:
      cron.present:
        - identifier: snap
        - name: /usr/local/sbin/snap
        - hour: 2,10,18
        - minute: {{ pillar['backup_minute'] }}

The 'backup_minute' is created with ext_pillar. To build the entire ext_pillar
is a task for the reader, what matters is:

.. code-block:: python

    import zlib
    return zlib.crc32(grains['hostname']) % 60

You may notice that using 60 doubles the chance a backup running on the top of
the hour. You can feel free to choose 59, but I like nice round numbers that
are easy to identify.

SSH Keys
~~~~~~~~~

I mentioned that I wanted something 100% automated. I'm a huge fan of Salt and
use it in my home environment, so Salt was the only choice for the automation.

A feature of Salt is the Salt Mine. The mine is a way for minions (every server)
to report bits of data back to the salt master that can be shared with other
systems. I utilized this feature to share root's SSH public key. I also used
salt to generate that key if it doesn't already exist.

Here's a mini-snippet for clarification:


.. code-block:: sls

    root_sshkeygen:
      cmd.run:
        - name: 'ssh-keygen -f /root/.ssh/id_rsa -t rsa -N ""'
        - unless: 'test -f /root/.ssh/id_rsa.pub'

    /etc/salt/minion.d/mine.conf:
      file.managed:
        - contents: |
            mine_functions:
              ssh.user_keys:
                user: root
                prvfile: False
                pubfile: /root/.ssh/id_rsa.pub

Overall, this is pretty simple, but amazingly effective.

User Accounts
~~~~~~~~~~~~~

At this point, all of the servers are ready to back up their data. They just
aren't able to yet because the backup server is sitting there empty with no user
accounts.

This part is surprisingly easy as well. I simply use salt to create a separate
jailed home directory for every server in the environment. The salt master
already has the public SSH keys for every server in addition to the servers
hostname.

To keep things simple, this example does not include jails.

.. code-block:: sls

    {% for server, keys in salt['mine.get']('*', 'ssh.user_keys').items() %}
    {{ server }}:
      user.present:
        - name: {{ server }}
        - createhome: True
      ssh_auth.present:
        - user: {{ server }}
        - names: [ {{ keys['root']['id_rsa.pub'] }} ]

    # Ensures the user directory is never readable by others
    /home/{{ server }}:
      file.directory:
        - user: {{ server }}
        - group: {{ server }}
        - mode: '0700'
        - require:
          - user: {{ server }}
    {% endfor %}

This will get user accounts created on the backup server, add the SSH public
key to the users trusted keychain, and force the users home directory to be set
to 700 which prevents other users/groups from accessing the data.

Backup Archives
~~~~~~~~~~~~~~~

Now that data is getting from all servers to the backup server, it's time to
start having more than a single copy of the data. The best tool I could find for
this job was rsnapshot. I simply point rsnapshot at /home (or /srv/jails) and
keep data stored where the existing servers can't access it. This means no
compromised server can destroy any previous backups.

I broke some of my own rules and have rsnapshot also backing up my pfSense device
as well as my Cisco switch configurations. I'll get a better solution in place
for those, but that is it's own project.

Ice Ice Baby
~~~~~~~~~~~~

At this point, we have a rather complete backup option that meets nearly
everything I care about. So far, we're at $0.00 to build this solution.
However, off-site backups haven't been included.

Do you want to trust your buddy and arrange to share backups with each other?
Hopefully the obvious answer to everyone is an emphatic NO.

The only two reasonable options I found were AWS Glacier and Google Nearline.
Because we're talking about data that you should never need to actually access,
the two options are very comparable. Google Nearline advertises fastest time to
first byte; however, the more you pull down, the slower your retrieval rate is.
AWS Glacier advertises cheapest storage, but the faster you want your data, the
more you get to pay.

The important thing to remember is that you're dealing with an off-site backup.
You are "putting it on ice." If nothing ever breaks, the only time you will ever
access this data is to verify your backup process.

I wrote a relatively simple script that runs on a cron (2x/mo) that:

* Creates a squashfs image of the entire rsnapshot archive
* Encrypts the quashfs image with a public GPG key
* Uploads the encrypted image

I created a GPG key pair for this single process, encrypted the private key with
my personal key, moved multiple copies (including paper) to various locations,
and removed the private key from the server.

Wrapping Up
-----------

There are a *lot* of backup options that exist. I have concerns about nearly
every option that exists, including most commercial/enterprise offerings. To
have a backup solution that I considered reasonably secure, I had to spend a
lot of time thinking through the process and researching many different tools.

I very much hope that what I put here will prove useful to other people trying
address similar concerns. As always, I'm more than eager to answer questions.
