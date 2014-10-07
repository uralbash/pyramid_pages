Application configuration
=========================

Create model of tree pages.

.. code-block:: python

    from pyramid_sacrud_pages.models import BasePages

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

First, configure `pyramid_sacrud <https://github.com/ITCase/pyramid_sacrud>`_

.. code-block:: python

    from youproject.models import MPTTPages

    ...

    # SACRUD configuration
    config.include('pyramid_sacrud', route_prefix='/admin')
    settings = config.registry.settings
    settings['pyramid_sacrud.models'] = {'Tree pages': {'tables': [MPTTPages],
                                                        'position': 1,},
                                        }

Then add settings of `pyramid_sacrud_pages`

.. code-block:: python

    # pyramid_sacrud_pages - put it after all routes
    config.set_request_property(lambda x: MPTTPages,
                                'sacrud_pages_model', reify=True)
    config.include("pyramid_sacrud_pages")
