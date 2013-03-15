.. _tutorial:

Tutorial
========

At the end of this tutorial we're going to have a basic version of the Academic
Earth Plugin. This plugin plays videos from http://www.academicearth.org/.

Since this tutorial is meant to cover the usage of xbmcswift2, we will not be
covering HTML scraping. It makes sense to partition your scraping code into a
separate module from your addon's core functionality. In this example, we're
going to use a scraping library for academic earth that I already have written.


Creating the Plugin Structure
-----------------------------

The first step is to create your working directory for your addon. Since this
can be repetitive, xbmcswift2 provides a script which will create the necessary
files and folders for you. So we'll do just that::

    (xbmcswift2)jon@lenovo tmp  $ xbmcswift2 create

        xbmcswift2 - A micro-framework for creating XBMC plugins.
        xbmc@jonathanbeluch.com
        --

        I'm going to ask you a few questions to get this project started.
        What is your plugin name? : Academic Earth Tutorial
        Enter your plugin id. [plugin.video.academicearthtutorial]: 
        Enter parent folder (where to create project) [/tmp]: 
        Enter provider name : Jonathan Beluch (jbel)
        Projects successfully created in /tmp/plugin.video.academicearthtutorial.
        Done.

If you ``cd`` into the created directory, you should see the familiar addon
structure, including ``addon.py``, ``addon.xml``, ``resourcres`` directory,
etc.

Setup for this Tutorial
-----------------------

To make this tutorial go a bit smoother, we're going to use some existing code
which handles the scraping of the Academic Earth website. Download `this file
<https://github.com/downloads/jbeluch/xbmc-academic-earth/academicearth.tgz>`_
and extract it to ``resources/lib/``. ::

    $ cd resources/lib
    $ wget https://github.com/downloads/jbeluch/xbmc-academic-earth/academicearth.tgz
    $ tar -xvzf academicearth.tgz
    $ rm academicearth.tgz

We should now have an ``academicearth`` directory in our lib directory.

Since our api library requires the use of BeautifulSoup, we'll need to add this
as a depenency to our addon.xml file.

If you open the addon.xml file, you'll notice that xbmcswift2 is already in your dependencies:

.. sourcecode:: xml

    <import addon="xbmc.python" version="2.0" />
    <import addon="script.module.xbmcswift2" version="1.1.1" />

We'll add BeautifulSoup right after those lines:

.. sourcecode:: xml

    <import addon="script.module.beautifulsoup" version="3.0.8" />

The last step is to install BeautifulSoup locally, so we can run our addon on
the command line.::

    $ pip install BeautifulSoup


Creating our Addon's Main Menu
------------------------------

Let's modify the the index function, to look like this:

.. sourcecode:: python

   @plugin.route('/')
   def main_menu():
    items = [
        {'label': 'Show Subjects', 'path': plugin.url_for('show_subjects')}
    ]
    return items

The ``main_menu`` function is going to be our default view. Take note that is
has the route of ``/``. The first time the addon is launched, there will be no
state information, so the requested URL will match '/'.

If you were to run the plugin now, you'd see an exception about a view not
being found. This is because we are specifying a view name of 'show_subjects'
but we don't have a view with that name! So let's create a stub for that view.

.. sourcecode:: python

    @plugin.route('/subjects/')
    def show_subjects():
        pass

So now we have a basic plugin with two views. Keep in mind as we go along, that
we can always run the plugin from the command line.::

    $ xbmcswift2 run 2>/dev/null
    ------------------------------------------------------------
     #  Label    Path
     ------------------------------------------------------------
     [0] Subjects (plugin://plugin.video.academicearth/subjects/)
     ------------------------------------------------------------


Creating the Subjects View
--------------------------

Now let's add some logic to our ``show_subjects`` function.

.. sourcecode:: python

    @plugin.route('/subjects/')
    def show_subjects():
        api = AcademicEarth()
        subjects = api.get_subjects()

        items = [{
            'label': subject.name,
            'path': plugin.url_for('show_subject_info', url=subject.url),
        } for subject in subjects]

        sorted_items = sorted(items, key=lambda item: item['label'])
        return sorted_items

You can see that we are going to be using our Academic Earth api module here.
So we need to import the class before we instantiate it: ``from
resources.lib.academicearth.api import AcademicEarth``.

The call to ``get_subjects`` returns a list of Subject objects with various
attributes that we can access.

So our code simply loops over the subjects and creates a dictionary for each
subject. These simple dictionaries will be converted by xbmcswift2 into proper
list items and then displayed by XBMC. The two mandatory keys are ``label``,
which is the text to display for the item, and ``path``, which is the URL to
follow when the item is selected.

Here, if the user selects a subject list item, we want to send them to the
``show_subject_info`` function. Notice we are also passing a keyword argument
to the ``url_for`` method. This is the main way that we can pass information
between successive invocations of the addon. By default, XBMC addons are
stateless, each time a user clicks on an item the addon is executed, it does
some work and then exits. To keep track of what the user was doing, we need to
encode the information in the url. xbmcswift2 handles the url encoding as long
as you pass the arguments to url_for.

The last lines of code in our view simply sort the list of dictionaries based
on the label and then return the list.

The last step we need to take before running our addon is to stub out the
``show_subject_info`` view.

.. sourcecode:: python

    @plugin.route('/subjects/<url>/')
    def show_subject_info(url):
        pass

Note that since we are passing a url argument to ``url_for``, we need to
ensure our view can handle the argument. This involves creating a placeholder
in the url, ``<url>`` and then ensuring our view takes a single argument,
``url``. xbmcswift2 will attempt to match incoming URLs against the list of
routes. If it finds a match, it will convert any instances of ``<var_name>`` to
variables and then call the view with those variables.  See :ref:`routing` for
more detailed information about routing.

Now let's run our plugin in interactive mode (for the sake of brevity I've replaces a lot of entries in the example output with ``...``)::

    $ xbmcswift2 run interactive 2>/dev/null
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
    [ 5] Applied CompSci          (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Fapplied-computer-science/)
    [ 6] Architecture             (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Farchitecture/)
    ...
    [67] Visualization & Graphics (plugin://plugin.video.academicearth/subjects/http%3A%2F%2Fwww.academicearth.org%2Fsubjects%2Fvisualization-graphics/)
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Choose an item or "q" to quit:

The first output we see is our main menu. Then we are prompted for an item to
select (only 1 available in this case). When we select Subjects, we are then
routed to our show_subjects view.


Adding Code to ``show_subject_info``
------------------------------------

Let's add some logic to our ``show_subject_info`` view:

.. sourcecode:: python

    @plugin.route('/subjects/<url>/')
    def show_subject_info(url):
        subject = Subject.from_url(url)

        courses = [{
            'label': course.name,
            'path': plugin.url_for('show_course_info', url=course.url),
        } for course in subject.courses]

        lectures = [{
            'label': 'Lecture: %s' % lecture.name,
            'path': plugin.url_for('play_lecture', url=lecture.url),
            'is_playable': True,
        } for lecture in subject.lectures]

        by_label = itemgetter('label')
        items = sorted(courses, key=by_label) + sorted(lectures, key=by_label)
        return items


Most of this should look very similar to our code for show subjects. This time
however, we have two different types of Academic Earth content to handle,
courses and lectures. We want courses to route to ``show_course_info``, which
will list all of the lectures for the course. Lectures, however, are simply
videos, so we want these list items to play a video when the user selects one.
We are going to route lectures to ``play_lecture``.

A new concept in this view is the ``is_playable`` item. By default, list items
in xbmcswift2 are not playable. This means that XBMC expects the list item to
point back to an addon and will not attempt to play a video (or audio) for the
given URL. When you are finally ready for XBMC to play a video, a special flag
must be set. xbmcswift2 handles this for you, all you need to do is remember to
set the ``is_playable`` flag to True.

There is another new concept in this view as well. Typically, if you tell XBMC
that a URL is playable, you will pass a direct URL to a resource such as an mp4
file. In this case, we have to do more scraping in order to figure out the URL
for the particular video the user selects. So our playable URL actually calls
back into our addon, which will then make use of plugin.set_resolved_url().

Adding the ``show_course_info`` and ``play_lecture`` views
----------------------------------------------------------

Let's add the following code to complete our addon:

.. sourcecode:: python

    @plugin.route('/courses/<url>/')
    def show_course_info(url):
        course = Course.from_url(url)
        lectures = [{
            'label': 'Lecture: %s' % lecture.name,
            'path': plugin.url_for('play_lecture', url=lecture.url),
            'is_playable': True,
        } for lecture in course.lectures]

        return sorted(lectures, key=itemgetter('label'))


    @plugin.route('/lectures/<url>/')
    def play_lecture(url):
        lecture = Lecture.from_url(url)
        url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % lecture.youtube_id
        plugin.log.info('Playing url: %s' % url)
        plugin.set_resolved_url(url)

The ``show_course_info`` view should look pretty familiar at this point. We are
just listing the lectures for the given course url.

The ``play_lecture`` view introduces some new concepts however. Remember that
we told XBMC that our lecture items were *playable*. Since we gave a URL which
pointed to our addon, we now have to use ``plugin.set_resolved_url(url)``. This
communicates to XBMC, that this is the *real* url that we want to play.

We are introducing one more layer of indirection here however. Since all of the
content on Academic Earth is hosted on youtube, our addon would normally
require lots of extra code just to parse URLs out of youtube. However, the
youtube addon conveniently does all of that! So, we will actually set the
playable URL to point to the youtube plugin, which will then provide XBMC with
the actual playable URL. Sounds a bit complicated, but it makes addons much
simpler in the end. Our addon simply deals with parsing the Academic Earth
website, and leaves anything youtube specific to the youtube addon.

The last step is now to add youtube as a dependency for our addon. Let's edit
the addon.xml again and add youtube:

.. sourcecode:: xml

    <import addon="plugin.video.youtube" version="3.1.0" />

Conclusion
----------

We're finished! You should be able to navigate your addon using the command
line. You should also be able to test your addon directly in XBMC. I personally
like to use symlinks to test my addons. On linux, you could do something like
this::

    $ cd ~/.xbmc/addons
    $ ln -s ~/Code/plugin.video.academicearthtutorial

Note that you'll also have to install the xbmcswift2 XBMC distribution. The
easiest way is to install one of the addons listed on the :ref:`poweredby`
page. Since they all require xbmcswift2 as a dependency, it will automatically
be installed. The other option is to download the newest released version from
`this page <https://github.com/jbeluch/xbmcswift2-xbmc-dist/tags>`_ and unzip
it in your addons directory.
