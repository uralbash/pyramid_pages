#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

from models import MPTTPages

__version__ = "0.0.1a"


@view_config(route_name='sacrud_pages_move', renderer='json',
             permission=NO_PERMISSION_REQUIRED)
def page_move(request):
    node = request.matchdict['node']
    method = request.matchdict['method']
    left_sibling = request.matchdict['leftsibling']
    page = request.dbsession.query(MPTTPages).filter_by(id=node).one()

    if method == 'inside':
        page.move_inside(left_sibling)
    if method == 'after':
        page.move_after(left_sibling)
    return ''


@view_config(route_name='sacrud_pages_insert', renderer='json',
             permission=NO_PERMISSION_REQUIRED)
def page_insert(request):
    parent_id = request.matchdict['parent_id']
    node = MPTTPages(parent_id=parent_id)
    request.dbsession.add(node)
    request.dbsession.flush()

    return {'label': str(node), 'id': node.id}


@view_config(route_name='sacrud_pages_get_tree', renderer='json',
             permission=NO_PERMISSION_REQUIRED)
def get_tree(request):
    def fields(node):
        return {'visible': node.visible}
    return MPTTPages.get_tree(request.dbsession, json=True, json_fields=fields)


@view_config(route_name='sacrud_pages_visible', renderer='json',
             permission=NO_PERMISSION_REQUIRED)
def page_visible(request):
    node = request.matchdict['node']
    node = request.dbsession.query(MPTTPages).filter_by(id=node).one()
    node.visible = not node.visible
    request.dbsession.add(node)
    request.dbsession.flush()

    return {"visible": node.visible}


@view_config(route_name='sacrud_pages_view', renderer='/sacrud_pages/index.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def page_view(context, request):
    return {"page_context": context,
            "page": context.node}


def root_factory(request):
    class Resource(object):
        def __init__(self, subobjects, node):
            self.subobjects = subobjects
            self.node = node

        def __getitem__(self, name):
            return self.subobjects[name]

        def __repr__(self):
            return "<%s>" % self.node

    def recursive_node_to_dict(node):
        children = {str(c.slug): recursive_node_to_dict(c) for c in node.children}
        return Resource(children, node)

    query = request.dbsession.query(MPTTPages)
    nodes = query.filter_by(parent_id=None).all()
    tree = {}
    for node in nodes:
        tree[str(node.slug)] = Resource(recursive_node_to_dict(node), node)

    return tree


def includeme(config):
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("sacrud_pages:templates")
    config.add_static_view('/sacrud_pages_static', 'sacrud_pages:static')

    config.add_route('sacrud_pages_move', '/sacrud_pages/move/{node}/{method}/{leftsibling}/')
    config.add_route('sacrud_pages_insert', '/sacrud_pages/insert/{parent_id}/')
    config.add_route('sacrud_pages_get_tree', '/sacrud_pages/get_tree/')
    config.add_route('sacrud_pages_visible', '/sacrud_pages/visible/{node}/')
    config.add_route('sacrud_pages_view', '/*traverse',
                     factory='sacrud_pages.root_factory')

    config.scan()
