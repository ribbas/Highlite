#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""parse
"""

from __future__ import absolute_import, unicode_literals

import subprocess
from os import path

from .settings import HTML_CONVERTED_OUT, HTML_CONVERTED_PATH, PARSED_PATH


def pdf_to_text(file_path):

    subprocess.call(["pdftotext", file_path, PARSED_PATH])

    with open(PARSED_PATH) as parsed_file:
        parsed_text = (
            line.decode("utf-8").strip() for line in parsed_file.readlines()
        )

    return " ".join(parsed_text)


def pdf_to_html(file_path):

    if not path.exists(HTML_CONVERTED_OUT):
        subprocess.call(
            ["pdftohtml", "-s", "-c", file_path, HTML_CONVERTED_PATH]
        )

    with open(HTML_CONVERTED_OUT) as parsed_file:
        parsed_html = (
            line.decode("utf-8").strip() for line in parsed_file.readlines()
        )

    return parsed_html
