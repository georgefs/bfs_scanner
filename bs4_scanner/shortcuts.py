#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 lizongzhe 
#
# Distributed under terms of the MIT license.
from .extractors import (
        simple_img_extractor,
        simple_youtube_extractor,
        blockquote_imgur_extractor,
        blockquote_instagram_extractor,
        quick_extractor,
)

from .matchers import navigablestring_matcher

def mirror(info, result):
    return result

def simple_img_handler(callback=mirror):
    return ("img", simple_img_extractor(callback), False)

def simple_youtube_handler(callback=mirror):
    return ("iframe[src*=youtube]", simple_youtube_extractor(callback), False)

def simple_imgur_handler(callback=mirror):
    return ("blockquote.imgur-embed-pub", blockquote_imgur_extractor(callback), False)

def simple_instagram_handler(callback=mirror):
    return ("blockquote.instagram-media", blockquote_instagram_extractor(callback), False)

def simple_text_handler(callback=mirror):
    return (navigablestring_matcher(), quick_extractor(lambda info, e: callback(info, unicode(e).strip()) or None), False)
