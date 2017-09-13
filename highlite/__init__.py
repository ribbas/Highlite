#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from os import getcwd, path

BASE_DIR = getcwd()
with open(path.join(path.dirname(__file__), "basedir")) as custom_dir:
    PROJ_DIR = custom_dir.read() or BASE_DIR


PARSED_PATH = path.join(BASE_DIR, "target_doc.txt")
HTML_CONVERTED_PATH = path.join(BASE_DIR, "target_doc.html")
HTML_CONVERTED_OUT = path.join(BASE_DIR, "target_doc-html.html")
HEATMAP_CSS_PATH = path.join(PROJ_DIR, "ext", "heatmap.css")
BUZZWORDS = path.join(PROJ_DIR, "ext", "buzzwords.json")

RAWCORPUS_DIR = path.join(BASE_DIR, "data", "rawcorpus")
