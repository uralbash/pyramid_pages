#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Models for page.
"""
from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String,
                        UnicodeText)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import foreign, relationship
from sqlalchemy.orm.session import Session

from sacrud.common import TableProperty, ClassProperty
from sacrud.exttype import ChoiceType, SlugType
from sqlalchemy_mptt import BaseNestedSets

from .common import Menu

REDIRECT_CHOICES = (
    ('200', 'OK (200)'),
    ('301', 'Moved Permanently (301)'),
    ('302', 'Moved Temporarily (302)'),
)


class PageMixin(object):

    name = Column(String, nullable=False)
    visible = Column(Boolean)
    in_menu = Column(Boolean)
    slug = Column(SlugType('name', False), unique=True, nullable=False)
    description = Column(UnicodeText)

    def __repr__(self):
        return self.name or ''

    def __json__(self, request):
        return self.id


class MpttPageMixin(BaseNestedSets, PageMixin):

    menu_template = 'pyramid_pages/menu/mptt.jinja2'

    def get_menu(self, **kwargs):
        table = self.__class__
        session = Session.object_session(self)
        return Menu(session, table).mptt(**kwargs)


class FlatPageMixin(PageMixin):

    menu_template = 'pyramid_pages/menu/flat.jinja2'

    def get_menu(self):
        table = self.__class__
        session = Session.object_session(self)
        return Menu(session, table).flat()


class RecursionPageMixin(PageMixin):
    """ model with single parent_id field """
    pass


class SeoMixin(object):

    seo_title = Column(String)
    seo_keywords = Column(String)
    seo_description = Column(String)
    seo_metatags = Column(UnicodeText)


class RedirectMixin(object):

    redirect_url = Column(String)
    redirect_type = Column(ChoiceType(choices=REDIRECT_CHOICES))

    @declared_attr
    def redirect_page(cls):
        return Column(
            Integer,
            ForeignKey(
                '{}.{}'.format(cls.__tablename__, cls.get_pk_name()),
                ondelete='CASCADE')
        )

    @declared_attr
    def redirect(cls):
        pk = getattr(cls, cls.get_pk_name())
        return relationship(
            cls, foreign_keys=[cls.redirect_page],
            remote_side='{}.{}'.format(cls.__name__, cls.get_pk_name()),
            primaryjoin=lambda: foreign(cls.redirect_page) == pk,
        )


class BaseSacrudMpttPage(SeoMixin, RedirectMixin, MpttPageMixin):

    # pyramid_sacrud options.
    verbose_name = 'MPTT pages'

    @TableProperty
    def sacrud_css_class(cls):
        col = cls.columns
        return {
            'tinymce': [col.description],
            'description': [col.description],
            'name': [col.name]
        }

    @ClassProperty
    def sacrud_detail_col(cls):
        col = cls.__table__.columns
        return [
            ('', [col.name, col.slug, col.description, col.visible,
                  col.in_menu, cls.parent]),
            ('Redirection', [col.redirect_url, cls.redirect,
                             col.redirect_type]),
            ('SEO', [col.seo_title, col.seo_keywords, col.seo_description,
                     col.seo_metatags])
        ]
