#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
__version__ = "0.0.1a"


def includeme(config):
    config.include('pyramid_jinja2')
    config.add_jinja2_extension('jinja2.ext.with_')
    config.add_jinja2_search_path("pyramid_sacrud_pages:templates")
    config.add_static_view('/static_sacrud_pages', 'pyramid_sacrud_pages:static')

    config.include('pyramid_sacrud_pages.routes')
    config.scan()
