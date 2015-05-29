# #! /usr/bin/env python
# # -*- coding: utf-8 -*-
# # vim:fenc=utf-8
# #
# # Copyright © 2014 uralbash <root@uralbash.ru>
# #
# # Distributed under terms of the MIT license.
#
# """
# test models of sacrud_pages
# """
#
# import unittest
# from collections import OrderedDict
#
# from sqlalchemy import Column, create_engine, Integer
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# from ps_pages.models import BasePages
# from .test_views import add_mptt_pages
#
# Base = declarative_base()
#
#
# class MPTTPages(Base, BasePages):
#     __tablename__ = "mptt_pages"
#
#     pk = Column('id', Integer, primary_key=True)
#     sqlalchemy_mptt_pk_name = 'pk'
#
#
# def get_page_by_name(session, name):
#     return session.query(MPTTPages).filter_by(name=name).one()
#
#
# class TestTree(unittest.TestCase):
#
#     def setUp(self):
#         self.engine = create_engine('sqlite:///:memory:')
#         Session = sessionmaker(bind=self.engine)
#         self.session = Session()
#         MPTTPages.__table__.create(self.engine)
#         self.session.commit()
#         add_mptt_pages(self.session)
#
#     def tearDown(self):
#         pass
#
#     def test_tree_initialize(self):
#         self.assertEqual(
#             [(1, u'About company', None),
#              (2, u'We \u2665  gevent', 1),
#              (3, u'And Pyramid', 2),
#              (4, u'Our history', 1), (5, u'foo', 4),
#              (6, u'\u043a\u043e\u043c\u043f\u0430\u043d\u0438\u044f ITCase', 4),
#              (7, u'Our strategy', 1), (8, u'Wordwide', 7),
#              (9, u'Technology', 8), (10, u'What we do', 7),
#              (11, u'at a glance', 10), (12, u'foo12', None),
#              (13, u'foo13', 12), (14, u'foo14', 13),
#              (15, u'foo15', 12), (16, u'foo16', 15),
#              (17, u'foo17', 15), (18, u'foo18', 12),
#              (19, u'foo19', 18), (20, u'foo20', 19),
#              (21, u'foo21', 18), (22, u'foo22', 21)],
#             self.session.query(MPTTPages.pk,
#                                MPTTPages.name,
#                                MPTTPages.parent_id).all())
#
#     def test_repr(self):
#         page = self.session.query(MPTTPages).filter_by(pk=1).one()
#         self.assertEqual(page.__repr__(), "About company")
#
#     def test_get_url(self):
#         page = self.session.query(MPTTPages).filter_by(pk=6).one()
#         url = page.get_url()
#         self.assertEqual(u'about-company/our-history/kompania-itcase', url)
#
#     def test_get_menu(self):
#         page = self.session.query(MPTTPages).filter_by(pk=6).one()
#
#         def get_page(name):
#             return get_page_by_name(self.session, name)
#
#         menu = page.get_menu()
#         self.assertEqual(
#             menu,
#             OrderedDict([(get_page('About company'),
#                           OrderedDict([(get_page(u'We ♥  gevent'), OrderedDict([(get_page('And Pyramid'), OrderedDict())]))])),
#                          (get_page('foo12'), OrderedDict([(get_page('foo15'), OrderedDict([(get_page('foo16'), OrderedDict())])), (get_page('foo18'), OrderedDict([(get_page('foo21'), OrderedDict([(get_page('foo22'), OrderedDict())]))]))]))])
#         )
#
#         menu = page.get_menu(to_lvl=2, trees=(1,))
#         self.assertEqual(menu,
#                          OrderedDict([(get_page('About company'),
#                                        OrderedDict([(get_page(u'We ♥  gevent'),
#                                                      OrderedDict())]))])
#                          )
#
#         menu = page.get_menu(to_lvl=-1)
#         self.assertEqual(menu, {})
#
#     def test_sacrud_css_class(self):
#         page = self.session.query(MPTTPages).filter_by(pk=6).one()
#         columns = page.__table__.c
#         css_classes = page.sacrud_css_class
#         self.assertEqual(css_classes,
#                          {'content': [columns.description],
#                           'tinymce': [columns.description],
#                           'name': [columns.name]})
