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
    # TODO: return JSON tree
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


def includeme(config):
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("sacrud_pages:templates")
    config.add_static_view('/sacrud_pages_static', 'sacrud_pages:static')

    config.add_route('sacrud_pages_move', '/sacrud_pages/move/{node}/{method}/{leftsibling}/')
    config.add_route('sacrud_pages_insert', '/sacrud_pages/insert/{parent_id}')
    config.add_route('sacrud_pages_get_tree', '/sacrud_pages/get_tree/')

    config.scan()
