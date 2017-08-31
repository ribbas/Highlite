#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from os import getcwd, path

BASE_DIR = getcwd()
PARSED_PATH = path.join(BASE_DIR, "resume.txt")
HTML_CONVERTED_PATH = path.join(BASE_DIR, "resume.html")
HTML_CONVERTED_OUT = path.join(BASE_DIR, "resume-html.html")
HEATMAP_CSS_PATH = path.join(BASE_DIR, "static", "heatmap.css")
