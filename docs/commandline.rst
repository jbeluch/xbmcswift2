.. _commandline:


Running xbmcswift2 on the Command Line
======================================


Commands
--------

When running xbmcswift2 from the command line, there are two commands
available, *create* and *run*. *create* is a script that will create the basic
scaffolding and necessary files for an XBMC addon and personalize it by asking
a few questions. *run* enables you to debug your addon on the command line.

To see the command line help, simply execute ``xbmcswift2 -h``. Both of the
commands are explained further below.


create
~~~~~~

To create a new addon, change your current working directory to a location
where you want your addon folder to be created. Then execute ``xbmcswift2
create``. After answering a few questions, you should have the basic addon
structure in place.

run
~~~

When running an addon on the command line, there are three different run modes
available, once_, interactive_, and crawl_. 

There is also a second positional argument, ``url``, which is optional. By
default, xbmcswift2 will run the root URL of your addon (a path of '/'), e.g.
``plugin://plugin.video.academicearth/``. This is the same default URL that
XBMC uses when you first enter an addon. You can gather URLs from the output of
xbmcswift2.

The options ``-q`` and ``-v`` decrease and increase the logging level.

.. note::

    To enable running on the command line, xbmcswift2 attempts to mock a
    portion of the XBMC python bindings. Certain functions behave properly like
    looking up strings. However, if a function has not been implemented,
    xbmcswift2 lets the function call pass silently to avoid exceptions and
    allow the plugin to run in a limited fashion. This is why you'll often see
    WARNING log messages when running on the command line.

    If you plan on using the command line to develop your addons, you should
    always import the xbmc modules from xbmcswift2::

        from xbcmswift2 import xbmcgui

    xbmcswift2 will correctly import the proper module based on the
    environment. When running in XBMC, it will import the actual modules, and
    when running on the command line it will import mocked modules without
    error.


once
____

Executes the addon once then quits. Useful for testing when used
with the optional ``url`` argument.::

    $ xbmcswift2 run once # you can omit the once argument as it is the default

    ------------------------------------------------------------
     #  Label    Path
    ------------------------------------------------------------
    [0] Subjects (plugin://plugin.video.academicearth/subjects/)
    ------------------------------------------------------------


    $ xbmcswift2 run once plugin://plugin.video.academicearth/subjects/
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
     #   Label                    Path
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
     [ 0] ACT                      (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Fact/)
     [ 1] Accounting               (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Faccounting/)
     [ 2] Algebra                  (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Falgebra/)
     [ 3] Anthropology             (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Fanthropology/)
     [ 4] Applied CompSci          (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Fapplied-computer-science/)
     ...


interactive
___________

Allows the user to step through their addon using an interactive session. This
is meant to mimic the basic XBMC interface of clicking on a listitem, which
then brings up a new directory listing. After each listing is displayed the
user will be prompted for a listitem to select.  There will always be a ``..``
option to return to the previous directory (except for the initial URL).::

    $ xbmcswift2 run interactive
    ------------------------------------------------------------
     #  Label    Path
    ------------------------------------------------------------
    [0] Subjects (plugin://plugin.video.academicearth/subjects/)
    ------------------------------------------------------------
    Choose an item or "q" to quit: 0

    ----------------------------------------------------------------------------------------------------------------------------------------------------------
     #   Label                    Path
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    [ 0] ..                       (plugin://plugin.video.academicearth/)
    [ 1] ACT                      (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Fact/)
    [ 2] Accounting               (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Faccounting/)
    [ 3] Algebra                  (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Falgebra/)
    [ 4] Anthropology             (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Fanthropology/)
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Choose an item or "q" to quit: 1

    -----------------------------------------------------------------------------------------------------------------------------------------------
     #  Label                   Path
    -----------------------------------------------------------------------------------------------------------------------------------------------
    [0] ..                      (plugin://plugin.video.academicearth/subjects/)
    [1] ACT - Science Test Prep (plugin://plugin.video.academicearth/courses/http%3A%2F%2Fwww.academicearth.org%2Fcourses%2Fact-science-test-prep/)
    -----------------------------------------------------------------------------------------------------------------------------------------------


crawl
_____

Used to crawl every available path in your addon. In between each request the
user will be prompted to hit Enter to continue.::

    $ xbmcswift2 run crawl 2>/dev/null
    ------------------------------------------------------------
     #  Label    Path
    ------------------------------------------------------------
    [0] Subjects (plugin://plugin.video.academicearth/subjects/)
    ------------------------------------------------------------
    Enter to continue or "q" to quit
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
     #   Label                    Path
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    [ 0] ACT                      (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Fact/)
    [ 1] Accounting               (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Faccounting/)
    [ 2] Algebra                  (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Falgebra/)
    [ 3] Anthropology             (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Fanthropology/)
    [ 4] Applied CompSci          (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Fapplied-computer-science/)
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Enter to continue or "q" to quit
    -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     #   Label                                                                                                  Path
    -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    [ 0] A Cultural and Scientific Survey of the Eye and Vision                                                 (plugin://plugin.video.academicearth/courses/http%3A%2F%2Fwww.academicearth.org%2Fcourses%2Fa-cultural-and-scientific-survey-of-the-eye-and-vision/)
    [ 1] Autism and Related Disorders                                                                           (plugin://plugin.video.academicearth/courses/http%3A%2F%2Fwww.academicearth.org%2Fcourses%2Fautism-and-related-disorders/)
    [ 2] Biology                                                                                                (plugin://plugin.video.academicearth/courses/http%3A%2F%2Fwww.academicearth.org%2Fcourses%2Fbiology/)
    [ 3] Core Science - Biochemistry I                                                                          (plugin://plugin.video.academicearth/courses/http%3A%2F%2Fwww.academicearth.org%2Fcourses%2Fcore-science---biochemistry-i/)
    [ 4] Darwin's Legacy                                                                                        (plugin://plugin.video.academicearth/courses/http%3A%2F%2Fwww.academicearth.org%2Fcourses%2Fdarwins-legacy/)
    -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Enter to continue or "q" to quit

