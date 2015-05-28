#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Main for example
"""
import transaction
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import Column, Integer, engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from ps_pages.common import get_pages_menu
from ps_pages.models import BasePages, PageMixin
from ps_pages.routes import PageResource
from sqlalchemy_mptt import BaseNestedSets

Base = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class MPTTPages(BasePages, Base):
    __tablename__ = "mptt_pages"

    id = Column('id', Integer, primary_key=True)


class MPTTNews(BaseNestedSets, PageMixin, Base):
    __tablename__ = "mptt_news"

    id = Column('id', Integer, primary_key=True)


def add_fixture(model, fixtures, session):
    """
    Add fixtures to database.

    Example::

    hashes = ({'foo': {'foo': 'bar', '1': '2'}}, {'foo': {'test': 'data'}})
    add_fixture(TestHSTORE, hashes)
    """
    for fixture in fixtures:
        session.add(model(**fixture))


def add_mptt_tree(session):
    session.query(MPTTPages).delete()
    session.query(MPTTNews).delete()
    transaction.commit()
    tree1 = (
        {'id': '1', 'slug': 'about-company', 'name': 'About company',
         'visible': True,
         'in_menu': True,
         'parent_id': None},
        {'id': '2', 'slug': 'we-love-gevent', 'name': u'We ♥ gevent',
         'visible': True,
         'in_menu': True,
         'parent_id': '1'},
        {'id': '3', 'slug': 'and-pyramid', 'name': 'And Pyramid',
         'visible': True,
         'in_menu': True,
         'parent_id': '2'},
        {'id': '4', 'slug': 'redirect-301',
         'name': 'Redirect 301 to we-love-gevent',
         'redirect_type': '301',
         'redirect_page': 2,
         'visible': True,
         'in_menu': True,
         'parent_id': '1'},
        {'id': '5', 'slug': 'redirect-200',
         'name': 'Redirect 200 to about-company',
         'redirect_type': '200',
         'redirect_page': 1,
         'visible': True, 'in_menu': True,
         'parent_id': '4'},
        {'id': '6', 'slug': 'kompania-itcase', 'name': u'компания ITCase',
         'redirect_type': '302',
         'redirect_url': 'http://itcase.pro/',
         'visible': True,
         'in_menu': True,
         'parent_id': '4'},
        {'id': '7', 'slug': 'our-strategy', 'name': 'Our strategy',
         'visible': True, 'parent_id': '1'},
        {'id': '8', 'slug': 'wordwide', 'name': 'Wordwide', 'visible': True,
         'parent_id': '7'},
        {'id': '9', 'slug': 'technology', 'name': 'Technology',
         'visible': False, 'parent_id': '8'},
        {'id': '10', 'slug': 'what-we-do', 'name': 'What we do',
         'visible': True, 'parent_id': '7'},
        {'id': '11', 'slug': 'at-a-glance', 'name': 'at a glance',
         'visible': True, 'parent_id': '10'},
    )

    tree2 = (
        {'id': '12', 'slug': 'foo12', 'name': 'foo12', 'visible': True,
         'in_menu': True,
         'parent_id': None, 'tree_id': '2'},
        {'id': '13', 'slug': 'foo13', 'name': 'foo13', 'visible': False,
         'in_menu': True,
         'parent_id': '12', 'tree_id': '2'},
        {'id': '14', 'slug': 'foo14', 'name': 'foo14', 'visible': False,
         'in_menu': True,
         'parent_id': '13', 'tree_id': '2'},
        {'id': '15', 'slug': 'foo15', 'name': 'foo15', 'visible': True,
         'in_menu': True,
         'parent_id': '12', 'tree_id': '2'},
        {'id': '16', 'slug': 'foo16', 'name': 'foo16', 'visible': True,
         'in_menu': True,
         'parent_id': '15', 'tree_id': '2'},
        {'id': '17', 'slug': 'foo17', 'name': 'foo17', 'visible': True,
         'parent_id': '15', 'tree_id': '2'},
        {'id': '18', 'slug': 'foo18', 'name': 'foo18', 'visible': True,
         'in_menu': True,
         'parent_id': '12', 'tree_id': '2'},
        {'id': '19', 'slug': 'foo19', 'name': 'foo19', 'visible': True,
         'parent_id': '18', 'tree_id': '2'},
        {'id': '20', 'slug': 'foo20', 'name': 'foo20', 'visible': True,
         'parent_id': '19', 'tree_id': '2'},
        {'id': '21', 'slug': 'foo21', 'name': 'foo21', 'visible': True,
         'parent_id': '18', 'tree_id': '2'},
        {'id': '22', 'slug': 'foo22', 'name': 'foo22', 'visible': True,
         'parent_id': '21', 'tree_id': '2'},
    )
    news = (
        {'id': '1', 'slug': 'sed-ut-perspiciatis',
         'name': 'Sed ut perspiciatis',
         'visible': True,
         'in_menu': True,
         'parent_id': None, 'tree_id': '1'},
        {'id': '2', 'slug': 'dolor-sit-amet-consectetur-adipisc',
         'name': 'Dolor sit, amet, consectetur, adipisc',
         'visible': True,
         'in_menu': True,
         'parent_id': '1', 'tree_id': '1'},
        {'id': '3', 'slug': 'foo14', 'name': 'foo14',
         'visible': True,
         'in_menu': True,
         'parent_id': '2', 'tree_id': '1'},
        {'id': '4', 'slug': 'foo15', 'name': 'foo15',
         'visible': True,
         'in_menu': True,
         'parent_id': '3', 'tree_id': '1'}
    )
    add_fixture(MPTTPages, tree1, session)
    add_fixture(MPTTPages, tree2, session)
    add_fixture(MPTTNews, news, session)


def index_view(request):
    def page_menu(**kwargs):
        return get_pages_menu(DBSession, MPTTPages, **kwargs)
    return {'page_menu': page_menu}


def index_page_factory(request):
    settings = request.registry.settings
    models = settings['ps_pages.models']
    table = models[''] or models['/']
    dbsession = settings['ps_pages.dbsession']
    node = dbsession.query(table)\
        .filter(table.slug.is_('about-company')).first()
    if not node:
        raise HTTPNotFound
    return PageResource(node)


def main(global_settings, **settings):
    config = Configurator(
        settings=settings,
        session_factory=SignedCookieSessionFactory('itsaseekreet')
    )

    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('ps_pages_example:templates')

    config.add_route('index', '/', factory=index_page_factory)
    config.add_view(index_view,
                    route_name='index',
                    context=PageResource,
                    renderer='index.jinja2')

    # Database
    settings = config.registry.settings
    settings['sqlalchemy.url'] = "sqlite:///example.sqlite"
    engine = engine_from_config(settings)
    DBSession.configure(bind=engine)
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        add_mptt_tree(DBSession)
        transaction.commit()
    except Exception as e:
        print(e)

    # ps_pages
    config.include("ps_pages")
    settings['ps_pages.dbsession'] = DBSession
    settings['ps_pages.models'] = {
        '': MPTTPages,
        'pages': MPTTPages,
        'news': MPTTNews
    }

    return config.make_wsgi_app()

if __name__ == '__main__':
    settings = {}
    app = main({}, **settings)

    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
