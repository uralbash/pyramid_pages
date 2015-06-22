#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Base classes for tests
http://www.sontek.net/blog/2011/12/01/writing_tests_for_pyramid_and_sqlalchemy.html
"""
import unittest

from pyramid import testing
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from webtest import TestApp
from sqlalchemy_mptt import mptt_sessionmaker

import imp
imp.load_source('pyramid_pages_example', 'example/pyramid_pages_example.py')

from pyramid_pages_example import NewsPage, WebPage, Base, main, models  # noqa

settings = {
    'sqlalchemy.url': 'sqlite:///test.sqlite',
    'pyramid_pages.models': models
}


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        cls.DBSession = mptt_sessionmaker(sessionmaker())

    def setUp(self):
        # bind an individual Session to the connection
        self.dbsession = self.DBSession(bind=self.engine)
        self.create_db()

    def tearDown(self):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        self.drop_db()
        self.dbsession.close()

    def drop_db(self):
        Base.metadata.drop_all(bind=self.engine)
        self.dbsession.commit()

    def create_db(self):
        Base.metadata.create_all(bind=self.engine)
        self.dbsession.commit()


class UnitTestBase(BaseTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request)
        super(UnitTestBase, self).setUp()


class IntegrationTestBase(BaseTestCase):

    def setUp(self):
        self.app = TestApp(main({}, **settings))
        self.config = testing.setUp()
        super(IntegrationTestBase, self).setUp()
