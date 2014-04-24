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
        .filter_by(parent_id=None)
    context = {'pages': pages}
    return context


def includeme(config):
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path("sacrud_pages:templates")

    config.add_static_view('/sacrud_pages_static', 'sacrud_pages:static')

    config.add_route('mptt_pages', '/mptt_pages')

    config.scan()