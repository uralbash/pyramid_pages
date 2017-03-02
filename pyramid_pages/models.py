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
# SQLAlchemy
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    ForeignKey,
    UnicodeText
)
from sqlalchemy.orm import foreign, relationship
from sqlalchemy.ext.declarative import declared_attr

# third-party
from saexttype import SlugType, ChoiceType
from sqlalchemy_mptt import BaseNestedSets

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
    """
    Model with single parent_id field
    """


class SeoMixin(object):

    seo_title = Column(String)
    seo_keywords = Column(String)
    seo_description = Column(String)
    seo_metatags = Column(UnicodeText)


class RedirectMixin(object):

    redirect_url = Column(String)
    redirect_type = Column(ChoiceType(choices=REDIRECT_CHOICES))

    @declared_attr
    def redirect_page(self):
        return Column(
            Integer,
            ForeignKey(
                '{}.{}'.format(self.__tablename__, self.get_pk_name()),
                ondelete='CASCADE')
        )

    @declared_attr
    def redirect(self):
        pk = getattr(self, self.get_pk_name())
        return relationship(
            self, foreign_keys=[self.redirect_page],
            remote_side='{}.{}'.format(self.__name__, self.get_pk_name()),
            primaryjoin=lambda: foreign(self.redirect_page) == pk,
        )


class SacrudOptions(object):

    pass
    # @ClassProperty
    # def sacrud_detail_col(cls):
    #     options = [
    #         ('', [cls.name, cls.slug, cls.visible, cls.in_menu,
    #               cls.description, getattr(cls, 'parent', None)])
    #     ]
    #     if all(hasattr(cls, name)
    #            for name in ('redirect_url', 'redirect', 'redirect_type')):
    #         options.append(
    #             ('Redirection', [cls.redirect_url, cls.redirect,
    #                              cls.redirect_type])
    #         )
    #     if all(hasattr(cls, name)
    #            for name in ('seo_title', 'seo_keywords', 'seo_description',
    #                         'seo_metatags')):
    #         options.append(
    #             ('SEO', [cls.seo_title, cls.seo_keywords,
    #                      cls.seo_description,
    #                      cls.seo_metatags])
    #         )
    #     return options


class BaseSacrudMpttPage(
        SacrudOptions,
        SeoMixin,
        RedirectMixin,
        MpttPageMixin
):
    """
    Base mptt page class for :mod:`pyramid_sacrud`.
    """


class BaseSacrudFlatPage(
        SacrudOptions,
        SeoMixin,
        RedirectMixin,
        FlatPageMixin
):
    """
    Base flat page class for :mod:`pyramid_sacrud`.
    """
