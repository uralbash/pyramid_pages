#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Views for pages
"""
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response


def page_view(context, request):
    if type(context) == dict:
        if request.path in context:
            context = context[request.path]

    if not hasattr(context, 'node'):
        raise HTTPNotFound

    page = context.node

    if not page.visible:
        raise HTTPNotFound

    if all([hasattr(page, attr)
            for attr in ('redirect', 'redirect_url', 'redirect_page')]):
        redirect_type = getattr(page, 'redirect_type', '200') or '200'

        if page.redirect_page:
            if redirect_type == '200':
                page = page.redirect
            else:
                return Response(status_code=int(redirect_type),
                                location='/' + page.redirect.get_url())
        if page.redirect_url:
            return Response(status_code=int(redirect_type),
                            location=page.redirect_url)
    return {'page': page}
