#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from string import punctuation

from dateutil import parser as date_parser
from nltk.stem import WordNetLemmatizer

lemma = WordNetLemmatizer()


def normalize_text(content):

    norm_text = content.lower().encode("ascii", "ignore")

    for white_space in u"\n\r":
        norm_text = norm_text.replace(white_space, " ")

    for p in punctuation:
        norm_text = norm_text.replace(p, "")

    words = filter(lambda x: x.strip() != "", norm_text.split(" "))
    words = filter(lambda x: not x.isdigit() and len(x) > 3, words)
    words = [lemma.lemmatize(x) for x in words]
    # words = [re.sub(digit_pat, "", x) for x in words]

    time_filtered = []

    for word in words:
        try:
            if date_parser.parse(word):
                pass

        except (TypeError, ValueError):
            time_filtered.append(word)

    return time_filtered
