#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 lizongzhe
#
# Distributed under terms of the MIT license.
import re
import bs4


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

        if tag_class and tag_class not in getattr(element, 'attrs', {}).get('class', ''):  # noqa
            return False

        if tag_attribute:
            attr_pattern = re.compile('^(?P<name>\w+)(?P<opt>[\*\^\$]?=)[\"\']?(?P<val>\w+)[\"\']?')  # noqa
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
                raise Exception('attribute operator error {}'.format(attr_pattern))  # noqa

            if not re.search(target, element.attrs.get(info['name'], '')):
                return False
    return True


def navigablestring_matcher(pattern=""):
    def matcher(element):
        return isinstance(element, bs4.element.NavigableString) and re.search(pattern, unicode(element), re.M)  # noqa
    matcher.__name__ = u'<function text_matcher({}) at {}>'.format(pattern, id(matcher)).encode('utf-8')  # noqa
    return matcher


def tag_matcher(cssselector="", text_pattern="", strip=True):
    def matcher(element):
        if getattr(element, "name", None):
            text = element.text
            if strip:
                text = text.strip()

            return compare_selector(element, cssselector) and re.search(text_pattern, text, re.M)  # noqa
        elif cssselector:
            return False
        else:
            text = unicode(element)
            if strip:
                text = text.strip()
            return re.search(text_pattern, text, re.M)
    matcher.__name__ = u'<function tag_matcher(cssselector="{}", text_pattern="{}") at {}>'.format(cssselector, text_pattern, id(matcher)).encode('utf-8')  # noqa
    return matcher
