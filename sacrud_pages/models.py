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
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy_mptt import BaseNestedSets
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MPTTPages(Base, BaseNestedSets):
    """ https://bitbucket.org/zzzeek/sqlalchemy/src/73095b353124/examples/nested_sets/nested_sets.py?at=master
    """
    __tablename__ = "mptt_pages2"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(Text)

    visible = Column(Boolean)

    # SACRUD
    items_per_page = 20
    verbose_name = u'MPTT pages'
    sacrud_css_class = {'tinymce': [description],
                        'content': [description],
                        'name': [name], }

    @declared_attr
    def sacrud_list_col(cls):
        return [cls.id, cls.level, cls.tree_id,
                cls.parent_id, cls.left, cls.right]

    def __repr__(self):
        return "MPTTPages(%s, %s, %s)" % (self.id, self.left, self.right)
