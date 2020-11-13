Final Network Design
====================
:date: 2020/11/12
:tags: TODO
:desc: TODO
:status: draft


  7 It was a painful decision, but all good things in this universe must eventually
  8 come to an end. Here lies the obituary to my previous personal IT environment.

Over many years, my small home lab grew into small datacenter. It became one of
my prized creations and enabled me to do many amazing things. Unfortunately, all
things must eventually come to an end.

Looking over the past 10-15 years, it's interesting to consider the motivations,
lessons learned, knowledge gained, mistakes made, losses, etc. It was enjoyable
to see how all of this came together to aid the final decomission.

Why Build IT
------------

The lab was originally just a cheap desktop running VMWare Server and another
desktop running pfSense. I felt enlightened when I figured out how to move the
pfSense box into a virtual machine and drop down to a single physical host.

My first employment out of college was at a large enterprise where I was the
only linux admin and was in charge of ~250 linux servers and ~10k endpoints. It
was a pretty big trial by fire and I somehow managed to survive.

The original goal was to get a better grasp of some basic networking concepts
which I previously had no experience with. It became a place to experiment with
various solutions to $work problems without risk of breaking anything important.

Eventually, I had cause to learn how to work with cisco switches and added that
to the collection. Over time, the lab became a collection of every best practice
that I came across, as well as others that I developed.

The more I learned about automation, the more I dreamed about the potential it
has. I started to dream about `Inventory Driven Infrastructure`_.

The Culmination
---------------

The final result of my home network included...

- Over Ten VLANs (prod, dev, admin, guest, dmz, iot, etc.)
- Development Hosts
- Apt Proxies + Local Apt Repo
- Bastion Hosts (one per VLAN)
- Salt Master
- `Backup Host`_
- Git Server
- Load Balancers
- Netbox (DCIM/IPAM)
- Name Servers (DNS)
- Pingtest Agent
- Redundant Web Servers
- Syslog Host
- FOSS Projects
- WLC, IRC, CICD, etc.



Open Source Involvement
-----------------------


Professional Development
------------------------

FOSS Growth into Infra
----------------------

Personal Growth
---------------

Vision Reached
--------------

Personal Overload
-----------------

Final Decision
--------------

Decom
-----

Relationships
++++++++++++++

Many personal relationships were established throughout the years. Some were
with key members of companies, some were with enthusiasts, and all were with
humans (... and software).

During Decom, many projects had to meet their final death. Some things found an
archive while others found /dev/null. Without having established these
relationships, the projects still serving value would have been turned off,
leaving users with no alternatives.

Having established and maintained healthy relationships with other users has
made my experience in pone source much more fun and productive.

Checklist
+++++++++

It is impossible to measure just how important checklists are.


Physical Design
---------------

<pics / description>


.. _Backup Host: https://michael.lustfield.net/linux/long-term-secure-backups
.. _Inventory Driven Infrastructure: TODO
.. _TODO: https://michael.lustfield.net/misc/ground-up-infrastructure

