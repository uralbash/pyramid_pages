#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Model of Pages
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import foreign, relationship
from sqlalchemy.orm.session import Session

from sacrud.exttype import ChoiceType, SlugType
from sqlalchemy_mptt import BaseNestedSets

from .common import get_pages_menu

Base = declarative_base()

REDIRECT_CHOICES = (
    ('', '200'),
    ('Moved Permanently', '301'),
    ('Moved Temporarily', '302'),
)


class BasePages(BaseNestedSets):

    name = Column(String, nullable=False)
    slug = Column(SlugType('string_name', False), nullable=False, unique=True)
    description = Column(Text)

    visible = Column(Boolean)
    in_menu = Column(Boolean)

    # Redirection
    redirect_url = Column(String)
    redirect_type = Column(ChoiceType(choices=REDIRECT_CHOICES))

    @declared_attr
    def redirect_page(cls):
        return Column(Integer, ForeignKey('%s.id' % cls.__tablename__))

    @declared_attr
    def redirect(cls):
        return relationship(cls, foreign_keys=[cls.redirect_page],
                            remote_side=[cls.id],  # for show in sacrud
                            primaryjoin=lambda: foreign(cls.redirect_page) == cls.id,
                            )

    # SEO paty
    seo_title = Column(String, nullable=True)
    seo_keywords = Column(String, nullable=True)
    seo_description = Column(String, nullable=True)
    seo_metatags = Column(Text, nullable=True)

    # SACRUD
    items_per_page = 20
    verbose_name = u'MPTT pages'
    sacrud_list_template = "/sacrud_pages/tree.jinja2"
    sacrud_css_class = {'tinymce': [description],
                        'content': [description],
                        'name': [name], }

    def __repr__(self):
        return self.name

    def get_url(self):
        t = self.__class__
        session = Session.object_session(self)
        branch = session.query(t.slug).filter(t.left <= self.left)\
            .filter(t.right >= self.right)\
            .filter(t.tree_id == self.tree_id).order_by(t.left)
        return '/'.join(map(lambda x: x[0], branch))

    def get_menu(self, **kwargs):
        t = self.__class__
        session = Session.object_session(self)
        return get_pages_menu(session, t, **kwargs)
