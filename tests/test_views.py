#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Test for views
"""
import unittest

from pyramid import testing
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from sacrud_pages.models import MPTTPages

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


def get_app():
    config = Configurator()
    settings = config.registry.settings
    settings['sqlalchemy.url'] = "sqlite:///example.sqlite"

    # Database
    engine = engine_from_config(settings)
    DBSession.configure(bind=engine)

    # SACRUD
    config.include('sacrud.pyramid_ext', route_prefix='/admin')
    settings['sacrud.models'] = {'Pages': [MPTTPages], }

    # sacrud_pages - put it after all routes
    config.include("sacrud_pages")

    config.scan()
    return config.make_wsgi_app()


class BaseTest(unittest.TestCase):

    def setUp(self):
        app = get_app()

        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        del self.testapp


class ViewsTest(BaseTest):

    def _request(self):
        request = testing.DummyRequest()
        config = testing.setUp(request=request)
        config.registry.settings['sqlalchemy.url'] = "sqlite://"
        config.include('sacrud.pyramid_ext', route_prefix='/admin')

        # SACRUD
        config.include('sacrud.pyramid_ext', route_prefix='/admin')
        settings = config.registry.settings
        settings['sacrud.models'] = {'Pages': [MPTTPages], }

        # sacrud_pages - put it after all routes
        config.include("sacrud_pages")

        return request

    def test_page_move(self):
        request = self._request()
        print request
