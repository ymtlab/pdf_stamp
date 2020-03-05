# -*- coding: utf-8 -*-

class Item(object):
    def __init__(self, parent_item=None, dictionary={}):
        self._dict = dictionary
        self._parent_item = parent_item
        self._children = []

    def child(self, row):
        if row > len(self._children):
            return None
        return self._children[row]

    def child_count(self):
        return len(self._children)

    def children(self):
        return self._children

    def clear(self, column=None):
        if column is None:
            self._dict = {}
            return
        if column in set(self._dict):
            del self._dict[column]

    def data(self, column):
        if column in self._dict:
            return self._dict[column]
        return None

    def insert_children(self, row, count):
        self._children[row:row+count-1] = [ Item(self, {}) for i in range(count) ]

    def parent(self):
        return self._parent_item
        
    def remove_children(self, row, count):
        del self._children[row:row+count]

    def row(self):
        if self._parent_item:
            return self._parent_item._children.index(self)
        return 0

    def set_data(self, column, data):
        self._dict[column] = data

    def set_dict(self, _dict):
        self._dict = _dict

    def to_dict(self):
        return self._dict
