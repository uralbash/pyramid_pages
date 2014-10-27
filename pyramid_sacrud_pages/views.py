#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Views for sacrud_pages
"""
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

from sacrud.common import pk_to_list

from .common import get_pages_model


def _get_redirect_code(node):
    if node.redirect_type:
        return node.redirect_type[0]
    return '200'


@view_config(route_name='sacrud_pages_move', renderer='json',
             permission=NO_PERMISSION_REQUIRED)
def page_move(request):
    node = request.matchdict['node']
    method = request.matchdict['method']
    left_sibling = request.matchdict['leftsibling']

    table = get_pages_model(request.registry.settings)
    pk = getattr(table, table.get_pk())
    page = request.dbsession.query(table).filter(pk == node).one()

    if method == 'inside':
        page.move_inside(left_sibling)
    if method == 'after':
        page.move_after(left_sibling)
    if method == 'before':
        page.move_before(left_sibling)
    return ''


@view_config(route_name='sacrud_pages_get_tree', renderer='json',
             permission=NO_PERMISSION_REQUIRED)
def get_tree(request):
    def fields(node):
        pk = getattr(node, node.get_pk())
        redirect_code = _get_redirect_code(node)
        url_delete = request.route_url('sa_delete', table=node.__tablename__,
                                       pk=pk_to_list(node))
        url_update = request.route_url('sa_update', table=node.__tablename__,
                                       pk=pk_to_list(node))
        url_visible = request.route_url('sacrud_pages_visible', node=pk)
        return {'visible': node.visible,
                'CSSredirect': 'jqtree-redirect-%s' % redirect_code,
                'redirect': '%s' % (node.redirect or node.redirect_url or ''),
                'redirect_code': '%s' % redirect_code,
                'url_delete': url_delete,
                'url_update': url_update,
                'url_visible': url_visible,
                }
    table = get_pages_model(request.registry.settings)
    return table.get_tree(request.dbsession, json=True, json_fields=fields)


@view_config(route_name='sacrud_pages_visible', renderer='json',
             permission=NO_PERMISSION_REQUIRED)
def page_visible(request):
    node = request.matchdict['node']
    table = get_pages_model(request.registry.settings)
    pk = getattr(table, table.get_pk())
    node = request.dbsession.query(table).filter(pk == node).one()
    node.visible = not node.visible
    request.dbsession.add(node)
    request.dbsession.flush()

    return {"visible": node.visible}


@view_config(route_name='sacrud_pages_view',
             renderer='pyramid_sacrud_pages/index.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def page_view(context, request):
    if type(context) == dict:
        if request.path in context:
            context = context[request.path]

    if not hasattr(context, 'node'):
        raise HTTPNotFound

    page = context.node

    if not page.visible:
        raise HTTPNotFound

    context = {'page': page,
               'page_resource': context,
               }

    redirect_type = _get_redirect_code(page)

    if page.redirect_page:
        if redirect_type == '200':
            context['page'] = page.redirect
        else:
            return Response(status_code=int(redirect_type),
                            location='/'+page.redirect.get_url())
    if page.redirect_url:
        return Response(status_code=int(redirect_type),
                        location=page.redirect_url)
    return context
