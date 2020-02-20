Moving from personal mail server to Gmail
#########################################
:desc: Giving up self hosted email and moving to Google Apps
:date: 2009-06-09 12:07
:tags: email

I was hosting my own email server for about a year. I enjoyed the fact
that I had full and complete control over the entire mail server. I
enjoyed being able to fine tune everything to fit my needs exactly. I
was doing this for about 1.5 years.

Unfortunately, there were a few things I couldn't control that really
killed the fun of running my own email server. First of all, dealing
with the people complaining that it's not how they want it weighed on
me. Aside from that there were also power outages, hardware failures,
software hangs (from power dips), firewall/router deaths, modem spasms
(now very frequent), etc. Not only that, but I only had 1mbit upload
available and 1.5mib max available at about $100/mo more.

What it came down to is that running a mail server just isn't for me
given my limitations. I needed an alternative and I found one. There is
this thing called Google Apps (google.com/a) that is capable of hosting
your domain email for you.

I decided to give it a shot. It's not a quick or idiot proof process,
but it was worth the effort.

What you first need to do is sign up for `Google Apps`_. When you click
sign up, make sure to click the "Standard Edition" link to avoid them
wanting money. If you already have your own domain then you enter it and
procede with signup. Otherwise you can purchase a domain through Google.
It doesn't matter. They give you pretty easy to follow instructions to
setup your DNS to point MX and CNAME records to them instead of wherever
you're currently hosting from.

After you setup everything, you need to sync your email. I just set up
two different IMAP accounts in my email client (claws-mail) and
dragged/dropped the messages from my own server to the other.

Gmail handles email with tags and not folders. This is really the point
of this blog. Your mail client will recognize these tags as folders, but
Gmail doesn't handle them as such. This can make things pretty
interesting.

To start, make sure you archive all of your email. Anything in Trash
will be deleted after 30 days. Now we need to make some tags that our
mail client will use. Make sure you prefix all tags with [Gmail]/.
You'll see why later. At a minimum, you need to have [Gmail]/Archived,
[Gmail]/Drafts, [Gmail]/Queue, and [Gmail]/Trash. I also have a few
others such as [Gmail]/Saved, [Gmail]/Ubuntu, and [Gmail]/Kalliki. The
last three are personal tags that represent folders I want to have
available.

If any [Imap]/ tags exist, delete them. They're ugly and useless. You
may need to delete them after doing all of this too.

When it comes to a mail client, I use `Claws Mail`_. It's the only
client I've found with the features required to do this. You will need
to setup your connection to Gmail the same as as anything else. In order
to be able to do this at all, you'll need to log into your account, go
to "Settings > Forwarding and POP/IMAP" click "Enable IMAP" and click
"Save". This will allow you to access your account with claws-mail.

After you've set up the basics in claws-mail, you will see your standard
Inbox, Sent, Trash, etc. You will also see a [Gmail] directory with all
the tags you created underneath it.

Isn't that just ugly? Everything in a sub directory... Ya, let's fix
that.

Remember, I'm referencing claws-mail, not Thunderbird. I don't know if
Thunderbird can do this at all.

Go to Configuration > Edit Accounts. Select your account and click Edit.
Check out the Receive section. In this section you will see an "IMAP
server directory". In this area you will add "[Gmail]" (w/o quotes of
course). This will get rid of the [Gmail] directory and all your tags
will show up as directories at the root level. This is already MUCH
nicer to look at.

We don't want to stop there, but for now. Click Apply, OK, Close. Right
click the Account name in your folder list, this is the account name and
should show (IMAP4) beside it. From the right click menu, select
"Rebuild folder tree". This will make things easier to look at.

You have a "Sent Mail" folder and a "Sent" folder. "Sent Mail" is
created by Gmail and this is the one we want to copy sent mail to. Right
click "Sent Mail" and click Properties. Across from "Folder Type" select
"Outbox" and click Apply, OK. You can now delete the "Sent" folder as it
no longer matters. You will now use the Gmail's "Sent Mail" instead.

You also have an "Archived" folder and a "Trash" folder. You will set
your client to move deleted items here later. If Right click "Archived"
and click Properties. Set the Folder type to "Trash". Click Apply, OK.
This will make sure when you delete something, it's marked as read. The
actual directory it goes to when deleted is handled down this page.

Go back to your account properties. Configuration > Edit Accounts \|
Account \| Edit. This time, go to the Advanced section. You will see a
box titled Folder. This is a big deal with what we're doing. Check all
four boxes. Click the Browse button and select the appropriate folder.
~!Read this word for word!~ You want to make sure everything is filed
with a [Gmail]/ tag. Sent messages should be going into the "Sent Mail"
folder that Gmail uses. Deleted messages should be going in the Archived
folder you created with the tag.

By sending mail to Archived, we avoid Google's 30 day Trash deletion
nuisance.

Here is a sample of what I have:

::

    Put sent messages in: #imap/Profarius/[Gmail]/Sent Mail
    Put queued messages in: #imap/Profarius/[Gmail]/Queue
    Put draft messages in: #imap/Profarius/[Gmail]/Drafts
    Put deleted messages in: #imap/Profarius/[Gmail]/Archived

Note that Profarius is the name of the account. It will be whatever you
named yours. The rest should be identical. Make sure the [Gmail]/ part
exists in EVERY line.

When you delete something, it will instead be archived. No need to worry
about automatic deletion. If you really do decide you have email you
want to delete, you can drag it to the Trash. After 30 days, if you
haven't realized you really do need that message, it will be gone. This
avoids that "holy crap I needed that" problem.

It's possible that you have two "Trash" folders. If this is the case,
it's because claws-mail created one and Gmail created one. Just drop a
test email into one and check your Trash on Gmail. If the message is
there, delete the other Trash folder and move your test message back
wherever you want it. If it doesn't show up, then repeat the process
with the other directory, just to make sure.

The last step is to subscribe to ONLY the folders you care about. Right
click the account name, go to Subscriptions, click Subscribe, check
Search recursively, click Search. You can use this process to subscribe
to specific or all folders. My personal preference it to subscribe to
all and specifically unsubscribe from what I don't want.

I find Spam useless because I don't want to see spam. I find Starred
useless because I don't ever flag messages. I have [Gmail]/Saved to save
important messages. Of course if you flag messages, you could use this.
One folder that you may as well not bother with is "All Mail" because
it's just a duplication of everything else, including what you're
keeping in Archived.

I've tried to do this setup under other mail clients, but they don't
seem to have the features and flexibility required to do this.

You should now have your mail client working perfectly and beautifully
using Google's 'tag your email instead of sort it' approach. This is the
exact approach I took to host my email on Google using my domain. It
took me about 15hr to finish tweaking things to make it work just
perfect and I didn't figure out the last little piece until I was
writing this. Overall, I'm very happy with the result and I do feel the
hassle was worth the reward.

Of course, if you're going to have over 7GB of email, you will need to
split things between multiple user accounts or stick with your own
server. You can use this exact same process To have Archived on one
account, Inbox on another, etc. You just can't apply multiple tags.

I hope this helps someone out there!

By request, also on `Claws Wiki`_.

.. _Google Apps: http://google.com/a/
.. _Claws Mail: http://www.claws-mail.org/
.. _Claws Wiki: http://www.claws-mail.org/faq/index.php?title=Using_Claws_with_Gmail
