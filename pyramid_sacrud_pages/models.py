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
import deform
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import foreign, relationship
from sqlalchemy.orm.session import Session

from sacrud.common import TableProperty
from sacrud.exttype import ChoiceType, SlugType
from sqlalchemy_mptt import BaseNestedSets

from .common import get_pages_menu

Base = declarative_base()

REDIRECT_CHOICES = (
    ('200', 'OK (200)'),
    ('301', 'Moved Permanently (301)'),
    ('302', 'Moved Temporarily (302)'),
)


class BasePages(BaseNestedSets):

    name = Column(String, nullable=False)
    slug = Column(SlugType('name', False), unique=True, nullable=False,
                  info={"colanderalchemy": {'title': "URL (slug)"},
                        "description":
                        """Example: <br />
                           contacts => http://mysite.com/about/contacts"""})
    description = Column(
        Text,
        info={'colanderalchemy': {
            'title': 'Description',
            'widget': deform.widget.TextAreaWidget(css_class='tinymce')}}
    )

    visible = Column(Boolean)
    in_menu = Column(Boolean)

    # Redirection
    redirect_url = Column(String)
    redirect_type = Column(ChoiceType(choices=REDIRECT_CHOICES))

    @declared_attr
    def redirect_page(cls):
        return Column(Integer, ForeignKey('%s.%s' % (cls.__tablename__,
                                                     cls.get_db_pk()),
                                          ondelete='CASCADE'))

    @declared_attr
    def redirect(cls):
        pk = getattr(cls, cls.get_pk())
        return relationship(
            cls, foreign_keys=[cls.redirect_page],
            info={"colanderalchemy": {'title': "Redirect page"}},
            remote_side=cls.get_class_pk(),  # for show in sacrud relation
            primaryjoin=lambda: foreign(cls.redirect_page) == pk,
        )

    # SEO
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
    seo_description = Column(String, nullable=True,
                             info={"colanderalchemy": {'title': "META Description"},
                                   "description":
                                   """Generate:
                                      &lt;meta name='description'
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
    # SACRUD
    items_per_page = 20
    verbose_name = u'MPTT pages'
    sacrud_list_template = "pyramid_sacrud_pages/tree.jinja2"

    @TableProperty
    def sacrud_css_class(cls):
        col = cls.columns
        return {'tinymce': [col.description],
                'content': [col.description],
                'name': [col.name]}

    def __repr__(self):
        return self.name

    def get_url(self):
        t = self.__class__
        session = Session.object_session(self)
        branch = session.query(t.slug).filter(t.left <= self.left)\
            .filter(t.right >= self.right)\
            .filter(t.tree_id == self.tree_id).order_by(t.left)
        branch = map(lambda x: x[0], branch)
        branch = filter(lambda x: x != '/', branch)
        return '/'.join(branch)

    def get_menu(self, **kwargs):
        t = self.__class__
        session = Session.object_session(self)
        return get_pages_menu(session, t, **kwargs)
