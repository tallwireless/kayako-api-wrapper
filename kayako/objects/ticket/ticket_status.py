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
    "TicketStatus",
]


class TicketStatus(KayakoObject):
    """
    Kayako TicketStatus API Object.

    id                    ID of the ticket status
    title                 The title of the departmen.
    type                  The accessibility level of the department ('public' or 'private').
    displayorder          A positive integer that the helpdesk will use to sort departments when displaying them (ascending).
    statuscolor
    """

    controller = "/Tickets/TicketStatus"

    __parameters__ = ["id", "title", "type", "displayorder", "statuscolor"]

    __required_add_parameters__ = ["title", "type"]
    __add_parameters__ = ["title", "type", "displayorder", "statuscolor"]

    __required_save_parameters__ = ["title"]
    __save_parameters__ = ["title", "type", "displayorder", "statuscolor"]

    @classmethod
    def _parse_ticketstatus(cls, ticketstatus_tree):

        params = dict(
            id=cls._get_int(ticketstatus_tree.find("id")),
            title=cls._get_string(ticketstatus_tree.find("title")),
            type=cls._get_string(ticketstatus_tree.find("type")),
            displayorder=cls._get_int(ticketstatus_tree.find("displayorder")),
            statuscolor=cls._get_string(ticketstatus_tree.find("statuscolor")),
        )
        return params

    def _update_from_response(self, ticketstatus_tree):

        for int_node in ["id", "displayorder"]:
            node = ticketstatus_tree.find(int_node)
            if node is not None:
                setattr(self, int_node, self._get_int(node, required=False))

        for str_node in ["title", "type", "statuscolor"]:
            node = ticketstatus_tree.find(str_node)
            if node is not None:
                setattr(self, str_node, self._get_string(node))

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, "GET")
        tree = etree.fromstring(response.data)
        print(tree)
        return [
            TicketStatus(api, **cls._parse_ticketstatus(ticketstatus_tree))
            for ticketstatus_tree in tree.findall("ticketstatus")
        ]

    @classmethod
    def get(cls, api, id):
        response = api._request("%s/%s/" % (cls.controller, id), "GET")
        tree = etree.fromstring(response.data)
        node = tree.find("ticketstatus")
        if node is None:
            return None
        params = cls._parse_ticketstatus(node)
        return TicketStatus(api, **params)

    def add(self):
        response = self._add(self.controller)
        tree = etree.fromstring(response.data)
        node = tree.find("ticketstatus")
        self._update_from_response(node)

    def save(self):
        response = self._save("%s/%s/" % (self.controller, self.id))
        tree = etree.fromstring(response.data)
        node = tree.find("ticketstatus")
        self._update_from_response(node)

    def delete(self):
        self._delete("%s/%s/" % (self.controller, self.id))

    def __str__(self):
        return "<TicketStatus (%s): %s>" % (self.id, self.title)
