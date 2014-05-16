#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
test models of sacrud_pages
"""

import unittest

from sqlalchemy import Column, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sacrud.common.sa_helpers import TableProperty
from sacrud_pages.models import BasePages

Base = declarative_base()


class MPTTPages(BasePages, Base):
    __tablename__ = "mptt_pages"

    id = Column(Integer, primary_key=True)

    @TableProperty
    def sacrud_list_col(cls):
        col = cls.columns
        return [col.name, col.level, col.tree_id,
                col.parent_id, col.left, col.right]

    @TableProperty
    def sacrud_detail_col(cls):
        col = cls.columns
        return [('', [col.name, col.slug, col.description, col.visible]),
                ('Redirection', [col.redirect_url, col.redirect_page,
                                 col.redirect_type]),
                ('SEO', [col.seo_title, col.seo_keywords, col.seo_description,
                         col.seo_metatags])
                ]

MPTTPages.register_tree()


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
    session.commit()


class TestTree(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        MPTTPages.__table__.create(self.engine)
        self.session.commit()
        add_mptt_pages(self.session)

    def tearDown(self):
        pass

    def test_tree_initialize(self):
        self.assertEqual([(1, u'About company', None),
                          (2, u'We \u2665  gevent', 1),
                          (3, u'And Pyramid', 2),
                          (4, u'Our history', 1), (5, u'foo', 4),
                          (6, u'\u043a\u043e\u043c\u043f\u0430\u043d\u0438\u044f ITCase', 4),
                          (7, u'Our strategy', 1), (8, u'Wordwide', 7),
                          (9, u'Technology', 8), (10, u'What we do', 7),
                          (11, u'at a glance', 10), (12, u'foo12', None),
                          (13, u'foo13', 12), (14, u'foo14', 13),
                          (15, u'foo15', 12), (16, u'foo16', 15),
                          (17, u'foo17', 15), (18, u'foo18', 12),
                          (19, u'foo19', 18), (20, u'foo20', 19),
                          (21, u'foo21', 18), (22, u'foo22', 21)],
                         self.session.query(MPTTPages.id,
                                            MPTTPages.name,
                                            MPTTPages.parent_id).all())

    def test_repr(self):
        page = self.session.query(MPTTPages).filter_by(id=1).one()
        self.assertEqual(page.__repr__(), "About company")

    def test_get_url(self):
        page = self.session.query(MPTTPages).filter_by(id=6).one()
        url = page.get_url()
        self.assertEqual(u'about-company/our-history/kompania-itcase', url)

