.. _commandline:


Running Addons on the Command Line
==================================


Options
-------

To see the command line help, simply execute ``xbmcswift2 run -h``.::

    $ xbmcswift2 run -h
    Usage: xbmcswift2 run [once|interactive|crawl] [url]

    Options:
      -h, --help     show this help message and exit
      -q, --quiet    set logging level to quiet
      -v, --verbose  set logging level to verbose


There are three different run modes available, once_ (default),
interactive_, and crawl_.

There is also a second positional argument which is optional, ``url``. By
default, xbmcswift2 will run the root URL,
``plugin://plugin.video.academicearth/``. This is the same default URL that
XBMC uses when you first enter an addon. You can gather runnable URLs from the
output of xbmcswift2.

The options ``-q`` and ``-v`` decrease and increase the logging level.

.. note::

    To enable running on the command line, xbmcswift2 attempts to mock a
    portion of the XBMC python bindings. Certain functions behave properly like
    looking up strings. However, if a function has not been implemented,
    xbmcswift2 lets the function call pass silently to avoid Exceptions and
    allow the plugin to run in a limited fashion. This is why you'll very often
    see WARNING log messages when running on the command line.

    This is also why you should import the xbmc python modules from xbmcswift2::

        from xbcmswift2 import xbmcgui

    xbmcswift2 will correctly import the proper XBMC modules in the correct
    environments so you don't have to worry about it.




once
~~~~

Executes the addon once then quits. Useful for testing when used
with the optional ``url`` argument.::

    $ xbmcswift2 run once 2>/dev/null
    ------------------------------------------------------------
     #  Label    Path
    ------------------------------------------------------------
    [0] Subjects (plugin://plugin.video.academicearth/subjects/)
    ------------------------------------------------------------


interactive
~~~~~~~~~~~

Allows the user to step through their addon using an interactive session. This
is meant to mimic the basic XBMC interface of clicking on a listitem, which
then brings up a new directory listing. After each listing is displayed the
user will be prompted for a listitem to select.  There will always be a ``..``
option to return to the previous directory (except for the initial URL).::

    (xbmc-academic-earth)jon@lenovo ~/Code/xbmc-academic-earth (master) $ xbmcswift2 run interactive 2>/dev/null
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
~~~~~

Used to crawl every available path in your addon. In between each request the
user will be prompted to hit Enter to continue.::

    Choose an item or "q" to quit: (xbmc-academic-earth)jon@lenovo ~/Code/xbmc-academic-earth (master) $ xbmcswift2 run crawl 2>/dev/null
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

