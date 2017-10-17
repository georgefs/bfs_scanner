#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 lizongzhe
#
# Distributed under terms of the MIT license.

from .core import Dfs_scaner
from .matchers import navigablestring_matcher, tag_matcher, compare_selector
from .extractors import (
        quick_extractor,
        simple_img_extractor, 
        simple_youtube_extractor,
        blockquote_imgur_extractor, 
        blockquote_instagram_extractor, 
        skip_extractor,
)

from .shortcuts import (
    simple_img_handler,
    simple_youtube_handler,
    simple_imgur_handler,
    simple_instagram_handler,
    simple_text_handler,
)
