Configuration
=============

Custom model for tree pages
---------------------------

To build a tree, using the model from `sqlalchemy_mptt
<https://github.com/uralbash/sqlalchemy_mptt>`_.

.. note::

  | Otherwise, it will look like flat pages.
  | Plans to add a recursive model with only `parent_id` field.

Create model of tree pages. For more detail see example `pyramid_pages_example
<https://github.com/uralbash/pyramid_pages/blob/master/example/pyramid_pages_example.py>`_.

.. no-code-block:: python

   from pyramid_pages.models import FlatPageMixin, MpttPageMixin, RedirectMixin

   ...

   class WebPage(Base, MpttPageMixin, RedirectMixin):
       __tablename__ = 'mptt_pages'

       id = Column('id', Integer, primary_key=True)


   class NewsPage(Base, FlatPageMixin):
       __tablename__ = 'flat_news'

       id = Column('id', Integer, primary_key=True)
       date = Column(Date, default=func.now())

If you use `pyramid_sacrud <https://github.com/uralbash/pyramid_sacrud>`_, you
can inherited from :class:`~pyramid_pages.models.BaseSacrudMpttPage` or
:class:`~pyramid_pages.models.BaseSacrudFlatPage` or just use
:class:`~pyramid_pages.models.SacrudOptions`. 

It's look likes this:

.. image:: _static/img/sacrud_pyramid_pages.png 
    :alt: Integration pyramid_pages with pyramid_sacrud
    :align: center

Configure `pyramid_pages`
-------------------------

Then add settings of :mod:`pyramid_pages`.

.. no-code-block:: python

    from youproject.models import WebPage, NewsPage

    ...

    settings['pyramid_pages.models'] = {
       '': WebPage,
       'pages': WebPage,  # available with prefix '/pages/'
       'news': NewsPage
    }

    # pyramid_pages - put it after all routes
    # and after pyramid_pages configuration.
    config.include("pyramid_pages")

If you use version of pyramid >= 1.6a1, there is a possibility put
``config.include("pyramid_pages")`` before pyramid_pages Configuration.

.. no-code-block:: python

    from youproject.models import WebPage, NewsPage

    ...

    config.include("pyramid_pages")
    settings['pyramid_pages.models'] = {
       '': WebPage,
       'pages': WebPage,  # available with prefix '/pages/'
       'news': NewsPage
    }

Custom resource
---------------

Base resource for pages can be found in the module :mod:`pyramid_pages.routes`.

.. literalinclude:: /../pyramid_pages/routes.py
   :language: python
   :linenos:
   :caption: Base resource for pages.
   :pyobject: PageResource

Just inherit your resource from :class:`~pyramid_pages.routes.PageResource`.

.. literalinclude:: /../example/pyramid_pages_example.py
   :language: python
   :linenos:
   :caption: Custom resource for gallery.
   :pyobject: GalleryResource

.. literalinclude:: /../example/pyramid_pages_example.py
   :language: python
   :linenos:
   :caption: Model for GalleryResource.
   :pyobject: Gallery

.. literalinclude:: /../example/pyramid_pages_example.py
   :language: python
   :linenos:
   :caption: Model photo for Gallery.
   :pyobject: Photo

And add it to config.

.. code-block:: python
    :emphasize-lines: 5

    settings['pyramid_pages.models'] = {
       '': WebPage,
       'pages': WebPage,  # available with prefix '/pages/'
       'news': NewsPage,
       'gallery': GalleryResource
    }

Generate menu
-------------

Make menu object and pass it in template context.

.. code-block:: python

    from pyramid_pages.common import Menu


    class Gallery(Base, MpttPageMixin):
        __tablename__ = 'mptt_gallery'

        menu_template = 'myproject/templates/my_custom_menu.mako'

        id = Column('id', Integer, primary_key=True)

    page_menu = Menu(DBSession, WebPage).mptt
    news_menu = Menu(DBSession, NewsPage).flat
    gallery_menu = Menu(DBSession, Gallery).mptt

Just include menu template.

.. code-block:: jinja

    {% with menu=news_menu() %}
      {% include menu.template with context %}
    {% endwith %}

    {% with menu=page_menu(from_lvl=1, to_lvl=6, trees=(1, 2, 3)) %}
      {% include menu.template with context %}
    {% endwith %}

Or write your own.

.. literalinclude:: /../pyramid_pages/templates/pyramid_pages/menu/flat.jinja2
   :language: html+jinja
   :linenos:
   :caption: Flat menu template.

.. literalinclude:: /../pyramid_pages/templates/pyramid_pages/menu/mptt.jinja2
   :language: html+jinja
   :linenos:
   :caption: MPTT menu template.

If you want show mptt menu with ``to_lvl==max-2`` or similar, just use ``to_lvl=-2``.

.. code-block:: jinja

    {% with menu=page_menu(from_lvl=1, to_lvl=-2, trees=(1, 2, 3)) %}
      {% include menu.template with context %}
    {% endwith %}
