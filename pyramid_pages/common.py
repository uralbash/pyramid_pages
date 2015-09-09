#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
"""
Menu generator
"""
from collections import OrderedDict


class PageMenu(object):

    def __init__(self, items, template):
        self.items = items
        self.template = template

    def __iter__(self):
        for item in self.items:
            yield item


def sort_by_left(tree):
    """ Sort dict by left and tree_id field
    """
    return OrderedDict(sorted(tree.items(),
                              key=lambda x: (x[0].left, x[0].tree_id)))


def recursive_node_to_dict(node, menu, json=None, json_fields=None):
    result = {}
    children = {}
    if node in menu:
        result = {node: {}}
    for item in node.children:
        children.update(recursive_node_to_dict(item, menu))
    if node in menu:
        result[node] = sort_by_left(children)
    return result


class Menu(object):

    def __init__(self, session, model, home=False):
        self.model = model
        self.template = self.model.menu_template
        self.items = session.query(model).filter_by(visible=True)\
            .filter_by(in_menu=True)
        if not home:
            self.items = self.items.filter(model.slug != '/')

    def flat(self):
        return PageMenu(self.items, self.template)

    def mptt(self, from_lvl=1, **kwargs):
        menu = self.items.filter(self.model.level >= from_lvl)
        if 'to_lvl' in kwargs:
            to_lvl = int(kwargs['to_lvl'])
            if to_lvl > 0:
                menu = menu.filter(self.model.level <= to_lvl)
            elif to_lvl < 0:
                from sqlalchemy import func
                menu = menu.filter(
                    self.model.level <=
                    func.max(self.model.level + to_lvl).select()
                )
        if 'trees' in kwargs:
            menu = menu.filter(self.model.tree_id.in_(kwargs['trees']))
        if not menu.all():
            return PageMenu((), self.template)

        tree = {}
        min_lvl = min(menu, key=lambda item: item.level).level
        top_nodes = filter(lambda item: item.level == min_lvl, menu)
        for item in top_nodes:
            tree.update(recursive_node_to_dict(item, menu))

        return PageMenu(sort_by_left(tree).items(), self.template)
