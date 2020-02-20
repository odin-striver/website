Ground Up Infrastructure
========================
:desc: Rebuilding an entire infrastructure from scratch after a fat finger
:date: 2016/01/02
:tags: infrastructure, debian, networking, virtualization


I've been working with a company that recently lost a very large amount of their
infrastructure. Not only were servers lost, but also backups, application data,
and much more. Unfortunately, I'm not at liberty to share too many details, but
I am able to say that it was the situation your worst nightmares are made of.

Very recently, I also lost all of my personal infrastructure. I lost all virtual
machines, VM hosts, networking configuration, router configs, firewall rules,
backups, the other backups, the third set of backups, AP configs, etc. It was
rather brutal. The only thing I got to keep was my laptop and anything I've put
on a public service.

Disaster Recovery
-----------------

First of all, both situations had very different causes. One was malicious and
the other was entirely PEBKAC. The company I've been working with was quite
fortunate and, because of some encryption, the tapes were able to be recovered.

The lesson learned here is that just having a disaster recovery plan and testing
it isn't enough. You need to test it from *NOTHING*. Don't test restoring a VM
onto a hypervisor. Test it by building a new UCS fabric interconnect from only
what you would have available if your building disappeared this second.

In my personal situation, there was *nothing* to go back to. So, I got to build
my personal infrastructure from the group all the way back up to the top. How
this happens is a question I've been asked many times. Instead of trying to
explain it each time, I decided I'd prefer just write about it and hope that the
information is valuable to others. If I provide poor information, I hope I get
yelled at so that I can correct any mistakes.

The Basics
----------

Where a person (or organization) chooses to start rebuilding from scratch is
entirely up to them. In a larger organization, I would expect to see each piece
managed by a separate team that I would hope are communicating effectively.

The basics that nearly every infrastructure has:

* Switches
* Routers
* Physical Servers
* Virtual Servers
* Hypervisors
* Access Points
* Backups
* VLAN's
* Backups
* Configuration Management Systems
* Git Server

Yes, as a matter of fact, I *do* consider git and salt (configuration management)
to be critical pieces. You should too. Having all salt data held within git is
the only reason I was able to get things back up as quickly as I did.

My preference was to start with the switch configs. Thanks to salt, I just copied
and pasted the previous configuration I had on my laptop. Next up was the VM Host.

Preparations
------------

Before getting started, I connected to my cable modem directly with my laptop and
then downloaded a proxmox and pfsense ISO. With my particular setup and the order
this particular rebuild was happening in, those were the "off-line" resources I
needed to aquire.

VM Host
-------

I chose proxmox because I have a lot of experience with it and it runs on Debian.
If you're not me, it might be wise to explore your options. I also chose to
install proxmox entirely off of the network because it couldn't have reached the
Internet anyway and I didn't want to deal with the cabling or switch port
configurations.

The proxmox installer is pretty dumb. You select a disk, IP settings, and that's
pretty much it. After the installation finishes, it's time to configure it. Since
this is Debian and I'm familiar with the way proxmox interacts with it, I went
directly into `/etc/network/interfaces` and modified it to be exactly what I
wanted to be there. I also got to edit udev rules to modify ethX assignments.

WAN:

* WAN -> eth2
* eth2 -> vmbr1
* vmbr1 -- <WAN_IF_on_pfSense>

LAN:

* eth0 -> bond0
* eth1 -> bond0
* bond0 -> vmbr0 (802.3ad)
* vmbr0 -- <LAN_Interfaces_with_VLAN_Tag>

Once configured, the VM host could be reattached to the switch without troubles.

I connected to the proxmox web interface from my laptop, logged in, and created
a VM (not container). This VM had one interface for vmbr0 and one for vmbr1. This
is the *ONLY* system that ever does anything with vmbr1 or eth2. They are off
limits to every other system including the host itself. There is one additional
NIC attached per VLAN with the appropriate VLAN tag.

Router
------

Now that the VM Host is up and has the VM created, it's time to spin up a virtual
router. After uploading the pfSense ISO, I attached it to the VM and booted it up.
The pfSense installation is pretty straight forward. Remember to double check the
MAC addresses to ensure they match the interface you're configuring.

I had to temporarily enable DHCP on the LAN interface while getting things
rocking, but eventually stuck all servers into their own VLAN without DHCP and
removed DHCP from LAN. DHCP (and DHCPv6) was only enabled on the guest, non-guest,
and lab networks. Using static IP addresses means a faster boot time, but it also
means less attack surfaces.

When configuring VLAN's, be careful what you choose. If you're too restrictive up
front, you'll run yourself into walls. If you're too open, you'll do the same.
However, if you're using strictly IPv6 on a properly deployed, it's entirely
irrelevant. You'll have exactly one /64 per subnet.

Switch
------

If I didn't have a switch configuration already available, this is where I would
have started working on the switch. I configured an access port to be in the
correct VLAN and connected my laptop to it. Then I grabbed a DHCP address.

Once I was able to grab this address and talk to the Internet, I decided it was
time for sleep. It was already 05:00 by this point.

The only thing that was really special was having a pair of switch ports set up
with LACP set up as a trunk port as well as another trunk port for my access
point. The remaining ports were set up as standard access ports that were set to
their correct VLAN.

Temp WLC
--------

So far, I've been dealing with physical network connections. About now, I was
getting quite frustrated with being connected to a wire.

I deployed a temporary Wireless LAN Controller (WLC) VM to get the AP configured.
Once deployed, I let the software configure the AP, configured the correct VLAN
per SSID. I didn't get fancy at this point because it's all temporary.

OpenVPN
-------

Now that I was comfortably working on my sofa, I decided to configure OpenVPN on
pfSense. If you're going to do this, I strongly recommend installing the "OpenVPN
Client Export Utility" because it makes life happy and grand.

Dynamic DNS
-----------

This infrastructure is at a residental address and the ISP available no longer
offers any static addresses. I set up DynDNS for the public address. Thankfully,
this doesn't change unless the cable modem loses power.

Everything is connected to a UPS that has been "slightly" modified to last
"slightly" longer. This takes the appearance of two very large deep cycle
batteries that could run 100% of my infrastructure (modem, VM host, wireless AP,
etc.) for over a full day. That's more than sufficient in  my book. :D

I happen to use Hurricane Electric for DNS. Within their interface, you can
optionally select a record for Dynamic DNS. Afetr enabling it, there is a refresh
icon on that line that you can select to generate a random key. Within pfSense,
while creating the DynDNS entry, you'll need to configure these options:

* Service Type: he.net OR he.net (v6)
* Hostname: <fqdn_of_dyndns_entry>
* Username: <fqdn_of_dyndns_entry>
* Password: <generated_key>

IPv6
----

My ISP only offers a /64 for the entire network. If only they'd heard about RFC's
and the value of following them. I need a minimum of a /60 for my network. This
forced me to ignore native IPv6 from my ISP, I wound up using Tunnel Broker to get
the /48 that my ISP should be providing.

VM Template
-----------

Now it's time to build a VM template for the virtual machines that will become
the production image. To get started, I downloaded a copy of the Debian 8 template
through the proxmox web interface.

We'll assume the file is named /tmp/debian-8.0-standard.tar.gz. To open this
archive for editing:

1. mkdir /tmp/d
#. tar -zx -C /tmp/d -f /tmp/debian-8.0-standard.tar.gz
#. mount -o rbind /dev /tmp/d/dev
#. mount -t sysfs none /tmp/d/sys
#. mount -t tmpfs none /tmp/d/tmp
#. mount -t proc  none /tmp/d/proc
#. cp /etc/resolv.conf /tmp/d/etc/resolve.conf
#. chroot /tmp/d /bin/bash

Next up, we want to modify the template. Things I did:

1. aptitude # remove any excess cruft you don't want
#. aptitude install vim screen salt-minion apt-transport-https
#. echo 'master: $fqdn_or_ip' >/etc/salt/minion.d/master.conf
#. salt-call state.sls sys.files.salt,sys.files.apt
#. aptitude update; aptitude upgrade; aptitude clean
#. aptitude purge -y --purge-unused ~c
#. dpkg-reconfigure locales
#. /etc/init.d/salt-minion stop
#. rm -Rf /etc/salt/minion_id /etc/salt/pki
#. cat /dev/null >/etc/resolv.conf; exit
#. rm /tmp/d/root/.bash_history
#. umount /tmp/d/*/*; umount /tmp/d/*
#. tar -czp -f /tmp/debian-8-<your_tag>.tar.gz * -C /tmp/d

This new tarball just needs to be uploaded to your VM host.

Side note, the packages I had installed went from 404 to 191 after removing what
I considered extra cruft. That's 213 packages times the number of servers that
won't need to be updated.

Salt Master
-----------

It's exciting to finally be at this point. It's pretty much pain free from this
point on. In my opinion, configuration management is one of the absolute critical
pieces of every infrastructure and my choice is salt. I deployed the new template
and installed salt-master on it. Then I configured `/etc/salt/master.d/main.conf`.

For the moment, I'll point salt-master at `/srv/salt/{states,data,pillar}/`. Then
I wrote the states that now manage salt-master configs.

Git Server
----------

Next up is the git server! Deploy the VM template, create salt states to configure
your choice of a git server. My choice was gogs (GO Git Service). It feels like a
somewhat clunky version of gitlab with all of the feauters that I actually use
but has a massively smaller footprint.

Once this was up, I created a system account and group so that the salt master
could access the salt states. Then I moved `/srv/salt/{states,data,pillar}` to
their own repositories that the salt master could access. Then I modified the
master config (using salt) to point at the git server instead of the local file
system. Last, but not least, `rm -rf /srv/salt`.

Permanent WLC
-------------

At this point, we're ready to deploy every single server by pushing commits to
the git repositories. This is where I destroyed the old temporary WLC and created
a new WLC server.

Security
--------

Hurray! I've now described exactly what my home network looks like and how to
build it. Should I now be paranoid about getting attacked? Yup, absolutely! We all
need to be paranoid all of the time. Keeping software in use hidden isn't anything
I've ever considered to be confidential information.

On that note, one level of paranoia that I love is having a special VLAN for
accessing the server network. This means that, even if you get connected to my
non-guest network, it still doesn't mean you can talk to my server network.

I'm also pretty strict about firewall rules. Every connection in to or out of any
VLAN needs an explicit firewall rule.

There are billions of things a person can do to decrease security risk. I'd love
to discuss many of them and might just need to write a separate blog post about
it. The bottom line, though, is that security by obscurity or secrecy is not
reliable security. If you build a strong and secure infrastructure, you should be
able to feel confident explaining the intricacies of your network. Unless, of
course, you're paranoid.

What Comes Next
---------------

After finishing all of that, I deployed a logging server and an apt caching proxy
followed by writing salt states to make servers report to them. Next up is the
backup server and configuring external backups.
