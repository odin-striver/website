Book Review - Nginx Module Extension
====================================
:desc: A typical review of Packt books
:date: 2014-03-14
:tags: nginx, packt, review

I apparently do enough work with Nginx that people keep asking me to review
things. In this case, Packt asked me to review another book called "Nginx
Module Extension." Well, a decent module development book doesn't exist, so
I'm rather excited to dive in!

While Reading
-------------

Instead of just a summary when I'm done, I want to also include my reactions
while reading.

Table of Contents
~~~~~~~~~~~~~~~~~

I hope I'm missing something, but it seems that the first 82 pages of this book
are focused on teaching you the basics of Nginx. That doesn't leave much for
discussing the actual module development. My assumption from the cover was that
we finally had a book explaining module development. I guess another book that
explains getting started would be okay.

Preface
~~~~~~~

The preface mentions that:

    This book is for advanced users such as system administrators and developers
    who want to extend Nginx's functionality using its highly flexible add-on system.
    We look at the existing modules available and how to compile and install them,
    along with practical examples of how to configure them with focus on optimizing
    the configuration. It also goes beyond what is available off the shelf and teaches
    you how to write your own module, in case something is not available from the
    big Nginx open source community.

and:

    This book is intended for advanced users, system administrators, and developers
    of Nginx modules.

Okay, so we actually can expect to dive into something. Maybe module development
within Nginx is much easier than I assumed. That would be a nice surprise.

I do enjoy that the progression of this book is from absolute basics to in depth
and advanced usage.

Chapters 1-4
~~~~~~~~~~~~

The first chapter briefly goes over installing Nginx on every OS I've heard of
it being installed on. Some of this was taken directly from the Nginx wiki which
is an excellent source of information. It's a relatively simple and easy to
follow chapter that gets through the basics.

The second chapter discusses configuring the events and main modules.

Chapter three explains configuration schematics and directives. It gets pretty
thorough without being boring. For a beginner, the information provided here is
very useful.

Chapter four is the logical continuation of third party modules. This chapter
takes a long time to explain the use of a small number of third party modules.
The modules explained are useful and the explanation is thorough, but I would
have preferred seeing an overview of finding modules, documentation, and usage.

In the end, I'm calling these sections the basic intro to Nginx. That would be
great if we weren't over half way through the book already.

Chapters 5
~~~~~~~~~~

This dives into the very basic structure of a module. It also references files
within the Nginx source that provide further information about development.
This chapter takes a pretty quick dive into development of modules and explains
many different points of interaction between Nginx core and the module.

Chapter 6
~~~~~~~~~

Nope, that's it. We're done. After chapter 5, we have the index followed by some
advertising of more Nginx books by this publisher.

After Reading
-------------

I enjoyed the basics of this book. It takes you through compiling and installing
Nginx as well as getting it configured properly. It does a solid job of making
you have a clue what's going on.

Unfortunately, the actual module development, the title of the book, is very
lacking. It's just a pile of details to get you started and then abruptly ends.

If the author added some more chapters to bring the development part together
and expand on initial concepts, this could have been an excellent book. If
you're looking for a basic intro to Nginx book, skip chapter five and get this.
If you want to dive into developing Nginx modules, this isn't the book for you.
