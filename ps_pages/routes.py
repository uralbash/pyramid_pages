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

from sqlalchemy import or_

from .views import page_view


class PageResource(object):

    def __init__(self, node, prefix=None):
        self.node = node
        self.prefix = prefix

    @property
    def __name__(self):
        if self.node and not self.node.slug == '/':
            return self.node.slug
        elif self.prefix:
            return self.prefix
        return None

    @property
    def __parent__(self):
        return PageResource(self.node.parent, self.prefix)

    def __getitem__(self, name):
        children = {str(child.slug or ''): PageResource(child, self.prefix)
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


def page_factory(request):
    settings = request.registry.settings
    models = settings['ps_pages.models']
    prefix = request.matchdict['prefix']
    if prefix not in models:
        # prepend {prefix} to *traverse
        request.matchdict['traverse'] =\
            tuple([prefix] + list(request.matchdict['traverse']))
        prefix = None
        table = models['']
    else:
        table = models[prefix]
    dbsession = settings['ps_pages.dbsession']
    nodes = dbsession.query(table)\
        .filter(or_(table.parent_id.is_(''),
                    table.parent_id.is_(None),
                    table.parent.has(table.slug == '/'))).all()
    return {node.slug: PageResource(node, prefix)
            for node in nodes if node.slug}


def home_page_factory(request):
    settings = request.registry.settings
    models = settings['ps_pages.models']
    table = models[''] or models['/']
    dbsession = settings['ps_pages.dbsession']
    node = dbsession.query(table).filter(table.slug.is_('/')).one()
    return PageResource(node)


def includeme(config):
    name = 'pyramid_pages_prefix_page_view'
    config.add_route(name, '/{prefix}*traverse', factory=page_factory)
    config.add_view(page_view,
                    route_name=name,
                    renderer='ps_pages/index.jinja2',
                    context=PageResource,
                    permission=name)

    name = 'pyramid_pages_home_page_view'
    config.add_route(name, '/', factory=home_page_factory)
    config.add_view(page_view,
                    route_name=name,
                    renderer='ps_pages/index.jinja2',
                    context=PageResource,
                    permission=name)
