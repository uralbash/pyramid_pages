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
from wsgiref.simple_server import make_server

import transaction
from pyramid.config import Configurator
from pyramid.response import Response
from sqlalchemy import Column, engine_from_config, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from sacrud.common import TableProperty
from pyramid_sacrud_pages.models import BasePages

Base = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class MPTTPages(BasePages, Base):
    __tablename__ = "mptt_pages"

    id = Column('id', Integer, primary_key=True)

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
    transaction.commit()
    tree1 = (
        {'id': '1', 'slug': 'about-company', 'name': 'About company', 'visible': True, 'parent_id': None},
        {'id': '2', 'slug': 'we-love-gevent', 'name': u'We ♥ gevent', 'visible': True, 'parent_id': '1'},
        {'id': '3', 'slug': 'and-pyramid', 'name': 'And Pyramid', 'visible': True, 'parent_id': '2'},
        {'id': '4', 'slug': 'our-history', 'name': 'Our history', 'visible': False, 'parent_id': '1'},
        {'id': '5', 'slug': 'foo', 'name': 'foo', 'visible': True, 'parent_id': '4'},
        {'id': '6', 'slug': 'kompania-itcase', 'name': u'компания ITCase', 'visible': False, 'parent_id': '4'},
        {'id': '7', 'slug': 'our-strategy', 'name': 'Our strategy', 'visible': True, 'parent_id': '1'},
        {'id': '8', 'slug': 'wordwide', 'name': 'Wordwide', 'visible': True, 'parent_id': '7'},
        {'id': '9', 'slug': 'technology', 'name': 'Technology', 'visible': False, 'parent_id': '8'},
        {'id': '10', 'slug': 'what-we-do', 'name': 'What we do', 'visible': True, 'parent_id': '7'},
        {'id': '11', 'slug': 'at-a-glance', 'name': 'at a glance', 'visible': True, 'parent_id': '10'},
    )

    tree2 = (
        {'id': '12', 'slug': 'foo12', 'name': 'foo12', 'visible': True, 'parent_id': None, 'tree_id': '2'},
        {'id': '13', 'slug': 'foo13', 'name': 'foo13', 'visible': False, 'parent_id': '12', 'tree_id': '2'},
        {'id': '14', 'slug': 'foo14', 'name': 'foo14', 'visible': False, 'parent_id': '13', 'tree_id': '2'},
        {'id': '15', 'slug': 'foo15', 'name': 'foo15', 'visible': True, 'parent_id': '12', 'tree_id': '2'},
        {'id': '16', 'slug': 'foo16', 'name': 'foo16', 'visible': True, 'parent_id': '15', 'tree_id': '2'},
        {'id': '17', 'slug': 'foo17', 'name': 'foo17', 'visible': True, 'parent_id': '15', 'tree_id': '2'},
        {'id': '18', 'slug': 'foo18', 'name': 'foo18', 'visible': True, 'parent_id': '12', 'tree_id': '2'},
        {'id': '19', 'slug': 'foo19', 'name': 'foo19', 'visible': True, 'parent_id': '18', 'tree_id': '2'},
        {'id': '20', 'slug': 'foo20', 'name': 'foo20', 'visible': True, 'parent_id': '19', 'tree_id': '2'},
        {'id': '21', 'slug': 'foo21', 'name': 'foo21', 'visible': True, 'parent_id': '18', 'tree_id': '2'},
        {'id': '22', 'slug': 'foo22', 'name': 'foo22', 'visible': True, 'parent_id': '21', 'tree_id': '2'},
    )
    add_fixture(MPTTPages, tree1, session)
    add_fixture(MPTTPages, tree2, session)


def hello_world(request):
    return Response('<a href="/admin/">Admin</a><br />' +
                    '<br /><a href="about-company">About company page</a>')


def get_app():
    config = Configurator()
    settings = config.registry.settings
    settings['sqlalchemy.url'] = "sqlite:///example.sqlite"

    config.add_route('hello', '/')
    config.add_view(hello_world, route_name='hello')
    # Database
    engine = engine_from_config(settings)
    DBSession.configure(bind=engine)
    try:
        MPTTPages.__table__.create(engine)
        add_mptt_tree(DBSession)
        transaction.commit()
    except Exception as e:
        print e

    # SACRUD
    settings['pyramid_sacrud.models'] = {'': {'tables': [MPTTPages],
                                              'column': 1,
                                              'position': 1}, }
    config.include('pyramid_sacrud', route_prefix='/admin')

    # sacrud_pages - put it after all routes
    settings['pyramid_sacrud_pages.model_locations'] = MPTTPages  # or 'app:MPTTPages'
    config.include("pyramid_sacrud_pages")
    return config.make_wsgi_app()

if __name__ == '__main__':
    app = get_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
