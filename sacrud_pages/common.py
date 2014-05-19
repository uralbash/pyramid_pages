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


def get_pages_menu(session, model, from_lvl=1, **kwargs):
    menu = session.query(model).filter_by(visible=True)\
        .filter(model.level >= from_lvl)
    if 'to_lvl' in kwargs:
        menu = menu.filter(model.level <= kwargs['to_lvl'])
    if 'trees' in kwargs:
        menu = menu.filter(model.tree_id.in_(kwargs['trees']))
    menu = menu.filter_by(in_menu=True).all()
    if not menu:
        return {}

    tree = {}
    min_lvl = min(menu, key=lambda item: item.level).level
    top_nodes = filter(lambda item: item.level == min_lvl, menu)
    for item in top_nodes:
        tree.update(recursive_node_to_dict(item, menu))

    return sort_by_left(tree)
