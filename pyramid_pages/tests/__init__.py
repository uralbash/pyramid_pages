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
from paste.deploy.loadwsgi import appconfig

from webtest import TestApp
from mock import Mock

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from app.db import Session
from app.db import Entity  # base declarative object
from app import main
import os
here = os.path.dirname(__file__)
settings = appconfig('config:' + os.path.join(here, '../../', 'test.ini'))


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        cls.Session = sessionmaker()

    def setUp(self):
        connection = self.engine.connect()

        # begin a non-ORM transaction
        self.trans = connection.begin()

        # bind an individual Session to the connection
        Session.configure(bind=connection)
        self.session = self.Session(bind=connection)
        Entity.session = self.session

    def tearDown(self):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        self.trans.rollback()
        self.session.close()
