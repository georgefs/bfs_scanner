#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 lizongzhe 
#
# Distributed under terms of the MIT license.
import re
from bs4 import BeautifulSoup
import bs4
from functools import partial
import urlparse

def compare_selector(element, selector):
    assert " " not in selector, "check_elem_by_selector is not support space"
    assert ">" not in selector, "check_elem_by_selector is not support >"
    assert "|" not in selector, "check_elem_by_selector is not support |"

    # match tagname, id, class, attribute
    pattern = re.compile('^([\w-]+)|#([\w-]+)|\.([\w-]+)|\[([^\]]*)\]')
    assert not re.sub(pattern, "", selector)

    matched = re.findall(pattern, selector)

    for tag_name, tag_id, tag_class, tag_attribute in matched:
        if tag_name and getattr(element, 'name', None) != tag_name:
            return False

        if tag_id and tag_id != getattr(element, 'attrs', {}).get('id', ''):
            return False

        if tag_class and tag_class not in getattr(element, 'attrs', {}).get('class', ''):
            return False

        if tag_attribute:
            attr_pattern = re.compile('^(?P<name>\w+)(?P<opt>[\*\^\$]?=)[\"\']?(?P<val>\w+)[\"\']?')
            info = re.match(attr_pattern, tag_attribute).groupdict()
            
            if info['opt'] == '=':
                target = "^{}$".format(info['val'])
            elif info['opt'] == '*=':
                target = re.compile(".*{}.*".format(info['val']))
            elif info['opt'] == '^=':
                target = re.compile("^{}".format(info['val']))
            elif info['opt'] == '$=':
                target = re.compile("{}$".format(info['val']))
            else:
                raise Exception('attribute operator error {}'.format(attr_pattern))
                
            if not re.search(target, element.attrs.get(info['name'], '')):
                return False
    return True


class Dfs_scaner:
    handlers = []

    class Command:
        next=0
        skip=1

    next_step = Command.next
    url = ""
    merged = False
    
    def __init__(self, element, url="http://localhost", merged=False, first=True):
        """
        Keyword arguments:
            element: target scan element (BeautifulSoup.element.Tag)
            url: base url 
        """
        if isinstance(element, bs4.BeautifulSoup):
            element = element.find()
        self.element = element
        self.url = url
        self.merged = merged
        self.first = first

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
        """
        self.handlers.append([element_matchers, handler, in_after])

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

    def _trigger_handlers(self, element, in_after=False):
        results = []
        for element_matchers, handler, handler_in_after in self.handlers:
            if not isinstance(element_matchers, (list, tuple)):
                element_matchers = [element_matchers]
                
            tmp = []
            for element_matcher in element_matchers:
                if isinstance(element_matcher, basestring):
                    tmp.append(tag_matcher(cssselector=element_matcher))
                elif callable(element_matcher):
                    tmp.append(element_matcher)
                else:
                    raise Exception('matcher is not support')

            element_matchers = tmp

            if in_after == handler_in_after and any([element_matcher(element) for element_matcher in element_matchers]):
                info = {}
                info['element'] = element
                info['handler'] = handler
                info['self'] = self
                info['in_after'] = in_after

                result = handler(info, element)
                if result != None:
                    results.append((info, result))
                if self.first:
                    break
        if self.merged:
            return [results]
        else:
            return results

    def set_next_step(self, command):
        self.next_step = command

    def run(self, element=None):
        element = element or self.element

        for handle_result in self._trigger_handlers(element):
            yield handle_result

        if getattr(element, 'name', None) and self.next_step == Dfs_scaner.Command.next:
            for child in element.childGenerator():
                for i in self.run(child):
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
        result = [r for r in self.run(self.element)]
        return result


# handler creator helper
def skip_handler(matcher):
    # skip childrens
    def extractor(info, element):
        info['self'].set_next_step(Dfs_scaner.Command.skip)
        return None
    extractor.__name__ = u'<function skip_extractor at {}>'.format(id(extractor)).encode('utf-8')
    return (matcher, extractor, False)


def tag_handler(matcher, tagger, in_after=False):
    # tag and continue scan childrens
    def extractor(info, element):
        if isinstance(basestring, tagger):
            result = tagger
        else:
            result = tagger(info, element)
        return result
    return (matcher, extractor, in_after)


def extract_handler(matcher, callback, in_after=False):
    # extract element without scan childrens
    extractor = simple_extractor(callback, Dfs_scaner.Command.skip)
    return (matcher, extractor, in_after)

def simple_img_extract_handler(callback=lambda info, src:src):
    def img_extract(info, elem):
        url = elem.attrs.get('src', None) or elem.attrs.get('data-src', None)
        if url.strip():
            url = urlparse.urljoin(info['self'].url, url.strip())
            result = url
        else:
            result = None
        return callback(info, result)
    return ('img', img_extract, False)

def simple_youtube_extract_handler(callback=lambda info, src:src):
    def youtube_extract(info, elem):
        youtube_url = elem.attrs['src']
        youtube_url = urlparse.urljoin(info['self'].url, youtube_url)
        return callback(info, youtube_url)
    return ('iframe[src*=youtube]', youtube_extract, False)


def text_extract_handler(pattern="", strip=True):
    # bs4.element.NavigableString extractor
    def matcher(element):
        return isinstance(element, bs4.element.NavigableString) and re.match(pattern, unicode(element))
    matcher.__name__ = u'<function text_matcher({}) at {}>'.format(pattern, id(matcher)).encode('utf-8')

    def extractor(info, element):
        result = unicode(element)
        if strip:
            result = result.strip()

        return result or None

    return (matcher, extractor, False)


def text_matcher(pattern, strip=True):
    def matcher(element):
        text = element.text
        if strip:
            text = text.strip()
        return re.match(pattern, text)
    matcher.__name__ = u'<function text_matcher({}) at {}>'.format(pattern, id(matcher)).encode('utf-8')
    return matcher


def tag_matcher(cssselector="", text_pattern=""):
    def matcher(element):
        if getattr(element, "name", None):
            return compare_selector(element, cssselector) and re.match(text_pattern, element.text.strip(), re.M)
        elif cssselector:
            return False
        else:
            return re.match(text_pattern, unicode(element))
    matcher.__name__ = u'<function tag_matcher(cssselector="{}", text_pattern="{}") at {}>'.format(cssselector, text_pattern, id(matcher)).encode('utf-8')
    return matcher


def simple_extractor(callback, step=Dfs_scaner.Command.next):
    def extractor(info, element):
        info['self'].set_next_step(step)
        return callback(info, element) or None
    return extractor



