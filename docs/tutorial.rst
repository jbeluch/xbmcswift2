.. _tutorial:

Tutorial
========

At the end of this tutorial we're going to have a basic version of the Academic
Earth Plugin. The web page we're going to be parsing is
http://www.academicearth.org/.


Creating the Plugin Structure
-----------------------------

You can either do this part manually, or use the ``xbmcswift2 create`` script.
We'll do the latter.::

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

If we were to run the plugin from the CLI now, we'd see a single list item.


Main Menu
---------

Let's modify the the index function, to look like below.

.. sourcecode:: python

   @plugin.route('/')
   def main_menu():
    items = [
        {'label': 'Show Subjects', 'path': plugin.url_for('show_subjects')}
    ]
    return items

The ``main_menu`` function is going to be our default view. To keep the
tutorial simple, we are only going to take one path through the website. 

If you were to run the plugin now, you'd see an exception about a view not
being found. This is because we are specifying a view name of 'show_subjects'
but we don't have a view with that name! So let's create a stub for that view.

.. sourcecode:: python

    @plugin.route('/subjects/')
    def show_subjects():
        pass

So now we have a basic plugin with two views. Keep in mind as we go along, that
we can always run the plugin from the command line. If we pass the interactive
argument (``python addon.py interactive``) we can explore the view hierarchies.


HTML Parsing
------------

So now we're ready for some HTML parsing. Specifically, we want to parse the
available subject names and urls from http://www.academicearth.org/subjects/.

When parsing HTML, you can use any library you like. My personal preference is
to use `Beautiful Soup`_ so we'll be using that for this tutorial.

.. _Beautiful Soup: http://www.crummy.com/software/BeautifulSoup/

We're first going to create a function that will take a URL and return a
BeautifulSoup object. This will save us some code later as we'll reuse it a
lot. Don't forget to add the imports to the top of your addon.py file.

.. sourcecode:: python

    from xbmcswift2 import download_page
    from BeautifulSoup import BeautifulSoup as BS

    def hmtlify(url): 
        return BS(download_page(url))

We're also going to create another helper function to return a full URL for the
academic earth website.

.. sourcecode:: python
    from urlparse import urljoin

    BASE_URL = 'http://academicearth.org'
    def full_url(path):
        '''Creates a full academicearth.org url from a relative path'''
        return urljoin(BASE_URL, path)

Now we can finally parse some HTML. In our ``show_subjects`` view, we're going
to add some code.

.. sourcecode:: python

    @plugin.route('/subjects/')
    def show_subjects():
        html = htmlify(full_url('subjects'))
        subjects = html.findAll('a', {'class': 'subj-links'})

        items = [{
            'label': subject.div.string.strip(),
            'path': plugin.url_for('show_topics', url=full_url(subject['href'])),
        } for subject in subjects]

        return items

Now just one more step before we attempt to view our work so far. We are now
referencing a new view, ``show_topics``. Let's create it since it doesn't
already exist.

.. sourcecode:: python

    @plugin.route('/topics/<url>/')
    def show_topics(url):
        pass

You can see that we're now passing arguments between view functions. If you
follow a link for a subject, you will be presented with a page that contains
topics. Since XBMC plugins are stateless, we need to pass some argument that
allows the plugin to identify which subject the user chose. In this case, we'll
simply pass the URL for the selected subject page.

Viewing Our Progress
--------------------

Let's take for granted that our code works and attempt to view the plugin
interactively. Run ``python addon.py interactive`` and explore the plugin. You
should see the available subjects listed. Notice that the path for each list
item is slightly different as it contains the URL for that specific subject.

Sometimes when testing from the CLI, it can be tedious to step all the way
through the menus. If you'd like to start from a particular menu, simply pass
in the plugin url as an argument.::

    # Display the subjects page
    $ python addon.py plugin://plugin.video.academicearthtutorial/subjects/

    # Start from the subjects page in interactive mode
    $ python addon.py interactive plugin://plugin.video.academicearthtutorial/subjects/


Parsing Topics From a Subject Page
----------------------------------

Now let's update the show_topics function with some parsing code.

.. sourcecode:: python

    @plugin.route('/topics/<url>/')
    def show_topics(url):
        '''Displays topics available for a given subject. If there is only
        one topic available, the user will be redirected to the topics view
        instead.
        '''
        html = htmlify(url)
        topics = html.findAll('a', {'class': 'tab-details-link '})

        items = [{
            'label': topic.string,
            'path': plugin.url_for('show_courses', url=full_url(topic['href'])),
        } for topic in topics]

        # If we only have one item, just redirect to the show_topics page,
        # there's no need to display a single item in the list
        if len(items) == 1:
            return plugin.redirect(items[0]['path'])
        return items

This function should look very similar to the show_subjects function we wrote
above. The main difference is that we are using a dynamic url being passed in
as an argument to our function.

We're also being exposed to some new functionality
:meth:`~xbmcswift2.Plugin.redirect`. This function allows us to redirect the
user to another view. In this case, if we have only one topic to display, we
might as well just redirect to `show_courses` for that particular topic.

Like above, we'll need to stub out ``show_courses`` before we can run our
plugin.

.. sourcecode:: python

    @plugin.route('/courses/<url>/')
    def show_courses(url):
        pass

As always, we should test our plugin iteractively to make sure things seem to
be working.

To be continued...

