Debian NEW and YOU
==================
:date: 2019/04/01
:tags: debian
:desc: TODO

There's been some debate recently about whether or not Debian is still relevant
in today's fast-paced development world. A large majority of these discussions
seem to focus on the effort it takes to get a package into the Debian archive.

Why are these extra steps still required, and what do they mean to the Free Open
Source Software (FOSS) community as a whole?

Debian NEW
----------

For those not familiar with "Debian NEW", it is a queue that is used to hold
uploaded packages that were not previously in the archive until they have been
reviewed by the "FTP Masters" team. The primary roles of this team is to ensure
copyrights and licenses are properly summarized in a special "copyright" file,
and to ensure there are no major package defects.

For anyone using a Debian-based distribution, this file is present for all
installed software at ``/usr/share/doc/<package>/copyright``.






FTP Masters ensure a project is properly licensed
- review d/copyright
- can be rebuilt using FOSS tools
- uses only FOSS licenses
- does not use conflicting licenses (openssl/gpl)

DDs work with upstream when licensing problems are found

Gitea as example

Potential problems of unlicensed / incompatible licenses

Why other distributions don't bother? (it's hard)
- but they still benefit from Debian
