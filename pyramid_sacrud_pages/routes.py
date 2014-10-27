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
from sqlalchemy import or_
from .common import get_pages_model


class Resource(object):
    def __init__(self, subobjects, node):
        self.subobjects = subobjects
        self.node = node

    def __getitem__(self, name):
        return self.subobjects[name]

    def __repr__(self):
        return "<%s>" % self.node.name.encode('utf-8')


def recursive_node_to_dict(node):
    children = {str(c.slug or ''): recursive_node_to_dict(c) for c in node.children}
    return Resource(children, node)


def get_root_factory(dbsession, table):
    query = dbsession.query(table)
    nodes = query.filter(or_(table.parent_id == None,
                             table.parent.has(table.slug == '/'))).all()
    tree = {}
    for node in nodes:
        if node.slug:
            tree[node.slug] = Resource(recursive_node_to_dict(node), node)

    return tree


def root_factory(request):
    table = get_pages_model(request.registry.settings)
    dbsession = request.dbsession
    return get_root_factory(dbsession, table)


def includeme(config):
    config.add_route('sacrud_pages_move',       '/sacrud_pages/move/{node}/{method}/{leftsibling}/')
    config.add_route('sacrud_pages_get_tree',   '/sacrud_pages/get_tree/')
    config.add_route('sacrud_pages_visible',    '/sacrud_pages/visible/{node}/')
    config.add_route('sacrud_pages_view',       '/*traverse',
                     factory='pyramid_sacrud_pages.routes.root_factory')
