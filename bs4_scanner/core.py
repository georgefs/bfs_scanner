#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 lizongzhe
#
# Distributed under terms of the MIT license.
import bs4
import matchers


class Dfs_scaner:
    base_handlers = []
    _handlers = []

    class Command:
        next = 0
        skip = 1

    next_step = Command.next
    url = ""
    merged = False

    def __init__(self, elements, url="http://localhost", merged=False, first=True):  # noqa
        """
        Keyword arguments:
            element: target scan element (BeautifulSoup.element.Tag) or [(BeautifulSoup.element.Tag)]
            url: base url
        """  # noqa
        if not isinstance(elements, (list, tuple)):
            elements = [elements]

        _elements = []
        for element in elements:
            if isinstance(element, bs4.BeautifulSoup):
                element = element.find()
            _elements.append(element)

        self.elements = _elements
        self.url = url
        self.merged = merged
        self.first = first
        self._handlers = []

    def add_handler(self, element_matchers, handler, in_after=False):
        """
        新增 element 處理器

        Keyword arguments:
            element_matchers: [element_matcher, element_matcher] or element_matcher
            handler: 符合條件則執行
            in_after: 在掃描離開前才執行 handler


        ## 備註
        ### element_matcher: 基本上會是callback function, 負責判斷目前的element 該不該執行handler
            function(element):
                return bool

            Keyword arguments:
                element: 需判斷的element
            Return:
                bool(判定結果, 符合則回傳True, 不符合則Fa;se)


        ### handler: 基本上會是callback function如下, 負責在掃描element 的時候做相對應的處理
            function(info, element):
                return Dfs_scaner.Command, result

            Keyword arguments:
                info: {}
                element: 當下的element
            Return:
                (Dfs_scaner.Command, handle_result)
        """  # noqa
        self._handlers.append([element_matchers, handler, in_after])

    def add_handlers(self, configures):
        """
        同 add_handler, 不過是批次載入

        Keyword arguments:
            configure: [
                (element_matchers, handler, in_after),
                (element_matchers, handler, in_after),
                ...
            ]
        """
        for element_matchers, handler, in_after in configures:
            self.add_handler(element_matchers, handler, in_after)

    @property
    def handlers(self):
        return self._handlers + self.base_handlers

    def _trigger_handlers(self, element, in_after=False):
        results = []
        for element_matchers, handler, handler_in_after in self.handlers:
            if not isinstance(element_matchers, (list, tuple)):
                element_matchers = [element_matchers]

            tmp = []
            for element_matcher in element_matchers:
                if isinstance(element_matcher, basestring):
                    tmp.append(matchers.tag_matcher(cssselector=element_matcher))  # noqa
                elif callable(element_matcher):
                    tmp.append(element_matcher)
                else:
                    raise Exception('matcher is not support')

            element_matchers = tmp

            if in_after == handler_in_after and any([element_matcher(element) for element_matcher in element_matchers]):  # noqa
                info = {}
                info['element'] = element
                info['handler'] = handler
                info['self'] = self
                info['in_after'] = in_after

                result = handler(info, element)
                if result is not None:
                    results.append((info, result))
                if self.first:
                    break
        if self.merged:
            return [results]
        else:
            return results

    def set_next_step(self, command):
        self.next_step = command

    def skip_childrens(self):
        self.set_next_step(self.Command.skip)

    def scan_multi(self, elements):
        for element in elements:
            for result in self.scan_one(element):
                yield result

    def scan_one(self, element=None):
        element = element or self.element

        for handle_result in self._trigger_handlers(element):
            yield handle_result

        if getattr(element, 'name', None) and self.next_step == Dfs_scaner.Command.next:  # noqa
            for child in element.childGenerator():
                for i in self.scan_one(child):
                    yield i

        elif self.next_step == Dfs_scaner.Command.skip:
            self.next_step = Dfs_scaner.Command.next
            pass

        for handlers_result in self._trigger_handlers(element, True):
            yield handlers_result

    def scan(self):
        """
        開始掃描
        """
        result = [r for r in self.scan_multi(self.elements)]
        return result
