#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Routes for sacrud_pages
"""
import re

from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy import or_

from .views import PageView
from .security import PREFIX_PAGE, HOME_PAGE

CONFIG_MODELS = 'pyramid_pages.models'
CONFIG_DBSESSION = 'pyramid_pages.dbsession'


class PageResource(object):

    template = 'pyramid_pages/index.jinja2'
    view = PageView
    attr = 'page_with_redirect'

    def __init__(self, node, prefix=None):
        self.node = node
        self.prefix = prefix

    @property
    def __name__(self):
        if self.node and not self.node.slug == '/':
            return self.node.slug
        elif self.node and self.node.slug == '/':
            return ''
        elif self.prefix:
            return self.prefix
        return None

    @property
    def __parent__(self):
        if hasattr(self.node, 'parent'):
            return self.__class__(self.node.parent, self.prefix)
        elif self.node:
            return self.__class__(None, self.prefix)
        return None

    def __getitem__(self, name):
        children = {str(child.slug or ''): self.__class__(child, self.prefix)
                    for child in self.node.children}
        return children[name]

    def __resource_url__(self, request, info):
        separator = '/' if self.prefix else ''
        # XXX: I feel a dissonance here
        info['virtual_path'] = re.sub('/+', '/', info['virtual_path'])
        url = info['app_url'] + separator + info['virtual_path']
        return url

    def __repr__(self):
        return "<{}>".format(self.node.name.encode('utf-8'))

    def get_prefix(self, request, node=None):
        if not node:
            node = self.node
        node = node.__class__
        settings = request.registry.settings
        models = settings[CONFIG_MODELS]
        reversed_models = dict(zip(models.values(), models.keys()))
        prefix = reversed_models.get(node, None)
        if prefix:
            return prefix

        # search prefix for resource
        for model in models.values():
            if not hasattr(model, '__table__') and hasattr(model, 'model')\
                    and model.model == node:
                return reversed_models.get(model, None)
        return None


def page_factory(request):
    settings = request.registry.settings
    models = settings[CONFIG_MODELS]
    prefix = request.matchdict['prefix']
    dbsession = settings[CONFIG_DBSESSION]

    if prefix not in models:
        # prepend {prefix} to *traverse
        request.matchdict['traverse'] =\
            tuple([prefix] + list(request.matchdict['traverse']))
        prefix = None
        table = models['']
    else:
        table = models[prefix]

    if not hasattr(table, '__table__') and hasattr(table, 'model'):
        resource = table
        table = table.model
    else:
        resource = PageResource

    nodes = dbsession.query(table)
    if hasattr(table, 'parent_id'):
        nodes = nodes.filter(or_(table.parent_id.is_(''),
                                 table.parent_id.is_(None),
                                 table.parent.has(table.slug == '/')))
    return {node.slug: resource(node, prefix)
            for node in nodes if node.slug}


def home_page_factory(request):
    settings = request.registry.settings
    models = settings[CONFIG_MODELS]
    table = models[''] or models['/']
    dbsession = settings[CONFIG_DBSESSION]
    node = dbsession.query(table).filter(table.slug.is_('/')).first()
    if not node:
        raise HTTPNotFound
    return PageResource(node)


def register(*args):
    config = args[0]
    settings = config.get_settings()
    models = settings[CONFIG_MODELS]
    for resource in models.values():
        if hasattr(resource, '__table__')\
                and not hasattr(resource, 'model'):
            continue

        config.add_view(resource.view,
                        attr=resource.attr,
                        route_name=PREFIX_PAGE,
                        renderer=resource.template,
                        context=resource,
                        permission=PREFIX_PAGE)


def includeme(config):
    # Home page factory
    config.add_route(HOME_PAGE, '/', factory=home_page_factory)
    config.add_view(PageResource.view,
                    attr=PageResource.attr,
                    route_name=HOME_PAGE,
                    renderer=PageResource.template,
                    context=PageResource,
                    permission=HOME_PAGE)

    # Default page factory
    config.add_route(PREFIX_PAGE, '/{prefix}*traverse', factory=page_factory)
    config.add_view(PageResource.view,
                    attr=PageResource.attr,
                    route_name=PREFIX_PAGE,
                    renderer=PageResource.template,
                    context=PageResource,
                    permission=PREFIX_PAGE)

    import pkg_resources
    pyramid_version = pkg_resources.get_distribution("pyramid").parsed_version
    if pyramid_version >= pkg_resources.SetuptoolsVersion('1.6a1'):
        # Allow you to change settings after including the addon
        config.action('pyramid_pages_routes', register, args=(config, ))
    else:
        config.include(register)
