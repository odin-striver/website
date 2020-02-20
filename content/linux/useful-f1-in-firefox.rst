Useful F1 in Firefox
####################
:desc: Make the F1 key in firefox useful for something
:date: 2010-09-13 18:26
:tags: tips

Do you ever use F1 to bring up help pages in Firefox? Do you find this
feature useful? Do you like rhetorical questions?

Personally, I've never found this F1 function useful or helpful. The
times I wanted some help from it I wasn't able to get the help I needed.
So then this becomes a pointless feature. I bumped it some so I kinda of
got irritated.

Here's what I did to make it useful:

1. Open a tab
#. Go to about:config
#. Search for app.support.baseURL
#. Right click
#. Modify

You'll notice a question mark (?) at the end of that. This is because
firefox wants to add "firefox-f1" to the end of the URL. The ? changes
the extra text to part of a query string. The cool part is that tacked
on to the end of an existing query string, this little piece is usually
ignored. You could alternatively use an ampersand (&) if you know for a
fact that a query string is already formed.

The result: an F1 hot key to a website you actually care about.
