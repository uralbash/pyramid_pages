#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Routes for pyramid_pages
"""
from sqlalchemy import or_
from pyramid.events import BeforeRender
from pyramid.location import lineage
from pyramid.httpexceptions import HTTPNotFound

from . import CONFIG_MODELS, CONFIG_DBSESSION
from .security import HOME_PAGE, PREFIX_PAGE
from .resources import (
    BasePageResource,
    models_of_config,
    resource_of_node,
    resources_of_config
)


def add_globals(event):
    event['lineage'] = lineage


def page_factory(request):
    """ Page factory.

    Config models example:

    .. code-block:: python

        models = {
            '': [WebPage, CatalogResource],
            'catalogue': CatalogResource,
            'news': NewsResource,
        }
    """
    prefix = request.matchdict['prefix']  # /{prefix}/page1/page2/page3...
    settings = request.registry.settings
    dbsession = settings[CONFIG_DBSESSION]
    config = settings[CONFIG_MODELS]

    if prefix not in config:
        # prepend {prefix} to *traverse
        request.matchdict['traverse'] =\
            tuple([prefix] + list(request.matchdict['traverse']))
        prefix = None

    # Get all resources and models from config with the same prefix.
    resources = config.get(
        prefix, config.get(   # 1. get resources with prefix same as URL prefix
            '', config.get(   # 2. if not, then try to get empty prefix
                '/', None)))  # 3. else try to get prefix '/' otherwise None

    if not hasattr(resources, '__iter__'):
        resources = (resources, )

    tree = {}

    if not resources:
        return tree

    # Add top level nodes of resources in the tree
    for resource in resources:
        table = None
        if not hasattr(resource, '__table__')\
                and hasattr(resource, 'model'):
            table = resource.model
        else:
            table = resource

        if not hasattr(table, 'slug'):
            continue

        nodes = dbsession.query(table)
        if hasattr(table, 'parent_id'):
            nodes = nodes.filter(or_(
                table.parent_id == None,  # noqa
                table.parent.has(table.slug == '/')
            ))
        for node in nodes:
            if not node.slug:
                continue
            resource = resource_of_node(resources, node)
            tree[node.slug] = resource(node, prefix=prefix)
    return tree


def home_page_factory(request):
    settings = request.registry.settings
    dbsession = settings[CONFIG_DBSESSION]
    config = settings[CONFIG_MODELS]
    models = models_of_config(config)
    resources = resources_of_config(config)
    for table in models:
        if not hasattr(table, 'slug'):
            continue
        node = dbsession.query(table).filter(table.slug == '/').first()
        if node:
            return resource_of_node(resources, node)(node)
    raise HTTPNotFound


def register_views(*args):
    """ Registration view for each resource from config.
    """
    config = args[0]
    settings = config.get_settings()
    pages_config = settings[CONFIG_MODELS]
    resources = resources_of_config(pages_config)
    for resource in resources:
        if hasattr(resource, '__table__')\
                and not hasattr(resource, 'model'):
            continue
        resource.model.pyramid_pages_template = resource.template
        config.add_view(resource.view,
                        attr=resource.attr,
                        route_name=PREFIX_PAGE,
                        renderer=resource.template,
                        context=resource,
                        permission=PREFIX_PAGE)


def includeme(config):
    config.add_subscriber(add_globals, BeforeRender)

    # Home page factory
    config.add_route(HOME_PAGE, '/', factory=home_page_factory)
    config.add_view(BasePageResource.view,
                    attr=BasePageResource.attr,
                    route_name=HOME_PAGE,
                    renderer=BasePageResource.template,
                    context=BasePageResource,
                    permission=HOME_PAGE)

    # Default page factory
    config.add_route(PREFIX_PAGE, '/{prefix}*traverse', factory=page_factory)
    config.add_view(BasePageResource.view,
                    attr=BasePageResource.attr,
                    route_name=PREFIX_PAGE,
                    renderer=BasePageResource.template,
                    context=BasePageResource,
                    permission=PREFIX_PAGE)

    import pkg_resources
    pyramid_version = pkg_resources.get_distribution("pyramid").parsed_version
    if pyramid_version >= pkg_resources.SetuptoolsVersion('1.6a1'):
        # Allow you to change settings after including this function. This
        # fuature works only in version 1.6 or above.
        config.action('pyramid_pages_routes', register_views, args=(config, ))
    else:
        config.include(register_views)
