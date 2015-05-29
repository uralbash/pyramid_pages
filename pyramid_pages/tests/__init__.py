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

from pyramid_pages_example import MPTTNews, MPTTPages, Base, main  # noqa

settings = {'sqlalchemy.url': 'sqlite:///test.sqlite'}


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        cls.DBSession = sessionmaker()

    def setUp(self):
        # bind an individual Session to the connection
        self.dbsession = self.DBSession(bind=self.engine)
        self.create_db()

    def tearDown(self):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        Base.metadata.drop_all(bind=self.engine)
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
    @classmethod
    def setUpClass(cls):
        cls.app = main({}, **settings)
        super(IntegrationTestBase, cls).setUpClass()

    def setUp(self):
        self.app = TestApp(self.app)
        self.config = testing.setUp()
        super(IntegrationTestBase, self).setUp()
