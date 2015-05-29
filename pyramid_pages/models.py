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
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import foreign, relationship
from sqlalchemy.orm.session import Session

from sacrud.common import TableProperty
from sacrud.exttype import ChoiceType, SlugType
from sqlalchemy_mptt import BaseNestedSets

from .common import get_pages_menu

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

    def __repr__(self):
        return self.name or '<{}>'.format(self)

    def get_menu(self, **kwargs):
        table = self.__class__
        session = Session.object_session(self)
        return get_pages_menu(session, table, **kwargs)


class SeoMixin(object):

    seo_title = Column(String)
    seo_keywords = Column(String)
    seo_description = Column(String)
    seo_metatags = Column(Text)


class RedirectMixin(object):

    redirect_url = Column(String)
    redirect_type = Column(ChoiceType(choices=REDIRECT_CHOICES))

    @declared_attr
    def redirect_page(cls):
        return Column(
            Integer,
            ForeignKey('{}.{}'.format(cls.__tablename__, cls.get_db_pk()),
                       ondelete='CASCADE')
        )

    @declared_attr
    def redirect(cls):
        pk = getattr(cls, cls.get_pk())
        return relationship(
            cls, foreign_keys=[cls.redirect_page],
            remote_side=cls.get_class_pk(),  # for show in sacrud relation
            primaryjoin=lambda: foreign(cls.redirect_page) == pk,
        )


class BasePages(BaseNestedSets, PageMixin, SeoMixin, RedirectMixin):

    description = Column(Text)

    # sacrud
    verbose_name = 'MPTT pages'

    @TableProperty
    def sacrud_css_class(cls):
        col = cls.columns
        return {'tinymce': [col.description],
                'content': [col.description],
                'name': [col.name]}
