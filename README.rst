===========
Discharge
===========

.. image:: https://secure.travis-ci.org/RichardOfWard/discharge.png
    :alt: Build Status
    :target: http://travis-ci.org/RichardOfWard/discharge


Discharge is a static site builder implemented in python. It builds
static sites from a folder full of Jinja2 templates, Markdown files,
and other assets (js, css, images etc.). It uses pygments for syntax
highlighting of <code> blocks

It is heavily plugin based - most of the functionality comes from plugins
shipped with discharge.

It is currently alpha software and subject to backwards-incompatible
changes.


Installation
============

Use your favorite install method, for example:

    $ pip install discharge


Usage
=====

Create a file in your source directory called `_discharge.py` (files
starting with a `_` or a `.` are ignored by discharge):

    import os
    
    from discharge.site import Site
    
    site = Site(
        os.path.join(os.path.dirname(__file__), './'),
        os.path.join(os.path.dirname(__file__), '_build'),
    )
    
    from discharge.plugins.robots import RobotsPlugin
    robots_plugin = RobotsPlugin()
    site.add_plugin(robots_plugin)
    
    from discharge.plugins.jinja2_templates import Jinja2TemplatesPlugin
    jinja2_templates_plugin = Jinja2TemplatesPlugin()
    site.add_plugin(jinja2_templates_plugin)
    
    from discharge.plugins.markdown import MarkdownPlugin
    markdown_plugin = MarkdownPlugin()
    site.add_plugin(markdown_plugin)

Create `.html`, `.markdown` and `.mdown` files in the same folder
and they will be processed by Jinja2 or Markdown.

Markdown files will be rendered using a template `_page.html`
which you must provide yourself. You can use `{{content}}` in `_page.html`
to get the content produced by Markdown.

You can then run `discharge build` to build the site or
`dscharge serve` to run the development server.
