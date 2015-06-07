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
import json
import os

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


class MPTTPages(Base, BasePages):
    __tablename__ = "mptt_pages"

    id = Column('id', Integer, primary_key=True)


class MPTTNews(Base, BaseNestedSets, PageMixin):
    __tablename__ = "mptt_news"

    id = Column('id', Integer, primary_key=True)


def add_fixture(model, fixtures, session):
    here = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(here, fixtures))
    fixtures = json.loads(file.read())
    for fixture in fixtures:
        session.add(model(**fixture))


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
        config.add_view(lambda request: {},
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
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    add_fixture(MPTTPages, 'fixtures/pages.json', DBSession)
    add_fixture(MPTTPages, 'fixtures/country.json', DBSession)
    add_fixture(MPTTNews, 'fixtures/news.json', DBSession)
    transaction.commit()

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

    from wsgiref.simple_server import make_server
    httpd = make_server('', 6543, app)
    httpd.serve_forever()
