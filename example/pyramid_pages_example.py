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
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import Column, Integer, engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from pyramid_pages.common import Menu
from pyramid_pages.models import BasePage, MpttPageMixin, FlatPageMixin

Base = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

CONFIG_SQLALCHEMY_URL = 'sqlalchemy.url'
CONFIG_PYRAMID_PAGES_MODELS = 'pyramid_pages.models'
CONFIG_PYRAMID_PAGES_DBSESSION = 'pyramid_pages.dbsession'


class WebPage(Base, BasePage, MpttPageMixin):
    __tablename__ = "mptt_pages"

    id = Column('id', Integer, primary_key=True)


class NewsPage(Base, FlatPageMixin):
    __tablename__ = "flat_news"

    id = Column('id', Integer, primary_key=True)


def add_fixture(model, fixtures, session):
    here = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(here, fixtures))
    fixtures = json.loads(file.read())
    for fixture in fixtures:
        session.add(model(**fixture))


def add_global_menu(event):
    event['page_menu'] = Menu(DBSession, WebPage).mptt
    event['news_menu'] = Menu(DBSession, NewsPage).flat


def main(global_settings, **settings):
    config = Configurator(
        settings=settings,
        session_factory=SignedCookieSessionFactory('itsaseekreet')
    )
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('pyramid_pages_example:templates')

    # Database
    settings = config.registry.settings
    settings[CONFIG_SQLALCHEMY_URL] =\
        settings.get(CONFIG_SQLALCHEMY_URL,
                     'sqlite:///example.sqlite')
    engine = engine_from_config(settings)
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    add_fixture(WebPage, 'fixtures/pages.json', DBSession)
    add_fixture(WebPage, 'fixtures/country.json', DBSession)
    add_fixture(NewsPage, 'fixtures/news.json', DBSession)
    transaction.commit()

    # pyramid_pages
    config.include("pyramid_pages")
    settings[CONFIG_PYRAMID_PAGES_DBSESSION] =\
        settings.get(CONFIG_PYRAMID_PAGES_DBSESSION,
                     DBSession)
    settings[CONFIG_PYRAMID_PAGES_MODELS] =\
        settings.get(
            CONFIG_PYRAMID_PAGES_MODELS,
            {
                '': WebPage,
                'pages': WebPage,
                'news': NewsPage
            })
    config.add_subscriber(add_global_menu, BeforeRender)
    return config.make_wsgi_app()

if __name__ == '__main__':
    settings = {}
    app = main({}, **settings)

    from wsgiref.simple_server import make_server
    httpd = make_server('', 6543, app)
    httpd.serve_forever()
