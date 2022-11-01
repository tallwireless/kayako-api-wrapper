# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
# -----------------------------------------------------------------------------
"""
Created on May 5, 2011

@author: evan
"""

from lxml import etree

from kayako.core.object import KayakoObject

__all__ = [
    "TicketPriority",
]


class TicketPriority(KayakoObject):
    """
    Kayako ticketpriority API Object.

    id                    ID of the ticket status
    title                 The title of the departmen.
    """

    controller = "/Tickets/TicketPriority"

    __parameters__ = ["id", "title", "type"]

    __required_add_parameters__ = ["title", "type"]
    __add_parameters__ = ["title", "type"]

    __required_save_parameters__ = ["title"]
    __save_parameters__ = ["title", "type"]

    @classmethod
    def _parse_ticketpriority(cls, ticketpriority_tree):

        params = dict(
            id=cls._get_int(ticketpriority_tree.find("id")),
            title=cls._get_string(ticketpriority_tree.find("title")),
            type=cls._get_string(ticketpriority_tree.find("type")),
        )
        return params

    def _update_from_response(self, ticketpriority_tree):

        for int_node in ["id"]:
            node = ticketpriority_tree.find(int_node)
            if node is not None:
                setattr(self, int_node, self._get_int(node, required=False))

        for str_node in ["title", "type"]:
            node = ticketpriority_tree.find(str_node)
            if node is not None:
                setattr(self, str_node, self._get_string(node))

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, "GET")
        tree = etree.fromstring(response.data)
        print(tree)
        return [
            TicketPriority(api, **cls._parse_ticketpriority(ticketpriority_tree))
            for ticketpriority_tree in tree.findall("ticketpriority")
        ]

    @classmethod
    def get(cls, api, id):
        response = api._request("%s/%s/" % (cls.controller, id), "GET")
        tree = etree.fromstring(response.data)
        node = tree.find("ticketpriority")
        if node is None:
            return None
        params = cls._parse_ticketpriority(node)
        return TicketPriority(api, **params)

    def add(self):
        response = self._add(self.controller)
        tree = etree.fromstring(response.data)
        node = tree.find("ticketpriority")
        self._update_from_response(node)

    def save(self):
        response = self._save("%s/%s/" % (self.controller, self.id))
        tree = etree.fromstring(response.data)
        node = tree.find("ticketpriority")
        self._update_from_response(node)

    def delete(self):
        self._delete("%s/%s/" % (self.controller, self.id))

    def __str__(self):
        return "<TicketPriority (%s): %s>" % (self.id, self.title)
