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
import deform
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
    slug = Column(
        SlugType('name', False), unique=True, nullable=False,
        info={"colanderalchemy": {'title': "URL (slug)"},
              "description":
              """Example: <br />
              contacts => http://mysite.com/about/contacts"""})

    def __repr__(self):
        return self.name or '<{}>'.format(self)

    def get_menu(self, **kwargs):
        table = self.__class__
        session = Session.object_session(self)
        return get_pages_menu(session, table, **kwargs)


class SeoMixin(object):

    seo_title = Column(String, nullable=True,
                       info={"colanderalchemy": {'title': "Title"},
                             "description":
                             "Generate: &lt;title&gt;Value&lt;/title&gt;"})
    seo_keywords = Column(String, nullable=True,
                          info={"colanderalchemy": {'title': "META Keywords"},
                                "description":
                                """Generate:
                                  &lt;meta name=''keywords''
                                  content=/"Value/" /&gt;"""})
    seo_description = Column(
        String, nullable=True,
        info={"colanderalchemy": {'title': "META Description"},
              "description": """Generate: &lt;meta name='description'
                                content='Value' /&gt;"""})
    seo_metatags = Column(
        Text, nullable=True,
        info={'colanderalchemy': {'title': 'META Tags',
                                  'widget': deform.widget.TextAreaWidget()},
              "description":
              """Example: <br />
              &lt;meta name='robots' content='Allow'/&gt;
              <br />&lt;meta property='og:image'
              content='http://mysite.com/logo.png'
              /&gt;"""})


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
            info={"colanderalchemy": {'title': "Redirect page"}},
            remote_side=cls.get_class_pk(),  # for show in sacrud relation
            primaryjoin=lambda: foreign(cls.redirect_page) == pk,
        )


class BasePages(BaseNestedSets, PageMixin, SeoMixin, RedirectMixin):

    description = Column(
        Text,
        info={'colanderalchemy': {
            'title': 'Description',
            'widget': deform.widget.TextAreaWidget(css_class='tinymce')}}
    )

    # sacrud
    verbose_name = 'MPTT pages'

    @TableProperty
    def sacrud_css_class(cls):
        col = cls.columns
        return {'tinymce': [col.description],
                'content': [col.description],
                'name': [col.name]}
