Nginx Book Review
#################
:desc: Another typical Packt book review
:date: 2010-08-26 15:42
:tags: nginx, reviews

Most anyone reading this already knows me. My name is Michael Lustfield.
I'm running the servers of a starting web development company called
Kalliki Software. We've been in business for a little while now. When we
started we had an Apache Web server with less than one half a gigabyte
of RAM. After three websites we were feeling the burn. The Apache web
server was taking us down. We didn't have the resources to grow out. We
needed to grow up. I turned to the two leaders, Nginx and Lighttpd.
After investigating each I easily settled on Nginx. We were then able to
handle upward of 10 websites on that exact same configuration. The
change was amazing. After all of my experiences, I absolutely would not
recommend Apache for anything.. ever.

I was asked to review a book called "`Nginx HTTP Server`_\" by Clément
Nedelcu. It's been published by Packt Publishing.

At the point of being asked to review this book, I'd moved into
customized packages of Nginx for distribution which include bug fixes
and feature additions. I'd also become the second administrator of the
Nginx wiki. I also provide support online.

Prior to this review, I'd read books by Packt Publishing but never
actually considered much about the publisher. After reviewing them I
realized that they focus on producing books about open source. More
specifically, they produce books authored by the FOSS community. The
book I as asked to review was about the Nginx HTTP Server. Nginx is, as
the title states, an HTTP server. This is similar in nature to Apache.
The difference is that Nginx is build for high efficiency. This book was
meant to help users into its use.

This book is obviously written for someone with no administrative
experience. In fact, it starts out the first couple chapters discussing
remote administration and command line basics. It also covered the
installation and configuration of nginx, nginx modules, and php/python
processes. This book was basically written in a way that it could guide
a Windows 95 user into configuring and setting up a high performance web
server with Nginx.

The language of the book was of particular interest. The author is very
obviously not a native English speaker but was still able to clearly and
accurately explain everything. It boiled down to a lot of grammar
mistakes which can easily be ignored by someone less pedantic that
myself.

The book itself covered many features. Some were funny to know existed
and others were extremely useful. The best part is that you can easily
make the binary of Nginx completely exclude these features which many
will never use. The book very clearly explained this process in the
second chapter.

From a more experienced standpoint, I found many issues in the book. The
minor suggesting “apt-get install build-essential” for dependency
resolving of custom builds. I also noticed that the author suggested
compiling things on a system rather than installing from a repository.
From the point of support, this is bad. The book was written for
beginners and compiling a package is not a beginner task.

The author suggested that not being able to read ".htaccess" files was a
bad thing but in reality this is an amazing performance gain by Nginx.
The author also suggested using an if statement in many places.
Unfortunately, an if is a horrible thing to use. 99.9% of the time there
is a much better way to handle it.

The author also had poor examples of using root and index directives.
Any directive should be placed as high as possible in the block
hierarchy. This prevents a lot of duplication. For example, if every
website has the same indexes, then put the line in the http block once
and nowhere else. This is minor for smaller websites but causes issues
later.

Almost any issues I found in this book I have already outlined in a
`Pitfalls`_ page on the `Nginx Wiki`_. If you follow that after reading
the book, you'll be miles and miles ahead of most online guides.

I do with the book had better line wrapping as some thing got confusing
to understand. This is especially true when a directive is split onto
two lines. I hope that knowing this in advance would enable a user to
avoid any confusion.

Aside from the issues I've mentioned I actually found that the book was
very good. It could take nearly anyone with any technical skill and make
them understand how Nginx works and what it does. This is extremely
important. Understanding how Nginx works is even more important than the
style issues described above. As I said, a `Pitfalls`_ wiki page prior
to even reading this because the mistakes are scattered across the whole
Internet.

If you want to ditch Apache or IIS but are entirely confused about
anything else, this book will give you an amazing boost in the right
direction.

As for configurations for specific applications, there's also a Wiki
page about that. Check out the `Applications`_ section of the Nginx Wiki
to find configurations that will be nearly drop-in for whatever you want
to run. It's a growing collection and includes applications such as
Drupal, Wordpress, Mailman, Redmine, MediaWiki, etc.

After reading the "Nginx HTTP Server" book and the Nginx Wiki, you
should be able to do just about anything in Nginx. Except for writing
your own modules which is only lightly touched in the Wiki.

Packt Publishing has generously offered a `Sample Chapter`_

.. _Nginx HTTP Server: http://www.packtpub.com/nginx-http-server-for-web-applications/book?utm_source=profarius.com&utm_medium=link&utm_content=blog&utm_campaign=mdb_004258
.. _Pitfalls: http://wiki.nginx.org/Pitfalls
.. _Nginx Wiki: http://wiki.nginx.org/
.. _Applications: http://wiki.nginx.org/NginxConfiguration#Applications
.. _Sample Chapter: https://www.packtpub.com/sites/default/files/0868-chapter-3-basic-nginx-configuration_1.pdf
