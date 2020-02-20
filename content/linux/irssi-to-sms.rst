Irssi to SMS
############
:desc: Send Irssi alerts to your phone as text messages
:date: 2009-02-02 16:43
:tags: irc

It's no longer a secret that when I'm not in an active irssi session and
you hilight me, that I get a text message. By popular request, I'm
writing up an explanation to it.

1. Get irssi. When you're using it, you'll want to have it in a screen
session so you can always stay online. I already wrote a guide about
`Using irssi with screen and SSH`_.

2. Setup Scripts. Once you're doing this, you'll want to get
`screen\_away.pl`_ and `awayproxy.pl`_. I explained this in the
previously mentioned guide as well.

Descriptions from irssi.org:

screen-away.pl - set (un)away, if screen is attached/detached

awayproxy.pl - Sets nick away when client discconects from the.
irssi-proxy. If away gathers messages targeted to nick and forwards .
them to an email address.

They are pretty basic to setup and the comments explain things very
well. screen-away.pl is just a drop-in script. awayproxy.pl is one you
will want to edit.

3. Sprinkle in some magic. So you have these scripts working and you're
getting emails about hilights you receive while away. What!? You don't
have an expensive phone/contract to alert you? I don't either.

What I do have is unlimited text messaging. Hurray, we're not doing the
magic, someone else is.

http://www.livejournal.com/tools/textmessage.bml?mode=details

Example, if my number is 123-456-7890 and I'm a verizon customer, I
would set my email to 1234567890@vtext.com.

It's all incredibly simple, but without going through and doing the
research, it's a pain to put together. Have fun with this. :)

.. _Using irssi with screen and SSH: http://michael.lustfield.net/content/irssi-using-screen-and-ssh
.. _screen\_away.pl: http://scripts.irssi.org/scripts/screen_away.pl
.. _awayproxy.pl: http://scripts.irssi.org/scripts/awayproxy.pl
