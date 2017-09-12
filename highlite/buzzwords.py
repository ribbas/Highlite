#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json
import re
import urllib2

from bs4 import BeautifulSoup

from . import BUZZWORDS
from .textutil import normalize_text

regex = re.compile("[[(/]|( -)")
url = "https://en.wikipedia.org/wiki/List_of_buzzwords"


def generate_buzzwords():

    response = urllib2.urlopen(url).read()

    soup = BeautifulSoup(response, "html.parser")

    categories = soup.find_all("div", {"class", "div-col"})
    headers = soup.find_all("h2")
    headers = (i.find_all("span", {"class": "mw-headline"}) for i in headers)
    extras = ("Other", "See also", "References", "External links")
    headers = [
        normalize_text(i[0].text) for i in headers
        if i and i[0].text not in extras
    ]

    buzzwords = {i: [] for i in headers}

    for category, header in zip(categories, headers):
        unordered_li = category.find_all("li")
        for li in unordered_li:
            li = regex.split(li.text)[0]
            if len(li) < 50:
                buzzwords[header].append(normalize_text(li))

    with open(BUZZWORDS, "w") as out_file:
        json.dump(buzzwords, out_file)
