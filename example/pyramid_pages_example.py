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
from pyramid.events import BeforeRender
from pyramid.httpexceptions import HTTPNotFound
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import Column, Integer, engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from pyramid_pages.common import get_pages_menu
from pyramid_pages.models import BasePages, PageMixin
from pyramid_pages.routes import PageResource
from sqlalchemy_mptt import BaseNestedSets

Base = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

CONFIG_SQLALCHEMY_URL = 'sqlalchemy.url'
CONFIG_PYRAMID_PAGES_MODELS = 'pyramid_pages.models'
CONFIG_PYRAMID_PAGES_DBSESSION = 'pyramid_pages.dbsession'


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
        {'id': '1', 'slug': 'about-company', 'name': 'Hello Traversal World!',
         'visible': True,
         'in_menu': True,
         'description': '''Hello Traversal World! Hello Traversal World!
         Hello Traversal World!''',
         'parent_id': None},
        {'id': '2', 'slug': 'we-love-gevent', 'name': u'We ♥  gevent',
         'visible': True,
         'in_menu': True,
         'parent_id': '1'},
        {'id': '3', 'slug': 'and-pyramid', 'name': 'And Pyramid',
         'visible': True,
         'in_menu': True,
         'parent_id': '2'},

        # Redirect
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

        # Not visible
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

        # Deep tree
        {'id': '12', 'slug': 'and-aiohttp', 'name': 'and aiohttp!',
         'in_menu': True,
         'visible': True, 'parent_id': '3'},
        {'id': '13', 'slug': 'and-asyncio', 'name': 'and asyncio!',
         'in_menu': True,
         'visible': True, 'parent_id': '3'},
        {'id': '14', 'slug': 'and-beer', 'name': 'and beer!',
         'in_menu': True,
         'visible': True, 'parent_id': '12'},
        {'id': '15', 'slug': 'and-bear-to', 'name': 'and bear to!',
         'in_menu': True,
         'visible': True, 'parent_id': '14'},
    )

    tree2 = (
        {'id': '100', 'slug': 'countries', 'name': 'Countries',
         'visible': True,
         'in_menu': True,
         'parent_id': None, 'tree_id': '2'},
        {'id': '101', 'slug': 'africa', 'name': 'Africa',
         'visible': True,
         'in_menu': True,
         'parent_id': '100', 'tree_id': '2'},
        {'id': '102', 'slug': 'algeria', 'name': 'Algeria',
         'visible': True,
         'in_menu': True,
         'parent_id': '101', 'tree_id': '2'},
        {'id': '103', 'slug': 'marocco', 'name': 'Marocco',
         'visible': True,
         'in_menu': True,
         'parent_id': '101', 'tree_id': '2'},
        {'id': '104', 'slug': 'libya', 'name': 'Libya',
         'visible': True,
         'in_menu': True,
         'parent_id': '101', 'tree_id': '2'},
        {'id': '105', 'slug': 'somalia', 'name': 'Somalia',
         'visible': True,
         'in_menu': True,
         'parent_id': '101', 'tree_id': '2'},
        {'id': '106', 'slug': 'kenya', 'name': 'Kenya',
         'visible': True,
         'in_menu': True,
         'parent_id': '101', 'tree_id': '2'},
        {'id': '107', 'slug': 'mauritania', 'name': 'Mauritania',
         'visible': True,
         'in_menu': True,
         'parent_id': '101', 'tree_id': '2'},
        {'id': '108', 'slug': 'foo19', 'name': 'South Africa',
         'visible': True,
         'in_menu': True,
         'parent_id': '101', 'tree_id': '2'},

        {'id': '200', 'slug': 'america', 'name': 'America',
         'visible': True,
         'in_menu': True,
         'parent_id': '100', 'tree_id': '2'},
        {'id': '201', 'slug': 'north-america', 'name': 'North-America',
         'visible': True,
         'in_menu': True,
         'parent_id': '200', 'tree_id': '2'},
        {'id': '202', 'slug': 'Canada', 'name': 'Canada',
         'visible': True,
         'in_menu': True,
         'parent_id': '201', 'tree_id': '2'},
        {'id': '203', 'slug': 'usa', 'name': 'USA',
         'visible': True,
         'in_menu': True,
         'parent_id': '201', 'tree_id': '2'},

        {'id': '300', 'slug': 'middle-america', 'name': 'Middle-America',
         'visible': True,
         'in_menu': True,
         'parent_id': '200', 'tree_id': '2'},
        {'id': '301', 'slug': 'mexico', 'name': 'Mexico',
         'visible': True,
         'in_menu': True,
         'parent_id': '300', 'tree_id': '2'},
        {'id': '302', 'slug': 'honduras', 'name': 'Honduras',
         'visible': True,
         'in_menu': True,
         'parent_id': '300', 'tree_id': '2'},
        {'id': '303', 'slug': 'guatemala', 'name': 'Guatemala',
         'visible': True,
         'in_menu': True,
         'parent_id': '300', 'tree_id': '2'},

        {'id': '400', 'slug': 'south-america', 'name': 'South-America',
         'visible': True,
         'in_menu': True,
         'parent_id': '200', 'tree_id': '2'},
        {'id': '401', 'slug': 'brazil', 'name': 'Brazil',
         'visible': True,
         'in_menu': True,
         'parent_id': '400', 'tree_id': '2'},
        {'id': '402', 'slug': 'argentina', 'name': 'Argentina',
         'visible': True,
         'in_menu': True,
         'parent_id': '400', 'tree_id': '2'},
        {'id': '403', 'slug': 'uruguay', 'name': 'Uruguay',
         'visible': True,
         'in_menu': True,
         'parent_id': '400', 'tree_id': '2'},
        {'id': '404', 'slug': 'chile', 'name': 'Chile',
         'visible': True,
         'in_menu': True,
         'parent_id': '400', 'tree_id': '2'},

        {'id': '500', 'slug': 'asia', 'name': 'Asia',
         'visible': True,
         'in_menu': True,
         'parent_id': '100', 'tree_id': '2'},
        {'id': '501', 'slug': 'china', 'name': 'China',
         'visible': True,
         'in_menu': True,
         'parent_id': '500', 'tree_id': '2'},
        {'id': '502', 'slug': 'india', 'name': 'India',
         'visible': True,
         'in_menu': True,
         'parent_id': '500', 'tree_id': '2'},
        {'id': '503', 'slug': 'malaysia', 'name': 'Malaysia',
         'visible': True,
         'in_menu': True,
         'parent_id': '500', 'tree_id': '2'},
        {'id': '504', 'slug': 'thailand', 'name': 'Thailand',
         'visible': True,
         'in_menu': True,
         'parent_id': '500', 'tree_id': '2'},
        {'id': '505', 'slug': 'vietnam', 'name': 'Vietnam',
         'visible': True,
         'in_menu': True,
         'parent_id': '500', 'tree_id': '2'},
        {'id': '506', 'slug': 'singapore', 'name': 'Singapore',
         'visible': True,
         'in_menu': True,
         'parent_id': '500', 'tree_id': '2'},
        {'id': '507', 'slug': 'indonesia', 'name': 'Indonesia',
         'visible': True,
         'in_menu': True,
         'parent_id': '500', 'tree_id': '2'},
        {'id': '508', 'slug': 'mongolia', 'name': 'Mongolia',
         'visible': True,
         'in_menu': True,
         'parent_id': '500', 'tree_id': '2'},
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
         'parent_id': '3', 'tree_id': '1'},

        {'id': '5', 'slug': 'hi', 'name': 'Hello',
         'visible': True,
         'in_menu': True,
         'parent_id': None},
        {'id': '6', 'slug': 'bye', 'name': 'Bye',
         'visible': True,
         'in_menu': True,
         'parent_id': None}
    )
    add_fixture(MPTTPages, tree1, session)
    add_fixture(MPTTPages, tree2, session)
    add_fixture(MPTTNews, news, session)


def index_view(request):
    return {}


def add_global_menu(event):
    def page_menu(**kwargs):
        return get_pages_menu(DBSession, MPTTPages, **kwargs)

    def news_menu(**kwargs):
        return get_pages_menu(DBSession, MPTTNews, **kwargs)
    event['page_menu'] = page_menu
    event['news_menu'] = news_menu


def index_page_factory(request):
    settings = request.registry.settings
    models = settings['pyramid_pages.models']
    table = models[''] or models['/']
    dbsession = settings['pyramid_pages.dbsession']
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
    config.add_jinja2_search_path('pyramid_pages_example:templates')

    if settings.get('index_view', False):
        config.add_route('index', '/', factory=index_page_factory)
        config.add_view(index_view,
                        route_name='index',
                        context=PageResource,
                        renderer='index.jinja2')

    # Database
    settings = config.registry.settings
    settings[CONFIG_SQLALCHEMY_URL] =\
        settings.get(CONFIG_SQLALCHEMY_URL,
                     'sqlite:///example.sqlite')
    engine = engine_from_config(settings)
    DBSession.configure(bind=engine)
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        add_mptt_tree(DBSession)
        transaction.commit()
    except Exception as e:
        print(e)

    # pyramid_pages
    config.include("pyramid_pages")
    settings[CONFIG_PYRAMID_PAGES_DBSESSION] =\
        settings.get(CONFIG_PYRAMID_PAGES_DBSESSION,
                     DBSession)
    settings[CONFIG_PYRAMID_PAGES_MODELS] =\
        settings.get(CONFIG_PYRAMID_PAGES_MODELS,
                     {
                         '': MPTTPages,
                         'pages': MPTTPages,
                         'news': MPTTNews
                     })
    config.add_subscriber(add_global_menu, BeforeRender)
    return config.make_wsgi_app()

if __name__ == '__main__':
    settings = {'index_view': True}
    app = main({}, **settings)

    from waitress import serve
    serve(app, host='0.0.0.0', port=6543)
