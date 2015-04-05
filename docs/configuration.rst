Configuration
=============

Custom model for tree pages
---------------------------

Create model of tree pages.

.. no-code-block:: python

    from ps_pages.models import BasePages

    ...

    class MPTTPages(BasePages, Base):
        __tablename__ = "mptt_pages"

        id = Column(Integer, primary_key=True)

        @TableProperty
        def sacrud_list_col(cls):
            col = cls.columns
            return [col.name, col.level, col.tree_id,
                    col.parent_id, col.left, col.right]

        @TableProperty
        def sacrud_detail_col(cls):
            col = cls.columns
            return [('', [col.name, col.slug, col.description, col.visible,
                        col.in_menu, col.parent_id]),
                    ('Redirection', [col.redirect_url, col.redirect_page,
                                    col.redirect_type]),
                    ('SEO', [col.seo_title, col.seo_keywords, col.seo_description,
                            col.seo_metatags])
                    ]

Configure `pyramid_sacrud`
--------------------------

First, configure `pyramid_sacrud <https://github.com/ITCase/pyramid_sacrud>`_

.. no-code-block:: python

    from youproject.models import MPTTPages

    ...

    # SACRUD configuration
    config.include('pyramid_sacrud', route_prefix='/admin')
    settings = config.registry.settings
    settings['pyramid_sacrud.models'] = (('Tree pages', [MPTTPages]), )

Configure `ps_pages`
--------------------

Then add settings of `ps_pages`

As string, support ini config

.. code-block:: python

    settings['ps_pages.model_locations'] = 'youproject.models:MPTTPages'
    # ps_pages - put it after all routes
    config.include("ps_pages")

Or just add model

.. no-code-block:: python

    from youproject.models import MPTTPages

    ...

    settings['ps_pages.model_locations'] = MPTTPages
    # ps_pages - put it after all routes
    config.include("ps_pages")
