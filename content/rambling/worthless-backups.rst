Worthless Backups
#################
:desc: Always verify that your backups are working before you need them
:date: 2008-12-30 19:11
:tags: mysql, backup, rant

How good are your backups?

I thought mine were pretty dang good. I found out otherwise. I had the
following two lines running nightly for my backups.

# Make MySQL backup

::

    mysqldump -u root -p "$(/.sql.pwd)" --all-databases | gzip > /var/mysqldump/mysql-$(date +%F).gz

# Delete old copies

::

    find /var/mysqldump/ -mtime +90 -exec rm {} \;

Anybody know what's wrong with that?

For 99% of Linux commands, this would be perfectly good syntax.
Unfortunately, this is one of those 1% times where things aren't the way
you expect them.

I was using -u root -p "$(</root/.sql.pwd)"

What I needed to be using was -uroot -p"$(</root/.sql.pwd)"

When working with MySQL in this syntax, you don't want a space when
passing in an argument.

I have a massive database issue and wasn't able to recover from it. I
tried to restore from the database backups. Problem is that I've been
creating backups of an error message. Worse yet, is I had no way of
knowing without actually going in and trying to restore from a backup.

Bottom line: TEST YOUR BACKUPS
