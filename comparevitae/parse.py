#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""parse
"""

from __future__ import absolute_import, unicode_literals
import subprocess

from resquest import cleaner
from settings import PARSED_PATH


def pdf_to_text(path):

    path = path
    subprocess.call(["pdftotext", path, PARSED_PATH])

    with open(PARSED_PATH) as parsed_file:
        parsed_text = parsed_file.read()

    obj = cleaner.ContentCleaner(parsed_text)
    return obj.normalize()


if __name__ == '__main__':

    obj = pdf_to_text("../sample/resume.pdf")
