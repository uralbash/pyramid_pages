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
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session

from sqlalchemy_mptt import BaseNestedSets
from sacrud.exttype import ChoiceType, SlugType

Base = declarative_base()

REDIRECT_CHOICES = (
    ('', '200'),
    ('Moved Permanently', '301'),
    ('Moved Temporarily', '302'),
)


class ClassProperty(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, inst, cls):
        return self.func(cls.__table__)


class BasePages(BaseNestedSets):

    name = Column(String, nullable=False)
    slug = Column(SlugType('string_name', False), nullable=False, unique=True)
    description = Column(Text)

    visible = Column(Boolean)

    # Redirection
    redirect_url = Column(String)
    redirect_type = Column(ChoiceType(choices=REDIRECT_CHOICES))

    @declared_attr
    def redirect_page(cls):
        return Column(Integer, ForeignKey('mptt_pages.id'))

    #@declared_attr
    #def redirect(cls):
        #return relationship("MPTTPages", foreign_keys=[cls.redirect_page],
                            #remote_side=[cls.id]  # for show in sacrud
                            #)

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


class MPTTPages(BasePages, Base):
    __tablename__ = "mptt_pages"

    id = Column(Integer, primary_key=True)

    @ClassProperty
    def sacrud_list_col(cls):
        col = cls.columns
        return [col.name, col.level, col.tree_id,
                col.parent_id, col.left, col.right]

    @ClassProperty
    def sacrud_detail_col(cls):
        col = cls.columns
        return [('', [col.name, col.slug, col.description, col.visible]),
                ('Redirection', [col.redirect_url, col.redirect_page,
                                 col.redirect_type]),
                ('SEO', [col.seo_title, col.seo_keywords, col.seo_description,
                         col.seo_metatags])
                ]

MPTTPages.register_tree()
