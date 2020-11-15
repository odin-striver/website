Final Network Design
====================
:date: 2020/11/12
:tags: TODO
:desc: TODO
:status: draft

Just over one decade ago (early 2010), I moved from a single VPS and laptop to
the beginnings of a home lab. Over time, that grew into a proper environment
ready to scale to most large-scale operations.

It was a painful decision, but all good things in this universe must eventually
come to an end. Here lies the obituary to my previous personal IT environment.

The Birth of a Lab
------------------

Back in my college days, I had a problem with dropping connections between
classes. This lead me to my first VPS, which lead to my first public website and
provided one of my paths into understanding systems and development.

That extra knowledge ultimately lead to being hired for a role I wasn't yet
prepared for. I jumped into a role where I was the only Linux administrator in a
company of 24,000 employees, supporting ~15,000 endpoints, and "`other duties, as
assigned`_," without any documentation.

? My first employment out of college was at a large enterprise where I was the
? only linux admin and was in charge of ~250 linux servers and ~10k endpoints. It
? was a pretty big trial by fire and I somehow managed to survive.

I had to learn a lot in a very short amount of time. Without a testing
environment at work, the most logical choice was to turn a server--from my
previous business venture--into a vm host for a lab. This enabled me to learn
and test things like automation--back in the days when the first autmation tools
were being born.

Growth Stage
------------

The original goal was to get a better grasp of networking concepts, which I
previously had minimal experience with. The lab became a place to experiment with
various solutions to $work problems without risk of breaking anything important.

Over many years, my small home lab grew into a small datacenter. It became one of
my prized creations and enabled me to do many amazing things. I could (and did)...

- Simulate a T1 (or any other connection speed).
- Test the effectiveness of anti-virus/malware tools with actual malicious code.
- Emulate any work environment I came across.
- Provide proof-of-concept solutions to complex problems.
- Host services for many open source projects (Debian, Nginx, SaltStack, etc.).
- Host team servers/projects.
- Host multimedia (stream my content from hotels).
- `Automate *Everything*`_.
- Design and implement "best practices".
- Host many Minecraft servers.
- Make everything redundant
- **Build my dream of the absolute most perfect enterprise environment.**

As I dug deeper and deeper, the desire for understanding grew exponentially. I
was continually able to do more with less effort. My automation skills grew to
the point that re-deploying (nearly) every (>40) server in my network took less
than a day.

Looking over the past 10-15 years, it's interesting to consider the motivations,
lessons learned, knowledge gained, mistakes made, losses, etc. It was enjoyable
to see how all of this came together to aid the final decomission.

Culmination
-----------

The final result of my home network included...

- Over Ten VLANs (prod, dev, admin, guest, dmz, iot, etc.)
- Development Hosts
- Apt Proxies + Local Apt Repo
- Bastion Hosts (one pair per VLAN)
- Salt Masters
- `Backup Host`_
- Git Servers
- Load Balancers
- Netbox (DCIM/IPAM)
- Name Servers (DNS)
- Pingtest Agents
- Web Servers
- Syslog Host
- FOSS Projecsts
- WLC, IRC, CICD, etc.
- (just about everything was redundant physically and virtually)




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
.. _other duties, as assigned: LinkToCV...&CreateACV
.. _Automated *Everything*: LinkTOIDI
