Configuration
=============

Custom model for tree pages
---------------------------

To build a tree, using the model from `sqlalchemy_mptt <https://github.com/ITCase/sqlalchemy_mptt>`_.

.. note::

   The plans make it more versatile

Create model of tree pages. For more detail see example `pyramid_pages_example
<https://github.com/ITCase/pyramid_pages/blob/master/example/pyramid_pages_example.py>`_.

.. no-code-block:: python

    from pyramid_pages.models import BasePages, PageMixin
    from sqlalchemy_mptt import BaseNestedSets

    ...

    class MPTTPages(BasePages, Base):
        __tablename__ = "mptt_pages"

        id = Column('id', Integer, primary_key=True)


    class MPTTNews(BaseNestedSets, PageMixin, Base):
        __tablename__ = "mptt_news"

        id = Column('id', Integer, primary_key=True)

Configure `pyramid_pages`
-------------------------

Then add settings of `pyramid_pages`.

.. no-code-block:: python

    from youproject.models import MPTTPages, MPTTNews

    ...

    settings['pyramid_pages.models'] = {
       '': MPTTPages,
       'pages': MPTTPages,  # available with prefix '/pages/'
       'news': MPTTNews
    }

    # pyramid_pages - put it after all routes
    config.include("pyramid_pages")
