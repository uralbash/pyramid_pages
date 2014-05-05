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
from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from sqlalchemy_mptt import BaseNestedSets

Base = declarative_base()


class MPTTPages(Base, BaseNestedSets):
    __tablename__ = "mptt_pages"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    description = Column(Text)

    visible = Column(Boolean)

    # SACRUD
    items_per_page = 20
    verbose_name = u'MPTT pages'
    sacrud_list_template = "/sacrud_pages/base.jinja2"
    sacrud_css_class = {'tinymce': [description],
                        'content': [description],
                        'name': [name], }

    @declared_attr
    def sacrud_list_col(cls):
        return [cls.id, cls.level, cls.tree_id,
                cls.parent_id, cls.left, cls.right]

    def __repr__(self):
        return "MPTTPages(%s, %s, %s, %s) %s" % (self.id, self.left, self.right,
                                                 self.tree_id, self.name)

MPTTPages.register_tree()
