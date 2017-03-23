#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

PARSED_PATH = "resume.txt"

STOPWORDS = []

with open("corpus/stopwords.txt") as stopwords_file:
    STOPWORDS = stopwords_file.read().split('\n')
