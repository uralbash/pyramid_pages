#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
CONFIG_MODELS = 'pyramid_pages.models'
CONFIG_DBSESSION = 'pyramid_pages.dbsession'


def includeme(config):
    config.include('.assets')
    config.include('.routes')
