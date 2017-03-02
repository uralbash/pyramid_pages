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
# standard library
import os
import json

# SQLAlchemy
from sqlalchemy import (
    Date,
    Text,
    Column,
    String,
    Integer,
    ForeignKey,
    engine_from_config
)
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.sql import func
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.ext.declarative import declarative_base

# Pyramid
from pyramid.config import Configurator
from pyramid.events import BeforeRender
from pyramid.session import SignedCookieSessionFactory

# third-party
from sqlalchemy_mptt import mptt_sessionmaker
from pyramid_pages.models import FlatPageMixin, MpttPageMixin, RedirectMixin
from pyramid_pages.resources import (
    BasePageResource,
    resource_of_node,
    resources_of_config
)

# third-party
import transaction

Base = declarative_base()
DBSession = scoped_session(
    mptt_sessionmaker(
        sessionmaker(extension=ZopeTransactionExtension())
    )
)

CONFIG_SQLALCHEMY_URL = 'sqlalchemy.url'
CONFIG_PYRAMID_PAGES_MODELS = 'pyramid_pages.models'
CONFIG_PYRAMID_PAGES_DBSESSION = 'pyramid_pages.dbsession'


class BasePage(Base, RedirectMixin):
    __tablename__ = 'base_pages'
    id = Column(Integer, primary_key=True)
    page_type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'base_page',
        'polymorphic_on': page_type,
        'with_polymorphic': '*'
    }

    @classmethod
    def get_pk_name(cls):
        return 'id'

    @classmethod
    def get_pk_with_class_name(cls):
        return 'BasePage.id'


class WebPage(BasePage, MpttPageMixin):
    __tablename__ = 'mptt_pages'

    id = Column(Integer, ForeignKey('base_pages.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'web_page',
    }


class NewsPage(BasePage, FlatPageMixin):
    __tablename__ = 'flat_news'

    id = Column(Integer, ForeignKey('base_pages.id'), primary_key=True)
    date = Column(Date, default=func.now())

    __mapper_args__ = {
        'polymorphic_identity': 'news_page',
    }


class Gallery(BasePage, MpttPageMixin):
    __tablename__ = 'mptt_gallery'

    id = Column(Integer, ForeignKey('base_pages.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'gallery_page',
    }


class Photo(Base):
    __tablename__ = 'photos'

    id = Column('id', Integer, primary_key=True)
    path = Column('path', Text)
    gallery_id = Column(Integer, ForeignKey('mptt_gallery.id'))
    gallery = relationship('Gallery', backref='photos')


class GalleryResource(BasePageResource):
    model = Gallery
    template = 'gallery/index.jinja2'


class NewsResource(BasePageResource):
    model = NewsPage
    template = 'news/index.jinja2'


class Fixtures(object):

    def __init__(self, session):
        self.session = session

    def add(self, model, fixtures):
        here = os.path.dirname(os.path.realpath(__file__))
        file = open(os.path.join(here, fixtures))
        fixtures = json.loads(file.read())
        for fixture in fixtures:
            self.session.add(model(**fixture))
            self.session.flush()
        transaction.commit()


MODELS = {
    '': WebPage,
    'pages': WebPage,
    'news': NewsResource,
    'gallery': GalleryResource,
}


def add_globals(event):

    class Menu(object):
        resources = resources_of_config(MODELS)

        def __init__(self, model):
            self.nodes = DBSession.query(model)
            self.template = 'pyramid_pages/menu/flat.jinja2'
            if hasattr(model, 'parent'):
                self.nodes = self.nodes.filter_by(parent=None)\
                    .order_by(model.tree_id)
                self.template = 'pyramid_pages/menu/mptt.jinja2'

        def __iter__(self):
            for node in self.nodes:
                yield resource_of_node(self.resources, node)(node)

    event['pages_menu'] = Menu(WebPage)
    event['news_menu'] = Menu(NewsPage)
    event['gallery_menu'] = Menu(Gallery)


def main(global_settings, **settings):
    config = Configurator(
        settings=settings,
        session_factory=SignedCookieSessionFactory('itsaseekreet')
    )
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('pyramid_pages_sacrud_example:templates')
    config.add_static_view('pyramid_pages_example_static',
                           'static')

    # Database with ORM SQLAlchemy
    settings = config.get_settings()
    settings[CONFIG_SQLALCHEMY_URL] =\
        settings.get(CONFIG_SQLALCHEMY_URL,
                     'sqlite:///example.sqlite')

    engine = engine_from_config(settings)
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    fixture = Fixtures(DBSession)
    fixture.add(WebPage,  'fixtures/pages.json')
    fixture.add(WebPage,  'fixtures/country.json')
    fixture.add(NewsPage, 'fixtures/news.json')
    fixture.add(Gallery,  'fixtures/gallery.json')
    fixture.add(Photo,    'fixtures/photos.json')

    # pyramid_sacrud - admin interface
    config.include('ps_malchemy')
    settings['pyramid_sacrud.models'] = (
        ('Pages', [WebPage, NewsPage, Gallery, Photo]),
    )
    config.include('pyramid_sacrud', route_prefix='admin')

    # pyramid_pages - tree of website pages stored in database
    settings[CONFIG_PYRAMID_PAGES_DBSESSION] =\
        settings.get(CONFIG_PYRAMID_PAGES_DBSESSION,
                     DBSession)
    settings[CONFIG_PYRAMID_PAGES_MODELS] =\
        settings.get(CONFIG_PYRAMID_PAGES_MODELS, MODELS)
    config.include("pyramid_pages")
    config.add_subscriber(add_globals, BeforeRender)
    return config.make_wsgi_app()


if __name__ == '__main__':
    settings = {}
    app = main({}, **settings)

    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', 6543, app)
    httpd.serve_forever()
