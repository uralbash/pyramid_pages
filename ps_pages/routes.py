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
    def __init__(self, node):
        self.node = node

    def __getitem__(self, name):
        children = {str(c.slug or ''): Resource(c) for c in self.node.children}
        return children[name]

    def __repr__(self):
        return "<%s>" % self.node.name.encode('utf-8')


def get_root_factory(dbsession, table):
    query = dbsession.query(table)
    nodes = query.filter(or_(table.parent_id == None,
                             table.parent.has(table.slug == '/'))).all()
    tree = {}
    for node in nodes:
        if node.slug:
            tree[node.slug] = Resource(node)

    return tree


def root_factory(request):
    table = get_pages_model(request.registry.settings)
    dbsession = request.dbsession
    return get_root_factory(dbsession, table)


def includeme(config):
    config.add_route('sacrud_pages_move',
                     '/sacrud_pages/move/{node}/{method}/{leftsibling}/')
    config.add_route('sacrud_pages_get_tree',
                     '/sacrud_pages/get_tree/')
    config.add_route('sacrud_pages_visible',
                     '/sacrud_pages/visible/{node}/')
    config.add_route('sacrud_pages_view', '/*traverse', factory=root_factory)
