#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from string import punctuation

from dateutil import parser as date_parser
from nltk.stem import WordNetLemmatizer

lemma = WordNetLemmatizer()


def normalize_text(content):

    norm_text = content.encode("ascii", "ignore").lower()

    for white_space in u"\n\r":
        norm_text = norm_text.replace(white_space, " ")

    words = norm_text.split()
    words = (word for word in words if (not word.isdigit() and len(word) > 2))
    words = [lemma.lemmatize(x) for x in words]

    for i, word in enumerate(words):
        if any(p in word for p in ('(', ')')):
            words[i] = word[word.find("(") + 1:word.find(")")]

        if words[i][-1] in punctuation and words[i][-2] not in punctuation:
            words[i] = word.replace(word[-1], '')

    time_filtered = []

    for word in words:
        try:
            if date_parser.parse(word):
                pass

        except (TypeError, ValueError):
            time_filtered.append(word)

    return ' '.join(time_filtered)
