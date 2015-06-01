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
    page = context.node

    if not page.visible:
        raise HTTPNotFound

    if all([hasattr(page, attr)
            for attr in ('redirect', 'redirect_url', 'redirect_page')]):
        # Prohibit redirect both url and page
        if page.redirect_url and page.redirect_page:
            raise HTTPNotFound

        # check redirect type
        if not page.redirect_type and page.redirect_url:
            redirect_type = '302'
        elif not page.redirect_type and page.redirect_page:
            redirect_type = '200'
        else:
            redirect_type = str(page.redirect_type)

        # Prohibit redirect itself
        if page.redirect == page and redirect_type != '200':
            raise HTTPNotFound

        # Redirect to Page
        if page.redirect_page:
            if not page.redirect.visible:
                raise HTTPNotFound
            if redirect_type == '200':
                page = page.redirect
            else:
                redirect_resource_url = request.resource_url(
                    context.__class__(page.redirect, context.prefix))
                return Response(status_code=int(redirect_type),
                                location=redirect_resource_url)
        # Redirect to URL
        if page.redirect_url:
            if redirect_type == '200':
                raise HTTPNotFound
            return Response(status_code=int(redirect_type),
                            location=page.redirect_url)
    return {'page': page}
