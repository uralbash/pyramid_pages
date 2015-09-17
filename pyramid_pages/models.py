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
from sqlalchemy.ext.declarative import declared_attr

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
    pass


class FlatPageMixin(PageMixin):
    pass


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
            ('', [cls.name, cls.slug, cls.visible, cls.in_menu,
                  cls.description, getattr(cls, 'parent', None)])
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


class BaseSacrudFlatPage(
        SacrudOptions,
        SeoMixin,
        RedirectMixin,
        FlatPageMixin
):
    pass
