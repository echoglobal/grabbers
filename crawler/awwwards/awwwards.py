# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os

from grab import Grab


def crawler(*urls):
    """
    This function browses the site for the purpose of web spidering
    """

    page = 3
    for url in urls:
        g = Grab(log_file='out.html')
        g.go(url)
        category = os.path.basename(url)
        print category + ": "
        companies = g.doc.select('//ul[@class="list-items list-flex"]').text()
        print companies

        # TODO: It is'nt done
        # while True:
        #     next_page = str(url) + '?page='+ str(page) + '&scroll=true'
        #     n = Grab()
        #     n.go(next_page)
        #     companies = n.doc.select('//ul[@class="list-items list-flex"]').text()
        #     print companies
        #     page += 1


crawler('http://www.awwwards.com/directory/search/app-development',
        'http://www.awwwards.com/directory/search/art-direction',
        'http://www.awwwards.com/directory/search/graphic-design',
        'http://www.awwwards.com/directory/search/interactive',
        'http://www.awwwards.com/directory/search/other',
        'http://www.awwwards.com/directory/search/seo-sem',
        'http://www.awwwards.com/directory/search/social-media',
        'http://www.awwwards.com/directory/search/ux-ui',
        'http://www.awwwards.com/directory/search/web-design',
        'http://www.awwwards.com/directory/search/web-development')
