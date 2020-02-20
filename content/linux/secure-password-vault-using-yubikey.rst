Secure Password Vault Using Yubikey
===================================
:date: 2017/02/14
:tags: linux, security
:desc: How to secure a password vault using yubikey

Up until recently, my passwords were stored in a rather precarious manner. For
my birthday, I decided it would be a nice gift to myself to perform a complete
password refresh. This involved taking inventory of every password there was
any record or memory of and resetting it to unique and cryptographically random
password of random length--between ~25 and ~200 characters long. Now I have
reason to keep these passwords secure!

My Delay
--------

Most people that know me would be surprised to learn I never needed a password
vault. It was possible to avoid using a password vault by memorizing different
algorithms. This worked well because an employer and year/quarter could be fed
into the algorithm to produce work-centric time-based passwords.

This comes with some obvious issues. The first, and likely biggest, issue being
that I'm not able to memorize an algorithm that wouldn't reveal a good portion
of the pattern after ~5 cracked passwords.

The previous solution included coming up with a weak and easy algorithm as well
as a strong and difficult alterantive. It also included replacing each after a
few years of use. Unfortunately, forgetting old didn't fit into the equation.

The Vault
---------

The first step is deciding on a tool to use for the password vault. After doing
a review and audit of various tools, I settled on KeePassX. Although it uses
the same database format as KeePass2, I trust this tool significantly more.
Every person considering a solution for storing this much private data should
do their own research in order to trust their decision.

When doing the password refresh, no "current" password was moved to the vault.
Instead, new passwords were generated and services updated with the new password
before erasing old records.

In Comes LUKS
-------------

It should be obvious that a very strong password should be set on the keepass
database. Maybe less obvious is that it would be rather silly to give keepass
our full trust. Despite having reviewed the source code and knowing smarter
people have already done the same, it's still a good idea to provide an extra
layer of protection. Remember, this is data that should be kept *very* secure.

Being familiar with LUKS, I saw it as the obvious tool for this job. LUKS
provides the ability to store a tiny little file used for encryption that can
be backed up just like any other file.

LUKS also provides the ability to store headers in a separate file. The headers
include the eight available key slots as well as other data required to unlock
the encrypted volume. Headers can get a bit large but they are static so they
become virtually non-existent with differential backups. The encrypted volume
only needs to fit your password database and only needs to be large enough to
accommodate growth. This will be the size consumed for any differential backup
that includes the encrypted volume.

To build a playground structure similar to mine::

    mkdir -p ~/.luks/{crypts,headers,mnt}

To build files for encryption::

    dd if=/dev/urandom of=~/.luks/headers/vault bs=1MB count=2
    dd if=/dev/urandom of=~/.luks/crypts/vault bs=200KB count=1
    mkdir /.luks/mnt/vault

It's recommended to use *--use-random* to ensure a stronger entropy pool. When
creating the LUKS volumes, use a memorable and secure password. This will later
be removed and kept as a backup.

Making cryptography::

    sudo cryptsetup luksFormat ~/.luks/crypts/vault \
        --header ~/.luks/headers/vault \
        -s 512 --align-payload=0 --use-random

Now that the encryption stuff has been configured, some sysadmin stuff needs to
be performed. This is pretty basic so explanation will be skipped.

It's a root thing::

    cryptsetup open ~/.luks/crypts/vault \
        --header ~/.luks/headers/vault vault
    mkfs.ext2 -I 128 /dev/mapper/vault
    mount /dev/mapper/vault ~/.luks/mnt/vault
    chown $user:$user ~/.luks/mnt/vault

Closing it up (also root)::

    umount ~/.luks/mnt/vault
    cryptsetup close vault

Yubikey Encryption
------------------

The only reasonably secure way to trust the yubikey seems to be with the
challenge-response / hmac-sha1 option. This seems to accept an input password
up to 64 characters long, combine it with a secret, and produce a 40 character
long hash.

This was actually a pretty big concern for me because [0-9a-f]{40} wouldn't take
a computer too terribly much time to crack. After some thinking, it became quite
obvious that the simple solution was using the yubikey hash as a portion of the
complete password rather than the whole thing.

Pro-tip: Most of the tools I reviewed that used a yubikey as an authentication
factor only utilized this return value. That includes the 'yubikey-luks'
package in a few package repositories. Most tools didn't even include a sane
option for decryption.

Configuring the Yubikey:

1. Install and launch "yubikey-personalization-gui"
#. Select Challenge-Response tab, then HMAC-SHA1
#. Configuration Slot: 2
#. Configuration Protection: <strongly recommended | but not serial>
#. Require User Input: <recommend yes | this means touching key>
#. Click Generate, then Write Configuration

If there's any intention of using the key as a permanent resident, it would be
wise to reset slot 1 and ensure it does not respond to contact (user input).

Password Derivatives
--------------------

To produce a strong password for LUKS (the encrypted volume), the algorithm
used should produce a key that is both variable in length and character set.
As unlikely as it is that the yubikey is storing entered passwords and caching
generated hashes, yubikey is now closed source and there's absolutely zero proof
that isn't happening. This is describing paranoia, but addressing the silly fear
is quite easy.

My first algorithm looked much like this::

    salt='71'
    read -sp '' -t 20 vault_key
    len="${#vault_key}"
    luks_pass="${vault_key:5}$(/usr/bin/ykchalresp -2 \
        "$(sha256sum <<<"${vault_key:0:8}$salt${vault_key:$(($len - 5)):4}" | cut -d ' ' -f 1)")"
    # sudo cryptsetup open [...]
    unset vault_key luks_pass

    # sample_in:  YouAreCorrectHorse,ThatIs@BatteryStaple!
    # sample_out: eCorrectHorse,ThatIs@BatteryStaple!ac3bc63c4949f8c902ea49a7d9409f506c79bcdc

If able, coming up with a more secure algorithm than this would be a good idea.
If using this sample, at least change the salt. Verifying checksums of binaries
accessed of the script checking checksums would also be an excellent idea.

If the configuration was set to require user input, processing will stop at the
"luks_pass=" line and the yubikey will begin blinking green. Once the key has
been touched it will emit solid green until the hash is generated and returned.

Pro-tip: sha512sum produces a string too large for ykchalresp (64 limit)

Adding Factors
--------------

Knowing the final derived password means the original plain password can finally
be retired. If there is no backup of the headers file, this would be an
excellent time to make the copy and stick it away in a safe.

To add the yubikey-derived key::

    sudo cryptsetup luksAddKey ~/.luks/headers/vault
    # first enter the old (current) password
    # enter the derived password
    # enter it a second time

To delete the old key::

    sudo cryptsetup luksKillSlot ~/.luks/headers/vault 0
    # note: slot 0 is the first used and will have the plain password
    #       this can be verified using luksDump
    # enter the old password (for this slot)

Up to eight key slots are available for storing description keys. The same
process that was used above can be repeated to add additional devices with the
only exception being that no keys will be deleted.

Vault Access
------------

Now that all record of that key for copy/paste purposes and the clipboard has
been scrubbed, all that's left is to build a convenient script to make accessing
the vault a bit less painful.

I have included a very simple script to use as a starting point for your venture.

Final Thoughts
--------------

It would be nice to build a very strong and universal algorithm.

Most attacks that could hijack this derived password would also imply the
attacker has already made it into the system far enough to grab a copy of the
keepass file after the volume were mounted. If the intrusion is ever detected,
ample time will be available to do another password refresh using a new password
vault and encrypted volume.

Attachments:

|image0| `access_vault`_

.. _access_vault: /files/uploads/access_vault
.. |image0| image:: /files/icons/text-plain.png
