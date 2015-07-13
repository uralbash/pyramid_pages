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
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    ForeignKey,
    UnicodeText
)
from sacrud.common import ClassProperty
from sacrud.exttype import SlugType, ChoiceType
from sqlalchemy.orm import foreign, relationship
from sqlalchemy_mptt import BaseNestedSets
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declared_attr

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


class SacrudOptions(object):

    @ClassProperty
    def sacrud_detail_col(cls):
        options = [
            ('', [cls.name, cls.slug, cls.description, cls.visible,
                  cls.in_menu, getattr(cls, 'parent', None)])
        ]
        if all(hasattr(cls, name)
               for name in ('redirect_url', 'redirect', 'redirect_type')):
            options.append(
                ('Redirection', [cls.redirect_url, cls.redirect,
                                 cls.redirect_type])
            )
        if all(hasattr(cls, name)
               for name in ('seo_title', 'seo_keywords', 'seo_description',
                            'seo_metatags')):
            options.append(
                ('SEO', [cls.seo_title, cls.seo_keywords, cls.seo_description,
                         cls.seo_metatags])
            )
        return options


class BaseSacrudMpttPage(
        SacrudOptions,
        SeoMixin,
        RedirectMixin,
        MpttPageMixin
):
    pass
