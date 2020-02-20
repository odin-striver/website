Upgrading to 9.04 and Ext4 Remotely
###################################
:desc: Upgrading to ext4 through an ssh connection
:date: 2009-04-07 19:05
:tags: file systems

WARNING! Do Not do this to your systems. This is for informational
purposes only. Do this in a virtual machine only. If you do this outside
of a virtual machine, your computer will blow up and you will die.
You've been warned.

I did in fact do this over SSH which was not safe and not smart. That
fact that I did it does not mean any intelligent or knowledgeable person
should do so. In fact, they probably wouldn't consider it.

Now, if you do decide to do this such thing without heeding my warning
about your own death, then it's time to stop joking. DO NOT follow other
guides. I've read many other guides and all of them left out at least
one very important step. All of them left out one step listed on the
Ubuntu website which renders your system unbootable if not done.

First off, we'll do the more stable upgrade. If you want to use Ext4
then you should be using Jaunty Jackalope (9.04). To get to Jaunty, we
first want to update your system to ensure a smooth transition.

sudo aptitude update && sudo aptitude full-upgrade

Now to upgrade to Jaunty.

sudo do-release-upgrade -d

Once this completes, reboot and you will be running the Beta version of
Jaunty. Read that again, Beta, not officially released yet.
(http://wordnetweb.princeton.edu/perl/webwn?s=beta | second
adjective)

Now to upgrade from Ext3 to Ext4. Do not stop half way through the
process and read this whole thing first before starting.

To start, we'll do this to non-vital drives. This means not /home,
/boot, or /. Anything else is game for the moment. Run 'mount | grep
/dev/sd' to see what partitions you have mounted. Your output will look
like this.

::

    michael@panther:~$ mount | grep /dev/sd
    /dev/sda5 on / type ext3 (rw,relatime,errors=remount-ro)
    /dev/sda1 on /boot type ext3 (rw,relatime)
    /dev/sda7 on /home type ext3 (rw,relatime)
    /dev/sda8 on /var/vbox type ext3 (rw,relatime)

According to what I stated and this list, I will only do /dev/sda8 for
the moment. We first unmount the device.

::

    sudo umount /dev/sda8

Now we'll set some flags on the device. Almost every guide you will see
will set different flags and I'm sure this isn't the absolute best.
However, I did grab these from a partition created as Ext4 from the
Ubuntu install CD so I assume they're set for a combination of stability
and performance.

::

    sudo tune2fs -O has_journal,ext_attr,resize_inode,dir_index,filetype,needs_recovery,extent,flex_bg,sparse_super,large_file,huge_file,uninit_bg,dir_nlink,extra_isize /dev/sda8

As a side note, I've seen it where the
ext_attr,resize_inode,needs_recovery options aren't supported. I
haven't seen any issues with omitting these.

Now that I set the options on this device, I need to run an fsck on the
drive.

::

    sudo fsck -pf /dev/sda8

The flags here:

::

    f - forces the check even if the file system looks clean
    p - automatically fix (preen) the file system

Now we need to edit /etc/fstab to reflect the change.

::

    sudo vim /etc/fstab

    ### Find the line relating to the partition you changed

    # /var/vbox was on /dev/sda8 during installation

    UUID=3311b3e1-3cfa-48a9-8911-f3ac30bc0afb /var/vbox ext3 relatime 0 2

    ### And change the ext3 to ext4

    UUID=3311b3e1-3cfa-48a9-8911-f3ac30bc0afb /var/vbox ext4 relatime 0 2

    Save/Close - :x

You should reboot at this point to make sure everything is working. If
everything is going great, then it's time to move onto the rest of your
partitions.

Please note: this is where things get dangerous and your system could
stop booting. It is generally recommended to not do this to the root or boot
partitions.

Now, we'll tune the next partitions. I did this on /dev/sda1, /dev/sda5,
and /dev/sda7. Refer to the mount listing for a reference.

::

    sudo tune2fs -O has_journal,ext_attr,resize_inode,dir_index,filetype,needs_recovery,extent,flex_bg,sparse_super,large_file,huge_file,uninit_bg,dir_nlink,extra_isize /dev/sda1

Edit /etc/fstab as stated above to reflect these changes.

At this point, be nervous. This is a point that was missed in every
other guide I read. You need to reinstall GRUB or it won't be able to
read your partitions anymore. Make /dev/sda reflect your setup. More
than likely, /dev/sda is what you want; unless you want your MBR on your
second drive. You most likely don't want to install it to a partition.
Remember, you're installing GRUB to the MBR, not creating files on your
partition.

::

    grub-install /dev/sda

This little command will bring your system from not being bootable to
being great. I believe you get one reboot before this must be done. When
you reboot, your system will do an fsck on these partitions and convert
them to Ext4. At this point, the drives are still Ext3.

Now that you've rebooted after installing GRUB to the MBR, do the
grub-install command again and reboot again. It's a quick little thing
that I've seen help systems.

CONGRATULATIONS! If you're system is still running, then you now have
the Ubuntu 9.04 running Ext4.

Your existing files are not using extents however. Your old files will
still behave like Ext3 files. New files will take the behavior of Ext4.
This will change after you do a defragmentation of your Ext4 file
systems. On-line defragmentation is not supported yet and is very
unstable. So unstable that I'm not even considering trying it yet. Once
Ubuntu officially supports it, I will indeed post something about it.
