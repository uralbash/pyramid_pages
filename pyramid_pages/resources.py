#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Base pages resources.
"""
import re

from pyramid.threadlocal import get_current_registry

from . import CONFIG_MODELS, CONFIG_DBSESSION
from .views import PageView


class BasePageResource(object):

    """ Base resource tree class for pages.

    :view: view of resource.
    :attr: The view machinery defaults to using the ``__call__`` method of the
        view callable (or the function itself, if the view callable is a
        function) to obtain a response. The attr value allows you to vary the
        method attribute used to obtain the response. For example, if your view
        was a class, and the class has a method named index and you wanted to
        use this method instead of the class's ``__call__`` method to return
        the response, you'd say attr="index" in the view configuration for the
        view. This is most useful when the view definition is a class.
    :template: template for view of resource.
    """

    view = PageView
    attr = 'page_with_redirect'
    template = 'pyramid_pages/index.jinja2'

    def __init__(self,
                 node, prefix=None, request=None, parent=None,
                 *args, **kwargs):
        """ Make resource of node for traversal URL dispatch.

        :node: instance of page
        :pages_config: config for pyramid_pages from your app
        :resources: list of all resources in config
        :prefix: URL prefix for current node
        :parent: if exist it assignet to ``__parent__`` attribute
        """
        self.settings = get_current_registry().settings
        self.node = node
        self.dbsession = self.settings[CONFIG_DBSESSION]
        self.pages_config = self.settings[CONFIG_MODELS]
        self.resources = resources_of_config(self.pages_config)
        self.prefix = prefix or self.get_prefix()
        self.parent = parent

    def get_prefix(self):
        """ Each resource defined in config for pages as dict. This method
        returns key from config where located current resource.
        """
        for key, value in self.pages_config.items():
            if not hasattr(value, '__iter__'):
                value = (value, )
            for item in value:
                if type(self.node) == item\
                        or type(self.node) == getattr(item, 'model', None):
                    return key

    def resource_of_node(self, node, parent=None):
        return resource_of_node(self.resources, node)(
            node, parent=parent or self.parent)

    @property
    def __name__(self):
        """ Returns ``slug`` attribute of node or ``prefix``.
        """
        if self.node and not self.node.slug == '/':
            return self.node.slug
        elif self.node and self.node.slug == '/':
            return ''
        elif self.prefix:
            return self.prefix
        return None

    @property
    def name(self):
        return self.node.name

    @property
    def __parent__(self):
        if self.parent:
            return self.parent
        elif hasattr(self.node, 'parent'):
            parent = self.node.parent
            return resource_of_node(self.resources, parent)(parent)
        elif self.node:
            return self.__class__(None)
        return None

    def __getitem__(self, name):
        for child in self.children:
            if child.slug == name:
                return self.resource_of_node(child.node)

    @property
    def slug(self):
        return getattr(self.node, 'slug', None)

    @property
    def children(self):
        for child in self.node.children:
            yield self.resource_of_node(child)

    @property
    def children_qty(self):
        return len([child for child in self.children
                    if child.node.visible and child.node.in_menu])

    def __resource_url__(self, request, info):
        """ Some hook for prefix and duplication root slash.
        """
        separator = '/{}'.format(self.prefix) if self.prefix else ''
        # XXX: I feel a dissonance here
        info['virtual_path'] = re.sub('/+', '/', info['virtual_path'])
        return info['app_url'] + separator + info['virtual_path']

    def __repr__(self):
        return self.name


def resource_of_node(resources, node):
    """ Returns resource of node.
    """
    for resource in resources:
        model = getattr(resource, 'model', None)
        if type(node) == model:
            return resource
    return BasePageResource


def resources_of_config(config):
    """ Returns all resources and models from config.
    """
    return set(             # unique values
        sum([               # join lists to flat list
            list(value)     # if value is iter (ex: list of resources)
            if hasattr(value, '__iter__')
            else [value, ]  # if value is not iter (ex: model or resource)
            for value in config.values()
        ], [])
    )


def models_of_config(config):
    """ Return list of models from all resources in config.
    """
    resources = resources_of_config(config)
    models = []
    for resource in resources:
        if not hasattr(resource, '__table__') and hasattr(resource, 'model'):
            models.append(resource.model)
        else:
            models.append(resource)
    return models
