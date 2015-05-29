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
from pyramid.httpexceptions import HTTPNotFound
from pyramid.traversal import ResourceTreeTraverser
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from pyramid_pages.views import page_view
from pyramid_pages_example import main, MPTTPages


# def get_app():
#     return main({})
#
#
# def mock_dbsession(request={}):
#     dburl = "sqlite:///test.sqlite"
#     engine = create_engine(dburl)
#     DBSession = scoped_session(sessionmaker())
#     DBSession.configure(bind=engine)
#     return DBSession

#
# class BaseTest(unittest.TestCase):
#
#     def make_dummy_request(self):
#         request = testing.DummyRequest()
#
#         class Settings(object):
#             pass
#
#         request.registry = Settings()
#         request.registry.settings = {}
#         settings = request.registry.settings
#         settings['pyramid_pages.models'] = {
#             'pages': MPTTPages,
#         }
#         return request
#
#     def setUp(self):
#         app = get_app()
#
#         from webtest import TestApp
#         self.testapp = TestApp(app)
#         self.request = self.make_dummy_request()
#
#     def tearDown(self):
#         del self.testapp

#
# class RootFactoryTest(BaseTest):
#
#     def _callFUT(self, request):
#         from pyramid_pages.routes import page_factory
#         return page_factory(request)
#
#     def test_it(self):
#         def _p(name):
#             return DBSession.query(MPTTPages).filter_by(name=name).one()
#
#         request = self.request
#         request.set_property(mock_dbsession, 'dbsession', reify=True)
#         DBSession = request.dbsession
#         tree = self._callFUT(request)
#         self.assertEqual(tree['about-company'].node, _p("About company"))
#         self.assertEqual(tree['foo12'].node, _p("foo12"))
#         self.assertEqual(str(tree['about-company'].__getitem__('our-history')),
#                          '<Our history>')
#
#         # root node with slash path
#         p = _p("foo12")
#         p.slug = '/'
#         DBSession.add(p)
#         DBSession.commit()
#         tree = self._callFUT(request)
#         self.assertEqual({u'about-company': _p("About company"),
#                           u'foo15': _p("foo15"), u'foo13': _p("foo13"),
#                           '/': _p("foo12"), u'foo18': _p("foo18")},
#                          {k: v.node for k, v in tree.items()})


# class ViewPageTest(BaseTest):
#     def get_request(self, page):
#         request = testing.DummyRequest()
#         request.path = '/' + page.get_url()
#         request.matchdict['traverse'] = request.path.split('/')
#         return request
#
#     def test_location(self):
#         DBSession = mock_dbsession()
#         page = DBSession.query(MPTTPages).filter_by(name="at a glance").one()
#         request = self.get_request(page)
#         context = get_view_context(DBSession, request)
#         response = page_view(context, request)
#         self.assertEqual(response['page_resource'].node, page)
#         self.assertEqual(response['page'], page)
#
#     def test_redirect_200(self):
#         DBSession = mock_dbsession()
#         page = DBSession.query(MPTTPages).filter_by(name="at a glance").one()
#         redirect = DBSession.query(MPTTPages).filter_by(name="foo16").one()
#         page.redirect_type = "200"
#         page.redirect_page = redirect.id
#         DBSession.add(page)
#         DBSession.commit()
#         request = self.get_request(page)
#         context = get_view_context(DBSession, request)
#         response = page_view(context, request)
#         self.assertEqual(response['page_resource'].node, page)
#         self.assertEqual(response['page'], redirect)
#
#     def test_redirect_url(self):
#         DBSession = mock_dbsession()
#         page = DBSession.query(MPTTPages).filter_by(name="at a glance").one()
#         page.redirect_url = "http://ya.ru"
#         DBSession.add(page)
#         DBSession.commit()
#         request = self.get_request(page)
#         context = get_view_context(DBSession, request)
#         response = page_view(context, request)
#         self.assertEqual(response.location, "http://ya.ru")
#
#     def test_redirect_301(self):
#         DBSession = mock_dbsession()
#         page = DBSession.query(MPTTPages).filter_by(name="at a glance").one()
#         redirect = DBSession.query(MPTTPages).filter_by(name="foo16").one()
#         page.redirect_type = "301"
#         page.redirect_page = redirect.id
#         DBSession.add(page)
#         DBSession.commit()
#         request = self.get_request(page)
#         context = get_view_context(DBSession, request)
#         response = page_view(context, request)
#         self.assertEqual(response.location, '/foo12/foo15/foo16')
#         self.assertEqual(response.status_code, 301)
#
#     def test_visible_false(self):
#         DBSession = mock_dbsession()
#         page = DBSession.query(MPTTPages).filter_by(name="Technology").one()
#         request = self.get_request(page)
#         context = get_view_context(DBSession, request)
#         try:
#             page_view(context, request)
#         except HTTPNotFound:
#             pass
#
#     def test_node_with_slash_path(self):
#         DBSession = mock_dbsession()
#         page = DBSession.query(MPTTPages).filter_by(name="foo12").one()
#         page.slug = '/'
#         DBSession.add(page)
#         DBSession.commit()
#         request = self.get_request(page)
#         context = get_view_context(DBSession, request)
#         response = page_view(context, request)
#         self.assertEqual(response['page_resource'].node, page)
#         self.assertEqual(response['page'], page)
#
#     def test_root_path_404(self):
#         DBSession = mock_dbsession()
#         request = testing.DummyRequest()
#         request.path = '/'
#         context = get_view_context(DBSession, request)
#         try:
#             page_view(context, request)
#         except HTTPNotFound:
#             pass
#

# class GetTreeTest(BaseTest):
#
#     def test_it(self):
#         response = self.testapp.get('/sacrud_pages/get_tree/')
#         self.assertEqual([{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/1', u'label': u'About company', u'visible': True, u'id': 1, u'url_update': u'http://localhost/admin/mptt_pages/update/id/1', u'children': [{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/2', u'label': u'We \u2665  gevent', u'visible': True, u'id': 2, u'url_update': u'http://localhost/admin/mptt_pages/update/id/2', u'children': [{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/3', u'label': u'And Pyramid', u'visible': True, u'url_update': u'http://localhost/admin/mptt_pages/update/id/3', u'id': 3, u'url_visible': u'http://localhost/sacrud_pages/visible/3/'}], u'url_visible': u'http://localhost/sacrud_pages/visible/2/'}, {u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/4', u'label': u'Our history', u'visible': False, u'id': 4, u'url_update': u'http://localhost/admin/mptt_pages/update/id/4', u'children': [{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/5', u'label': u'foo', u'visible': True, u'url_update': u'http://localhost/admin/mptt_pages/update/id/5', u'id': 5, u'url_visible': u'http://localhost/sacrud_pages/visible/5/'}, {u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/6', u'label': u'\u043a\u043e\u043c\u043f\u0430\u043d\u0438\u044f ITCase', u'visible': False, u'url_update': u'http://localhost/admin/mptt_pages/update/id/6', u'id': 6, u'url_visible': u'http://localhost/sacrud_pages/visible/6/'}], u'url_visible': u'http://localhost/sacrud_pages/visible/4/'}, {u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/7', u'label': u'Our strategy', u'visible': True, u'id': 7, u'url_update': u'http://localhost/admin/mptt_pages/update/id/7', u'children': [{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/8', u'label': u'Wordwide', u'visible': True, u'id': 8, u'url_update': u'http://localhost/admin/mptt_pages/update/id/8', u'children': [{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/9', u'label': u'Technology', u'visible': False, u'url_update': u'http://localhost/admin/mptt_pages/update/id/9', u'id': 9, u'url_visible': u'http://localhost/sacrud_pages/visible/9/'}], u'url_visible': u'http://localhost/sacrud_pages/visible/8/'}, {u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/10', u'label': u'What we do', u'visible': True, u'id': 10, u'url_update': u'http://localhost/admin/mptt_pages/update/id/10', u'children': [{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/11', u'label': u'at a glance', u'visible': True, u'url_update': u'http://localhost/admin/mptt_pages/update/id/11', u'id': 11, u'url_visible': u'http://localhost/sacrud_pages/visible/11/'}], u'url_visible': u'http://localhost/sacrud_pages/visible/10/'}], u'url_visible': u'http://localhost/sacrud_pages/visible/7/'}], u'url_visible': u'http://localhost/sacrud_pages/visible/1/'}, {u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/12', u'label': u'foo12', u'visible': True, u'id': 12, u'url_update': u'http://localhost/admin/mptt_pages/update/id/12', u'children': [{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/13', u'label': u'foo13', u'visible': False, u'id': 13, u'url_update': u'http://localhost/admin/mptt_pages/update/id/13', u'children': [{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/14', u'label': u'foo14', u'visible': False, u'url_update': u'http://localhost/admin/mptt_pages/update/id/14', u'id': 14, u'url_visible': u'http://localhost/sacrud_pages/visible/14/'}], u'url_visible': u'http://localhost/sacrud_pages/visible/13/'}, {u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/15', u'label': u'foo15', u'visible': True, u'id': 15, u'url_update': u'http://localhost/admin/mptt_pages/update/id/15', u'children': [{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/16', u'label': u'foo16', u'visible': True, u'url_update': u'http://localhost/admin/mptt_pages/update/id/16', u'id': 16, u'url_visible': u'http://localhost/sacrud_pages/visible/16/'}, {u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/17', u'label': u'foo17', u'visible': True, u'url_update': u'http://localhost/admin/mptt_pages/update/id/17', u'id': 17, u'url_visible': u'http://localhost/sacrud_pages/visible/17/'}], u'url_visible': u'http://localhost/sacrud_pages/visible/15/'}, {u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/18', u'label': u'foo18', u'visible': True, u'id': 18, u'url_update': u'http://localhost/admin/mptt_pages/update/id/18', u'children': [{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/19', u'label': u'foo19', u'visible': True, u'id': 19, u'url_update': u'http://localhost/admin/mptt_pages/update/id/19', u'children': [{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/20', u'label': u'foo20', u'visible': True, u'url_update': u'http://localhost/admin/mptt_pages/update/id/20', u'id': 20, u'url_visible': u'http://localhost/sacrud_pages/visible/20/'}], u'url_visible': u'http://localhost/sacrud_pages/visible/19/'}, {u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/21', u'label': u'foo21', u'visible': True, u'id': 21, u'url_update': u'http://localhost/admin/mptt_pages/update/id/21', u'children': [{u'redirect': u'', u'redirect_code': u'200', u'CSSredirect': u'jqtree-redirect-200', u'url_delete': u'http://localhost/admin/mptt_pages/delete/id/22', u'label': u'foo22', u'visible': True, u'url_update': u'http://localhost/admin/mptt_pages/update/id/22', u'id': 22, u'url_visible': u'http://localhost/sacrud_pages/visible/22/'}], u'url_visible': u'http://localhost/sacrud_pages/visible/21/'}], u'url_visible': u'http://localhost/sacrud_pages/visible/18/'}], u'url_visible': u'http://localhost/sacrud_pages/visible/12/'}],
#                          response.json_body)
#
#
# class PageMoveTest(BaseTest):
#
#     def _callFUT(self, request):
#         from ps_pages.views import page_move
#         return page_move(request)
#
#     def test_inside_method(self):
#         request = self.request
#         request.set_property(mock_dbsession, 'dbsession', reify=True)
#         request.matchdict['node'] = 5
#         request.matchdict['method'] = 'inside'
#         request.matchdict['leftsibling'] = 11
#         response = self._callFUT(request)
#         request.dbsession.commit()
#         moved_page = request.dbsession.query(MPTTPages).filter_by(id=5).one()
#         self.assertEqual('', response)
#         self.assertEqual(11, moved_page.parent_id)
#
#     def test_after_method(self):
#         request = self.request
#         request.set_property(mock_dbsession, 'dbsession', reify=True)
#         request.matchdict['node'] = 5
#         request.matchdict['method'] = 'after'
#         request.matchdict['leftsibling'] = 11
#         response = self._callFUT(request)
#         request.dbsession.commit()
#         moved_page = request.dbsession.query(MPTTPages).filter_by(id=5).one()
#         self.assertEqual('', response)
#         self.assertEqual(10, moved_page.parent_id)
#
#     def test_before_method(self):
#         request = self.request
#         request.set_property(mock_dbsession, 'dbsession', reify=True)
#         request.matchdict['node'] = 7
#         request.matchdict['method'] = 'before'
#         request.matchdict['leftsibling'] = 1
#         response = self._callFUT(request)
#         request.dbsession.commit()
#         moved_page = request.dbsession.query(MPTTPages).filter_by(id=7).one()
#         self.assertEqual('', response)
#         self.assertEqual(None, moved_page.parent_id)
#         self.assertEqual(1, moved_page.tree_id)
