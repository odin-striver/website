SSH Tab Complete
################
:desc: Tab complete hostnames for ssh from known_hosts file
:date: 2009-12-05 21:12
:tags: ssh

I manage many servers as well as pop into a few other systems now and
then. I was getting somewhat irritated with typing out everything. A
search on Google showed many results. It seemed the most common command
to do this was this.

::

    complete -W "$(echo `cat ~/.ssh/known_hosts | cut -f 1 -d ' ' | sed -e s/,.*//g | uniq | grep -v "\["`;)" ssh

It does a pretty crappy job of actually scanning your known\_hosts file
and seems to only marginally do what it's supposed to. If you're like me
you also tend to be involved with rearranging many servers. This causes
issues to because the simplest fix for the key verification is to delete
the known\_hosts file. This means your tab complete won't work anymore.

My method is create a file (~/.ssh/hosts). On each line I add a host
that I want to exist in my tab complete. Example:

::

    server1.domain.com
    server2.domain.com
    server3.domain.com

It's white space that matters so you could have it all on one line and
just have a space between each if you want. Next, add this line to your
~/.bashrc file.

::

    complete -W "$(<~/.ssh/hosts)" ssh

I just added it to the end of the file. Either reload your shell or type
bash .

Now do ssh <tab><tab>. See how pretty that is? :)

Alternatively, you could edit your ~/.ssh/config file to include aliases.

~/.ssh/config::

    # parens
    Host parens
        Hostname parens.domain.tld
        User michael

    Host fw
        Hostname firewall.domain.tld
        User admin

If you have the complete command available, then it's likely that any Host in
this file will already be auto-completed using tab. This is done using the file
/usr/share/bash-completion/completions/ssh.
