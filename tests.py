#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 lizongzhe
#
# Distributed under terms of the MIT license.
from bs4 import BeautifulSoup
import bs4_scanner
from bs4_scanner import *
import pytest

import requests


@pytest.mark.parametrize(("html", "cssselector", "target"), [
        ("<div id='123' class='456 abc' attr='789'></div>", "div", True),
        ("<div id='123' class='456 abc' attr='789'></div>", "p", False),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#123", True),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#12", False),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#1234", False),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#123.456", True),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#123.45", False),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#123.4567", False),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#123.456[attr=789]", True),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#123.456[attr^=7]", True),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#123.456[attr*=7]", True),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#123.456[attr*=8]", True),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#123.456[attr*=9]", True),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#123.456[attr$=9]", True),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#123.456[attr=7]", False),
        ("<div id='123' class='456 abc' attr='789'></div>", "div#123.456[attr$=7]", False),
    ]
)
def test_cssseletor(html, cssselector, target):
    soup = BeautifulSoup(html)
    elem = soup.find('body').next_element
    assert bs4_scanner.compare_selector(elem, cssselector) == target


def test_parse():
    html = u'''
<div class="text-holder">
   <div class="fb-like" data-href="https://pinknow.nownews.com/2017/10/14/17266" data-width="300px" data-layout="button_count" data-action="like" data-size="large" data-show-faces="false" data-share="true"></div>
   &nbsp;
   <div class="fb-save" data-uri="https://pinknow.nownews.com/2017/10/14/17266" data-size="large"></div>
   <h2 itemprop="headline">
      <header class="entry-header">
         <h1 class="entry-title">多圖／姜河那當兵滿月獻禮　「女友視角」帶妳玩香港</h1>
      </header>
   </h2>
   <span itemprop="description">
      <div class="entry-content">
         <p>南韓演員姜河那出演過無數膾炙人口的電視劇作品，不過他已在9月11日入伍從軍，粉絲們想再看到歐巴出現在螢光幕得等兩年。雖然他入伍前拍的電影《記憶之夜》將於11月底上映，但這仍無法滿足粉絲的心，好在他代言的「旅遊搜尋引擎KAYAK」在姜河那當兵滿一個月的當天釋出驚喜，充滿甜蜜氛圍的「女友視角」影片讓粉絲欣喜不已。<span id="more-17266"></span></p>
         <figure id="attachment_17287" style="width: 2100px" class="wp-caption aligncenter">
            <img class="wp-image-17287 size-full" src="https://i1.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/8-2.jpg?resize=780%2C520&#038;ssl=1" alt="▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）" srcset="https://i1.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/8-2.jpg?w=2100&amp;ssl=1 2100w, https://i1.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/8-2.jpg?resize=800%2C533&amp;ssl=1 800w, https://i1.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/8-2.jpg?resize=1600%2C1067&amp;ssl=1 1600w" sizes="(max-width: 780px) 100vw, 780px" data-recalc-dims="1" />
            <figcaption class="wp-caption-text">▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）</figcaption>
         </figure>
         <p>影片中的姜河那穿梭在香港的知名景點，為粉絲介紹不少遊玩聖地，不論飯店、或是午後遠離城市享受寧靜的片刻時光，以及適合小酌一杯的地點，通通不私藏的介紹給大家，同時也能讓情侶留下美好回憶。</p>
         <div class='code-block code-block-2' style='margin: 8px auto; text-align: center; clear: both;'>
            <center>
            <script type="text/javascript" src="https://cdn.innity.net/admanager.js"></script> <script type="text/javascript">innity_pcu = "%%CLICK_URL_UNESC%%";
               new innity_adZone("5a9d8bf5b7a4b35f3110dde8673bdda2", "64875", {"width": "300", "height": "250"});
            </script>
            <center>
         </div>
         <p>短片中姜河那除了帶螢幕前的觀眾一起走遍香港大街小巷，展示香港多元化的一面，他的「女友視角」模樣更讓不少粉絲尖叫，不管是河那貼心幫你擦嘴巴的畫面，或是不時對鏡頭比出「心心手指」，正好能讓想念姜河那的粉絲們，在螢幕上與他相聚。【記者陳雅蘭／台北報導】</p>
         <p>
            <strong>
               更多旅遊搜尋引擎
               <span lang="EN-US">
                  KAYAK資訊可至→「<em><a href="https://www.tw.kayak.com/">官網</a></em>」、「<em><a href="https://www.tw.kayak.com/news/">網誌</a></em>」、「<a href="https://www.facebook.com/KAYAK.com.Taiwan/"><em>臉書</em></a>」查詢。
         </p>
         <div class='code-block code-block-3' style='margin: 8px auto; text-align: center; clear: both;'><center><script type="text/javascript" src="https://cdn.innity.net/admanager.js"></script> <script type="text/javascript">innity_pcu = "%%CLICK_URL_UNESC%%";
            new innity_adZone("5a9d8bf5b7a4b35f3110dde8673bdda2", "64876", {"width": "300", "height": "250"});
         </script><center></div><p></span></strong></p>
         <p>姜河那「女友視角」影片↓（KAYAK提供）</p>
         <div class="jetpack-video-wrapper"><iframe width="780" height="439" src="https://www.youtube.com/embed/PKepvPWksI8?feature=oembed" frameborder="0" allowfullscreen></iframe></div>
         <figure id="attachment_17291" style="width: 1800px" class="wp-caption aligncenter">
            <img class="wp-image-17291 size-full" src="https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/12-2.jpg?resize=780%2C520&#038;ssl=1" alt="▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）" srcset="https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/12-2.jpg?w=1800&amp;ssl=1 1800w, https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/12-2.jpg?resize=800%2C533&amp;ssl=1 800w, https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/12-2.jpg?resize=1600%2C1067&amp;ssl=1 1600w" sizes="(max-width: 780px) 100vw, 780px" data-recalc-dims="1" />
            <figcaption class="wp-caption-text">▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）</figcaption>
         </figure>
         <figure id="attachment_17290" style="width: 1680px" class="wp-caption aligncenter">
            <img class="wp-image-17290 size-full" src="https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/11-2.jpg?resize=780%2C520&#038;ssl=1" alt="▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）" srcset="https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/11-2.jpg?w=1680&amp;ssl=1 1680w, https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/11-2.jpg?resize=800%2C533&amp;ssl=1 800w, https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/11-2.jpg?resize=1600%2C1067&amp;ssl=1 1600w" sizes="(max-width: 780px) 100vw, 780px" data-recalc-dims="1" />
            <figcaption class="wp-caption-text">▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）</figcaption>
         </figure>
         <figure id="attachment_17289" style="width: 1800px" class="wp-caption aligncenter">
            <img class="wp-image-17289 size-full" src="https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/10-2.jpg?resize=780%2C520&#038;ssl=1" alt="▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）" srcset="https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/10-2.jpg?w=1800&amp;ssl=1 1800w, https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/10-2.jpg?resize=800%2C533&amp;ssl=1 800w, https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/10-2.jpg?resize=1600%2C1067&amp;ssl=1 1600w" sizes="(max-width: 780px) 100vw, 780px" data-recalc-dims="1" />
            <figcaption class="wp-caption-text">▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）</figcaption>
         </figure>
         <figure id="attachment_17285" style="width: 1680px" class="wp-caption aligncenter">
            <img class="wp-image-17285 size-full" src="https://i1.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/6-2.jpg?resize=780%2C520&#038;ssl=1" alt="▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）" srcset="https://i1.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/6-2.jpg?w=1680&amp;ssl=1 1680w, https://i1.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/6-2.jpg?resize=800%2C533&amp;ssl=1 800w, https://i1.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/6-2.jpg?resize=1600%2C1067&amp;ssl=1 1600w" sizes="(max-width: 780px) 100vw, 780px" data-recalc-dims="1" />
            <figcaption class="wp-caption-text">▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）</figcaption>
         </figure>
         <figure id="attachment_17284" style="width: 1687px" class="wp-caption aligncenter">
            <img class="wp-image-17284 size-full" src="https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/5-3.jpg?resize=780%2C520&#038;ssl=1" alt="▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）" srcset="https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/5-3.jpg?w=1687&amp;ssl=1 1687w, https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/5-3.jpg?resize=800%2C533&amp;ssl=1 800w, https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/5-3.jpg?resize=1600%2C1067&amp;ssl=1 1600w" sizes="(max-width: 780px) 100vw, 780px" data-recalc-dims="1" />
            <figcaption class="wp-caption-text">▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）</figcaption>
         </figure>
         <figure id="attachment_17283" style="width: 1526px" class="wp-caption aligncenter">
            <img class="wp-image-17283 size-full" src="https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/4-6.jpg?resize=780%2C521&#038;ssl=1" alt="▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）" srcset="https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/4-6.jpg?w=1526&amp;ssl=1 1526w, https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/4-6.jpg?resize=800%2C535&amp;ssl=1 800w" sizes="(max-width: 780px) 100vw, 780px" data-recalc-dims="1" />
            <figcaption class="wp-caption-text">▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）</figcaption>
         </figure>
         <figure id="attachment_17292" style="width: 1600px" class="wp-caption aligncenter">
            <img class="wp-image-17292 size-full" src="https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/collage2.jpg?resize=780%2C585&#038;ssl=1" alt="▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）" srcset="https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/collage2.jpg?w=1600&amp;ssl=1 1600w, https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/collage2.jpg?resize=200%2C150&amp;ssl=1 200w, https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/collage2.jpg?resize=800%2C600&amp;ssl=1 800w, https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/collage2.jpg?resize=400%2C300&amp;ssl=1 400w" sizes="(max-width: 780px) 100vw, 780px" data-recalc-dims="1" />
            <figcaption class="wp-caption-text">▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）</figcaption>
         </figure>
         <div class='code-block code-block-1' style='margin: 8px auto; text-align: center; clear: both;'>
            <br>
            <div style="border: 6px solid #5ed0cb;padding: .4em 0 0 .4em;color: #000000;">
               <p class="padding: 0 0 0 .4em;color: #000000;">喜歡請幫我們點個讚</p>
               <div class='code-block code-block-4' style='margin: 8px auto; text-align: center; clear: both;'>
                  <center>
                  <script type="text/javascript" src="https://cdn.innity.net/admanager.js"></script> <script type="text/javascript">innity_pcu = "%%CLICK_URL_UNESC%%";
                     new innity_adZone("5a9d8bf5b7a4b35f3110dde8673bdda2", "64877", {"width": "300", "height": "250"});
                  </script>
                  <center>
               </div>
               <div class="fb-page" data-href="https://www.facebook.com/pinknowtw/" data-small-header="false" data-adapt-container-width="true" data-hide-cover="true" data-show-facepile="false">
                  <blockquote cite="https://www.facebook.com/pinknowtw/" class="fb-xfbml-parse-ignore"><a href="https://www.facebook.com/pinknowtw/">粉樂 NOW</a></blockquote>
               </div>
               <br>
            </div>
            <br><br>
         </div>
         <div class="fb-save" data-uri="https://pinknow.nownews.com/2017/10/14/17266" data-size="large"></div>
         <div class="fb-quote"></div>
         &nbsp;
         <div class="fb-like" data-href="https://pinknow.nownews.com/2017/10/14/17266" data-width="300px" data-layout="standard" data-action="recommend" data-size="large" data-show-faces="false" data-share="true"></div>
         <div class="fb-quote"></div>
         <div class="fb-comments" data-href="https://pinknow.nownews.com/2017/10/14/17266" data-numposts="5"></div>
      </div>
   </span>
</div>
    '''
    def format(pattern):
        def wrap(info, r):
            return pattern.format(r)
        return wrap
    soup = BeautifulSoup(html)
    container = soup.select('.text-holder')[0]
    scanner = bs4_scanner.Dfs_scaner(container)
    scanner.add_handlers([
        simple_text_handler(),
        simple_img_handler(format(u"\nimg:{}\n")),
        simple_youtube_handler(format(u"\nyoutube:{}\n")),
        simple_instagram_handler(format(u"\ninstagram:{}\n")),
        simple_imgur_handler(format(u"\nimgur:{}\n")),
        (['script', 'style', '.code-block', tag_matcher('p', u'^更多旅遊搜尋引擎')], skip_extractor, False),
        (['p', 'br'], quick_extractor(lambda info, e: e.text.strip() and u"\n{}\n".format(e.text.strip())), False),
        (['h1', 'h2', 'h3', 'h4'], quick_extractor(lambda into, e: u"<b>{}</b>".format(e.text.strip())), False)
    ])

    results = scanner.scan()
    result = "".join([r[1] for r in results])
    target = u'''
<b>多圖／姜河那當兵滿月獻禮　「女友視角」帶妳玩香港</b>
南韓演員姜河那出演過無數膾炙人口的電視劇作品，不過他已在9月11日入伍從軍，粉絲們想再看到歐巴出現在螢光幕得等兩年。雖然他入伍前拍的電影《記憶之夜》將於11月底上映，但這仍無法滿足粉絲的心，好在他代言的「旅遊搜尋引擎KAYAK」在姜河那當兵滿一個月的當天釋出驚喜，充滿甜蜜氛圍的「女友視角」影片讓粉絲欣喜不已。

img:https://i1.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/8-2.jpg?resize=780%2C520&ssl=1
▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）
影片中的姜河那穿梭在香港的知名景點，為粉絲介紹不少遊玩聖地，不論飯店、或是午後遠離城市享受寧靜的片刻時光，以及適合小酌一杯的地點，通通不私藏的介紹給大家，同時也能讓情侶留下美好回憶。

短片中姜河那除了帶螢幕前的觀眾一起走遍香港大街小巷，展示香港多元化的一面，他的「女友視角」模樣更讓不少粉絲尖叫，不管是河那貼心幫你擦嘴巴的畫面，或是不時對鏡頭比出「心心手指」，正好能讓想念姜河那的粉絲們，在螢幕上與他相聚。【記者陳雅蘭／台北報導】

姜河那「女友視角」影片↓（KAYAK提供）

youtube:https://www.youtube.com/embed/PKepvPWksI8?feature=oembed

img:https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/12-2.jpg?resize=780%2C520&ssl=1
▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）
img:https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/11-2.jpg?resize=780%2C520&ssl=1
▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）
img:https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/10-2.jpg?resize=780%2C520&ssl=1
▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）
img:https://i1.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/6-2.jpg?resize=780%2C520&ssl=1
▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）
img:https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/5-3.jpg?resize=780%2C520&ssl=1
▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）
img:https://i0.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/4-6.jpg?resize=780%2C521&ssl=1
▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）
img:https://i2.wp.com/pinknow.nownews.com/wp-content/uploads/2017/10/collage2.jpg?resize=780%2C585&ssl=1
▲姜河那「女友視角」帶你玩香港。（圖／KAYAK）
    '''.strip()
    assert result == target


def test_empty_tag(): # issue8
    html = "<div><p></p><p>test</p></div>"
    soup = BeautifulSoup(html)
    elem = soup.find('div')
    scanner = bs4_scanner.Dfs_scaner(elem)
    scanner.add_handlers([
        simple_text_handler(),
    ])
    results = scanner.scan()
    assert len(results) == 1
    assert results[0][1] == 'test'

def test_multi_element(): # issue1
    elem1 = BeautifulSoup("<div>page1</div>").find('div')
    elem2 = BeautifulSoup("<div>page2</div>").find('div')
    elem3 = BeautifulSoup("<div>page3</div>").find('div')

    scanner = bs4_scanner.Dfs_scaner([elem1, elem2, elem3])
    scanner.add_handlers([
        simple_text_handler(),
    ])
    results = scanner.scan()
    result = "".join([r[1] for r in results])
    assert len(results) == 3
    assert result == "page1page2page3"
