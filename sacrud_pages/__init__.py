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


@view_config(route_name='mptt_pages', renderer='/sacrud_pages/base.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def index_view(request):
    pages = request.dbsession.query(MPTTPages)\
        .filter_by(parent_id=None).order_by(MPTTPages.id).all()
    context = {'pages': pages}
    return context


@view_config(route_name='page_move', renderer='json',
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
    # TODO: return JSON tree
    return ''


@view_config(route_name='page_insert', renderer='json',
             permission=NO_PERMISSION_REQUIRED)
def page_insert(request):
    parent_id = request.matchdict['parent_id']
    node = MPTTPages(parent_id=parent_id)
    request.dbsession.add(node)
    request.dbsession.flush()

    return {'label': str(node), 'id': node.id}


@view_config(route_name='get_tree', renderer='json',
             permission=NO_PERMISSION_REQUIRED)
def get_tree(request):
    def recursive_node_to_dict(node):
        result = {
            'id': node.id,
            'label': str(node),
        }
        children = [recursive_node_to_dict(c) for c in node.children]
        if children:
            result['children'] = children
        return result
    pages = request.dbsession.query(MPTTPages)\
        .filter_by(parent_id=None).order_by(MPTTPages.id).all()
    tree = []
    for i, page in enumerate(pages):
        tree.append(recursive_node_to_dict(page))

    return tree


def includeme(config):
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("sacrud_pages:templates")
    config.add_static_view('/sacrud_pages_static', 'sacrud_pages:static')
    config.add_route('mptt_pages', '/mptt_pages/')
    config.add_route('page_move', '/move/{node}/{method}/{leftsibling}/')
    config.add_route('page_insert', '/insert_to/{parent_id}')
    config.add_route('get_tree', '/get_tree/')

    config.scan()
