The Inventory Driven Datacenter
===============================
:date: 2017/09/17
:tags: infrastructure, debian, networking, virtualization
:desc: Inventory Defined Infrastructure -- A New Era For Information Technology


It's been interesting to observe the progression of technology over the past few
years. We continue to increase what can be done with technology and we continue
to decrease the barrier to entry. What's expected of IT professionals must grow
in order to keep up with the demand.

While many fads have come and gone, system automation isn't going anywhere. Most
of us have reached a point where it's no longer possible to do our jobs without
implementing an automation solution. The further our industry progresses, the more
we are able to accomplish with less man power.

Unfortunately, it's become common for those that have implemented an automation
solution to spend more time maintaining the solution than it took to maintain the
original design. As IT professionals, it's time to take control of our automation.

My goal is to open source everything I know about automating infrastructure, my
opinions of best practices, neat tips and tricks, etc. I hope that what I discuss,
along with the material released, will be useful to organizations needing to get
a fresh start on their infrastructure. Through this, I hope that we can enter a
new era of system administration... an era where we no longer depend on ssh.


Disclaimer
----------

This post starts with basic beginnings but describes a new era of IT in which
system administrators become highly skilled administrative workers.


My Beginnings
-------------

My first corporate gig landed me in a company of over 24,000 employees. At one
count there were three people maintaining 150 Windows servers, two people
maintaining 50 AIX servers, and me handling ~200 servers. The Linux role came
with the added responsibliity of managing "every app running on all Linux hosts."

Automation wasn't a thing anywhere in the environment and any tiny bit of
information that could be found was always incorrect/inaccurate. Even worse, none
of the scripted process worked correctly and bridging those gaps was also entirely
undocumented. This was in an environment where updates were pushed out using scp
and then unpacking a tar file on top of the file system root.

At one point, many automation solutions were considered, but, ultimately, salt
v0.15.x was dismissed as being the best but still utterly terrible. As the
employment continued, more responsiblities continued to fall into the "as-assigned"
bucket. The workload continued to increase and I started volunteering overtime
just to keep up.

Eventually, there were about twelve massive projects--including rolling out a
replacement LDAP solution, replacement email solution, Windows 7 migration,
hardware refresh at >250 sites, etc.--that were going to not just depend on me
to help implement, but maintaining over half of them was to become another
"as-assigned" task. Clearly, I needed to take another look at salt.

Thankfully, the second look at salt showed some extreme leaps. It didn't take
long before I started replacing scripts with states and figuring out how the
different salt bits fit in with each other.


Years Later
-----------

There were some significant growing pains with salt. As an early adopter, there
were many scalability (and some security) bugs encountered. It was not uncommon
to find a module completely missing.

Fortunately, salt has an incredibly helpful community backed by an equally
enthusiastic company that interacts very closely with that community. Many of the
more critical issues encountered were met with quick and complete resolutions.

After only a few years, salt became the tool central authority of all configuration
of almost all of the servers under my umbrella. At this point, the threat of
double the servers was no longer something to lose sleep over. They would be added
and maintained just like any other server.

While effort had been spent rebuilding infrastruture using salt, another project
was going on at home. The goal of this project was to have an enterprise-level
set of infrastructure at home that is deployed in the most perfect way possible,
managed 100% by saltstack.

When this goal was achieved, the next was set. This time, my dream was to use
salt to deploy and manage my entire infrastructure... without ever having to
log into my salt master. This, my dearest readers, was no small feat. Many code
contributions had to be made and many days were spent tracing and debugging
every part of salt. The reward was definitely worth the effort (and wait).


Defining IDI
------------

The first obvious question is: What does Inventory Driven Infrastructure mean?

I believe I get to be the father of this term! As such, let me firmly define it.

Inventory Driven Infrastructure means using an inventory management system to
define the expected running state of all devices in an infrastructure.

Note: Although IDI has a different definition, I'm overloading it for the sake
of this article.


High Level View
---------------

To further define IDI, consider the following scenario.

A group of developers has announced that they are working on a difficult problem
and would like some additional servers deployed to their QA environment. You, as
the administrator, log into your inventory management system (Device42, RackTables,
NetBox, etc.) and click "Add Device."

Now, you read the hint on the page, so you know that you can create multiple
devices by using a pattern. You use the hostname "qa-project-[7-11].domain.tld"
and specify some details such as site location (DC). Now you click "Create" and
you wait for five emails with five different highstate outputs to review.

Once you've reviewed the emails, you send a notification to your team letting them
know that their new servers are now ready for them to get into.

It turns out a kernel parameter was causing the problem. After some review, it
is decided that this parameter should be configured globally. The change is then
made globally. As an administrator, no review is required to push this to the
pre-develop branch, which only impacts pdev-* boxes. After confirming this
solution works without causing issues, a PR is created to merge these changes
into a develop branch where a different administrator (or two) must approve the
change. This is followed by giving developers a chance to review the changes
and sign off on a PR to push this into a QA branch. Of course, a QA team made
up of non-devs and non-admins would now be required to approve a merge PR into
the production branch... where the change would be queued for the next maintenance
window.

Now that the change has been pushed to production and the fix has been verified,
it's time to destroy the extra test boxes. You log into your inventory management
application, click the checkbox next to the systems you no longer need, click
remove, and then confirm removal.

Compare that to your current processes and it should become quite clear why
these changes are imperative to the longevity of our profession. Without these
changes, it is not possible to meet the demands of today, let alone the demands
of the future.


Bringing IT To Life
-------------------

While some tools exist that accomplish some of these goals, there has never been
a non-commercial option to bring this to the masses... until now. Creating this
open-source IDI solution was done over the course of a few years and required
substantial contributions to many projects. However, now that it's been done once,
I believe it is a solution that is easily repeatable if properly documented and
openly shared.

To make this happen, there are a few key steps:

1. Clean, error-free, and automatic highstates
#. Organized and modular salt structure
#. Salt-deployed infrastructure
#. Strong and well-written policies and procedures
#. Documented and followed standards (e.g. system naming)

You'll notice that everything mentioned requires a substantial amount of time and
effort to build. Unfortunately, these are the basic building blocks of IDI. There
is no opportunity for slacking here without causing headaches in the future.


Keep IT Clean
-------------

The most important thing you need to focus on is keeping things clean and
organized. This means avoiding formulas in almost every situation. Formulas are
good for demos, prototyping, and learning, but they are almost always a terrible
solution for production environments.

Instead, time needs to be taken to fully understand an environment. Even in a
fresh start-up environment, it's critical to understand exactly what is expected
to exist, how it works, what it communicates with, why it's there, etc. Building
network, service, and application diagrams should take priority at this stage.

This is one of the most critical points in the process. Without time and quality
at this stage, an environment is doomed to become unmaintainable and confusing.

When using salt, make sure to...

* Keep states simple and easy to follow
* Avoid the tendency to over-use jinja templating
* Read the documentation!!!
* Keep states re-usable and pillar-driver (yes, with jinja)
* Remember, complex problems don't need complicated solutions
* Use different repositories to logicaly separate data
* Know where things are rendered and what context is available
* Avoid templating and extra logic when it's not needed


Starting Point
--------------

When I landed my first corporate employment, I had a lot to learn and no time.
I ended up setting deploying some `Home Infrastructure`_ to test ideas, learn
how things work without breaking production, and just for fun. I was able to
use this to build my dream of the perfect environment.

While I may not have achieved the dream yet, I'm incredibly excited about what
I've achieved. I believe that sharing what has worked well and giving others
an exceptional starting point can contribute to better overall IT management
and better security through more management and less interaction.

I have created a `git repository`_ to host over 80% of my personal setup,
including my pillar data. This repository has all of the magic I've learned
over the past years.

It works amazingly well... for me. I encourage you to look through it and learn
from it. I demand you do not treat it as a formula. It is an example and is not
a substitute for knowing what's going on in your environment. (See: Keeping IT
Clean)

Due to a mishap a while back, I had the opportunity to rebuild nearly my entire
infrastructure from the ground. This gave me the opportunity to take everything
I've done, clean it up, test deploying all of it from scratch, and make sure it
never ever happened again.

I have covered deploying `infrastructure from the ground up`_ and setting up 
`long-term secure backups`_ in previous posts.


Ready For IDI
-------------

It needs to be repeated, Inventory Defined Infrastructure will be absolutely
worthless and nothing but a burden if care is not taken in the previous steps.
Not only will time be spent chasing down and creating problems, but those newly
created problems due to obscure or undocumented requirements will be pushed out
at the press of enter.

Ideally, you'll implement automated deployment tests to ensure breaking changes
aren't pushed out to any important environments. Some ideas exist, but fully
functional IDI comes first. Watch for a future post!

With the hard stuff out of the way, it's time to dig in. No matter how big or
small the organization is, no matter what the requirements are, no matter how
many domains or organizational units are involved, and no matter what is currently
in place, a full understanding of the problem means an ability to follow these
steps and achieve the same results.


IDI Requires Quality
--------------------

If *salt '\*' state.highstate* from the master of masters does not work, this
is the time to get problems corrected. This command will be run a lot. In some
environments limits will need to be placed on the scope, but it's recommended
to avoid that for as long as possible and instead focus on efficiency.

It's important that if **ANY** minions report an error or take an extremely long
time to complete, these issues need to be addressed first.

Next on the list is to make sure all minions return no changes unless something
within the environment changed to effect the mofification. In other words, when
two highstates are run back to back, the second should always produce exactly
zero changes. This includes states that made no modification but still reported
changes.

This is important because no-op highstates will mean clean execution and nothing
to generate an alert from. Take this example::

    #!/bin/bash
    fh="$(mktemp)"
    if ! salt '*' state.highstate &>"$fh"; then
        sendEmail -s 'Highstate Error Report' \
                  -f "$USER@$(hostname -f)" \
                  -t 'admin@domain.tld' \
                  -a "$fh"
    rm -f "$fh"

Efficient execution time is not critical, but making it a priority will likely
reveal complicated logic that would have otherwise been a landmine ready to
bring destruction. In some cases, these problems might be in salt core, but
most of those bugs have been worked out by early adopters.

These steps help produce a high quality selection of states that are easy to
read, debug, and maintain, and audit.


Where Automation Begins
-----------------------

With efficient highstates running cleanly, it's now possible to begin the with
some real automation! In a previous post, I described building an `infrastructure
from the ground up`. Part of that process involved moving salt's resources from
the file system to git.

Git was chosen because it's our standard and is supported very well. Many
automation tools have been written to interact with git to provide code
review, continuous integration, automated testing, etc.

Once salt is pulling it's data from git, git hooks can be written to generate
salt events for the reactor. In the demo `git repository`_, there is an example
of triggering highstates in different ways from different salt events. However
this is implemented will be heavily dependent on the environment it's being
configured for.

TODO: Start using generic script first to get something deployed.
salt-cloud -p, custom bootstrap

Because quality is important, the generic bootstrap.sh salt should absolutely
never be used. This is similar to formulas. They are okay for testing and
prototyping, but not for production. The demo `git repository`_ has an example
bootstrap for DitigalOcean which can be used as a starting point.

Using this `referral link` will provide a credit to new accounts which can be
used to try out the DitialOcean bootstrap script in the demo. The demo also
includes an example of having servers connect to an openvpn server in order to
access restricted internal resources, such as the salt master and syslog host.

The salt master should now be able to deploy a VPS. That VPS should connect to
a VPN server, authenticate to the master, run a highstate, and report results.
Additional highstates should produce no changes. If they do, please revisit
the section about quality. At this point, quality is not a goal but rather
it is an absolute requirement.


Introducing The Map
-------------------

Now that a single virtual machine can be deployed and configured using a single
command and all components that make it possible are well understood, it's time
to move on to automating salt-cloud.

The first step in this process is to become familiar with the `salt cloud`_
documentation. A virtual machine (or VPS) has it's configuration defined by
a profile, which has defaults for the VM (or VPS). That profile is backed
by a provider, which also has defaults for the profile being used.

Salt has the concept of "maps" which map a salt ID to a profile. As mentioned,
this can be one to one or one to many. I chose one to one but scale would require
one to many. In the map, multiple machines can be created using the same profile.

The `demo repository`_ uses a one to one mapping between profiles and machines,
because it was the most flexible option. At larger scale, this can easily become
overwhelming for a master without sufficient resources. Again, IDI is not a
product, but rather a new era of IT management with many components.

Using a map allows salt to define what servers should exist and what servers
should be destroyed. It allows salt to deploy a server using known defined
settings.

The next step for the demonstration is build pillar data that constructs one
profile per system merged with a set of defaults.

Example pillar data::

    cloud_nodes:
      defaults:
        digital_ocean:
          size:      512MB
          location:  New York 3
        proxmox_internal:
          storage:   slowdisk
          memory:    512 MB
          disk_cap:  10 GB
          cpu_count: 2
      digitalocean-nodes:
        'foo.domain.tld': {}
        'bar.domain.tld':
          location: Hong Kong 1
      proxint-nodes:
        'apt.domain.tld': {}

The important goal in this phase is to build a data structure that is scalable
for the environment it's being deployed inside of. Once this data structure is
assembled and normalized, it should start to resemble a nomalized database in
it's second normal form. (If you reached 3NF, you've likely gone too far... which
could be good or bad, depending on your situation.)

Once this structure is built, it's time to use it in some jinja templating. As
much as the over-use of jinja templating can cause confusion, this is the time
for it. In fact, this is an excellent candidate for using a python renderer,
which is open for a PR!

Example profiles using the example data for a one-to-one mapping::

    {% import_yaml 'cloud/nodes.sls' as cn %}
    {% set cloud_nodes = cn['cloud_nodes'] %}
    {% set defaults = cloud_nodes['defaults'].get('digitalocean', {}) %}
    cloud:
      profiles:
        {% for node, opts in cloud_nodes.get('digitalocean-nodes', {}).iteritems() %}
        digitalocean_{{ node }}:
          provider: digitalocean
          image: {{ opts.get('image', defaults['image']) }}
          size: {{ opts.get('size', defaults['size']) }}
          location: {{ opts.get('location', defaults['location']) }}
        {% endfor %}

Again, what works in different environments will be widely varied. What's
important is that a clean and scalable structure it defined. This structure
will become the API of your environment and will not be easily changed. Most
environments do not get the opportunity to refactor after this point. Everything
hinges on quality and forward-thinking engineering. You will not build the best
design and you **should not** build the most flexible design.


Bringing In Inventory
---------------------

While it might mean a lot of work, it is highly recommended to start re-deploying
servers in an environment in order to ensure they are reproducible. This also
implies all servers in an environment should be deployed using salt. This goal is
easily defined, but not easily attained. It takes a lot of testing and repetition.

Once this level of quality and control is reached, it's time to bring in Data
Center Infrastructure Management / IP Address Management (DCIM/IPAM). There are
many options for many situations. Some organizations may enjoy the flexibility
offered by the Device42 API and may even write their own frontend for it. Others
may prefer an open source product with an activite community such as Netbox.

It was easy to write salt states to deploy NetBox. There were already states for
nginx and uwsgi. Dependencies for a django application under uwsgi were simple.
Postgresql was a unique requirement in the environment so states for postgresql
were constructed and are as flexible as they need to be for their environment.

It can become incredibly time consuming to add an entire set of infrastructure
into an inventory management system, but this step is as critical as the rest.
Until an inventory manangement system can describe the exact state of an
environment, it cannot begin to control that environment with absolute authority.

The demo repository uses a special device type to indicate if a system should
be managed my salt, but this isn't a requirement.

Most DCIM/IMAP tools provide options for applying custom attributes to systems
and some have options for automatic allocations. It's upm to the system
administration group to decide what definitions are required.

Making DCIM/IPAM Actionable
---------------------------

Once DCIM/IPAM is deployed and populated, a process needs to be built to pull this
data down and turn it into a data structure. This structure should very closely
resemble the custom structure that was previously build.

Once a script is built to query DCIM/IPAM and build a data structure usable for
pillar construction, it's time to turn that into a salt module. That salt module
will eventually replace the static yaml structure that pillar previously used.

At this point, it should now be possible to create a machine in DCIM/IPAM, refresh
pillar data on the salt master, and use a map run to effect the desired changes.
If a server should be destroyed, salt will know. If a server should be created,
salt cloud will know what values it needs. Because the module is only useful to
systems (salt masters) with credentials, it's possible to assemble only the data
each minion needs and know nothing about the configuration of other nodes.

Salt uses providers to define authentication to VPS providers and to configure
certain defaults. Profiles are then used to define a specific set of creation
arguments. At scale, a single profile per instance may be a lot for the master
to handle. It's up to the system admins to figure out how to efficiently query
data and work within their resources. The `demo repository`_ uses a single profile
per instance.

These instances are defined in a map file. This file has the structure::

    <profile>:
      - node1.domain.tld
      - node2.domain.tld

The map file is what salt uses to know what needs to be created or destroyed.













make profiles dynamic from static imported pillar structure



create states to deploy netbox

make netbox reflect real state
  add one extra test.domain.tld entry


write a script to poll api and build same imported pillar data

turn into salt module

update profiles to read from module








reactor to execute map





Getting Help
------------

Nothing li




RAMBLES_
Salt's cache is enough to rebuild the git server; an environment with no
master can have a master deployed using *salt --local*. In my environment, it's
expected that all but a very select number of systems be re-deployed at least
once per year to ensure reproducibility and reliability of backups.





.. _Home Infrastructure: https://imgur.com/a/fjdoE
.. _git repository: https://github.com/MTecknology/inventory-defined-infrastructure
.. _infrastructure from the ground up: https://michael.lustfield.net/misc/ground-up-infrastructure
.. _long-term secure backups: https://michael.lustfield.net/linux/long-term-secure-backups
.. _referral link: https://m.do.co/c/6186604441bb
.. _salt cloud: #TODO
