#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 lizongzhe
#
# Distributed under terms of the MIT license.
import requests
import urlparse
import re


def quick_extractor(callback, skip_childrens=True):
    def wrap(info, elem):
        if skip_childrens:
            info['self'].skip_childrens()
        return callback(info, elem)
    return wrap


skip_extractor = quick_extractor(lambda info, elem: None)


def simple_img_extractor(callback=lambda info, src: src):
    def img_extractor(info, elem):
        if elem.name == 'img':
            img_elem = elem
        else:
            img_elem = elem.select_one('img')

        url = img_elem.attrs.get('src', None) or img_elem.attrs.get('data-src', None)  # noqa
        if url.strip():
            url = urlparse.urljoin(info['self'].url, url.strip())
            result = url
        else:
            result = None
        return callback(info, result)
    return quick_extractor(img_extractor)


def simple_youtube_extractor(callback=lambda info, src: src):
    def youtube_extract(info, elem):
        if elem.name == 'iframe':
            youtube_elem = elem
        else:
            youtube_elem = elem.select_one('iframe[url*=youtube]')

        youtube_url = youtube_elem.attrs['src']
        youtube_url = urlparse.urljoin(info['self'].url, youtube_url)
        return callback(info, youtube_url)
    return quick_extractor(youtube_extract)


def blockquote_imgur_extractor(callback=lambda info, src: src):
    def imgur_extract(info, elem):
        if elem.name == 'blockquote' and 'imgur-embed-pub' in elem.attrs.get('class', []):  # noqa
            imgur_elem = elem
        else:
            imgur_elem = elem.select('blockquote.imgur-embed-pub')
            if not imgur_elem:
                return None
            else:
                imgur_elem = imgur_elem[0]

        imgur_id = imgur_elem.attrs.get('data-id')
        imgur_url = "https://i.imgur.com/{}.jpg".format(imgur_id)
        return callback(info, imgur_url)
    return quick_extractor(imgur_extract)


def blockquote_instagram_extractor(callback=lambda info, src: src):
    def instagram_extract(info, elem):
        if elem.name == 'blockquote' and 'instagram-media' in elem.attrs.get('class', []):  # noqa
            instagram_elem = elem
        else:
            instagram_elem = elem.select('blockquote.instagram-media')
            if not instagram_elem:
                return None
            else:
                instagram_elem = instagram_elem[0]

        page_url = instagram_elem.find('a').attrs.get('href')
        resp = requests.get(page_url)
        instagram_url = re.search('og:image"\s+content="([^"]+)"', resp.text).groups()[0]  # noqa
        return callback(info, instagram_url)
    return quick_extractor(instagram_extract)
