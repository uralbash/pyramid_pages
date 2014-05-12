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
from sacrud.exttype import ChoiceType

Base = declarative_base()

REDIRECT_CHOICES = (
    ('', '200'),
    ('Moved Permanently', '301'),
    ('Moved Temporarily', '302'),
)


class MPTTPages(Base, BaseNestedSets):
    __tablename__ = "mptt_pages"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    description = Column(Text)

    visible = Column(Boolean)

    # Redirection
    redirect_url = Column(String)
    redirect_page = Column(Integer, ForeignKey('mptt_pages.id'))
    redirect_type = Column(ChoiceType(choices=REDIRECT_CHOICES))
    redirect = relationship("MPTTPages", foreign_keys=[redirect_page],
                            remote_side=[id]  # for show in sacrud
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

    @declared_attr
    def sacrud_list_col(cls):
        return [cls.id, cls.level, cls.tree_id,
                cls.parent_id, cls.left, cls.right]

    @declared_attr
    def sacrud_detail_col(cls):
        return [('', [cls.name, cls.slug, cls.description, cls.visible]),
                ('Redirection', [cls.redirect_url, cls.redirect_page,
                                 cls.redirect_type]),
                ('SEO', [cls.seo_title, cls.seo_keywords, cls.seo_description,
                         cls.seo_metatags])
                ]

    def __repr__(self):
        return self.name

    def get_url(self):
        t = self.__class__
        session = Session.object_session(self)
        branch = session.query(t.slug).filter(t.left <= self.left)\
            .filter(t.right >= self.right)\
            .filter(t.tree_id == self.tree_id).order_by(t.left)
        return '/'.join(map(lambda x: x[0], branch))

MPTTPages.register_tree()
