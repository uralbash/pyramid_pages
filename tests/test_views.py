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

import transaction
from pyramid import testing
from pyramid.config import Configurator
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from sacrud_pages.models import MPTTPages


def add_fixture(model, fixtures, session):
    """
    Add fixtures to database.

    Example::

    hashes = ({'foo': {'foo': 'bar', '1': '2'}}, {'foo': {'test': 'data'}})
    add_fixture(TestHSTORE, hashes)
    """
    for fixture in fixtures:
        session.add(model(**fixture))


def add_mptt_pages(session):
    """ level           Nested sets tree1
          1                    1(1)22
                  _______________|___________________
                 |               |                   |
          2    2(2)5           6(4)11             12(7)21
                 |               ^                   ^
          3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                |          |
          4                                  14(9)15   18(11)19

        level           Nested sets tree2
          1                    1(12)22
                  _______________|___________________
                 |               |                   |
          2    2(13)5         6(15)11             12(18)21
                 |               ^                    ^
          3    3(14)4     7(16)8   9(17)10   13(19)16   17(21)20
                                                 |          |
          4                                  14(20)15   18(22)19

    """
    pages = (
        {'id': '1',  'slug': 'about-company',   'name': 'About company',    'visible': True, 'parent_id': None},
        {'id': '2',  'slug': 'we-love-gevent',  'name': u'We ♥  gevent',    'visible': True, 'parent_id': '1'},
        {'id': '3',  'slug': 'and-pyramid',     'name': 'And Pyramid',      'visible': True, 'parent_id': '2'},
        {'id': '4',  'slug': 'our-history',     'name': 'Our history',      'visible': False, 'parent_id': '1'},
        {'id': '5',  'slug': 'foo',             'name': 'foo',              'visible': True, 'parent_id': '4'},
        {'id': '6',  'slug': 'kompania-itcase', 'name': u'компания ITCase', 'visible': False, 'parent_id': '4'},
        {'id': '7',  'slug': 'our-strategy',    'name': 'Our strategy',     'visible': True, 'parent_id': '1'},
        {'id': '8',  'slug': 'wordwide',        'name': 'Wordwide',         'visible': True, 'parent_id': '7'},
        {'id': '9',  'slug': 'technology',      'name': 'Technology',       'visible': False, 'parent_id': '8'},
        {'id': '10', 'slug': 'what-we-do',      'name': 'What we do',       'visible': True,  'parent_id': '7'},
        {'id': '11', 'slug': 'at-a-glance',     'name': 'at a glance',      'visible': True,  'parent_id': '10'},

        {'id': '12', 'slug': 'foo12', 'name': 'foo12', 'visible': True, 'parent_id': None, 'tree_id': '12'},
        {'id': '13', 'slug': 'foo13', 'name': 'foo13', 'visible': False, 'parent_id': '12', 'tree_id': '12'},
        {'id': '14', 'slug': 'foo14', 'name': 'foo14', 'visible': False, 'parent_id': '13', 'tree_id': '12'},
        {'id': '15', 'slug': 'foo15', 'name': 'foo15', 'visible': True, 'parent_id': '12', 'tree_id': '12'},
        {'id': '16', 'slug': 'foo16', 'name': 'foo16', 'visible': True, 'parent_id': '15', 'tree_id': '12'},
        {'id': '17', 'slug': 'foo17', 'name': 'foo17', 'visible': True, 'parent_id': '15', 'tree_id': '12'},
        {'id': '18', 'slug': 'foo18', 'name': 'foo18', 'visible': True, 'parent_id': '12', 'tree_id': '12'},
        {'id': '19', 'slug': 'foo19', 'name': 'foo19', 'visible': True, 'parent_id': '18', 'tree_id': '12'},
        {'id': '20', 'slug': 'foo20', 'name': 'foo20', 'visible': True, 'parent_id': '19', 'tree_id': '12'},
        {'id': '21', 'slug': 'foo21', 'name': 'foo21', 'visible': True, 'parent_id': '18', 'tree_id': '12'},
        {'id': '22', 'slug': 'foo22', 'name': 'foo22', 'visible': True, 'parent_id': '21', 'tree_id': '12'},
    )
    add_fixture(MPTTPages, pages, session)
    transaction.commit()


def get_app(DBSession):
    config = Configurator()
    settings = config.registry.settings
    settings['sqlalchemy.url'] = DBSession.bind.engine.url

    # Database
    try:
        MPTTPages.__table__.drop(DBSession.bind.engine)
    except:
        pass
    MPTTPages.__table__.create(DBSession.bind.engine)
    transaction.commit()
    add_mptt_pages(DBSession)

    # SACRUD
    config.include('sacrud.pyramid_ext', route_prefix='/admin')
    settings['sacrud.models'] = {'Pages': [MPTTPages], }

    # sacrud_pages - put it after all routes
    config.include("sacrud_pages")

    config.scan()
    return config.make_wsgi_app()


class BaseTest(unittest.TestCase):

    def setUp(self):
        dburl = "sqlite:///test.sqlite"
        engine = create_engine(dburl)
        DBSession = scoped_session(
            sessionmaker(extension=ZopeTransactionExtension()))
        DBSession.configure(bind=engine)
        self.DBSession = DBSession

        app = get_app(DBSession)

        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        del self.testapp

    def get_db(self, request):
        return self.DBSession


class RootFactoryTest(BaseTest):

    def _callFUT(self, request):
        from sacrud_pages.routes import root_factory
        return root_factory(request)

    def test_it(self):
        request = testing.DummyRequest()
        request.set_property(self.get_db, 'dbsession', reify=True)
        tree = self._callFUT(request)
        self.assertEqual(str(tree),
                         "{'about-company': <About company>, 'foo12': <foo12>}")
        self.assertEqual(str(tree['about-company'].__getitem__('our-history')),
                         '<Our history>')
