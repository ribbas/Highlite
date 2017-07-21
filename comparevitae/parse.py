#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""parse
"""

from __future__ import absolute_import, unicode_literals
import subprocess

# from getresume import cleaner
from .settings import PARSED_PATH
from .textfilters import normalize_text


def pdf_to_text(path):

    subprocess.call(["pdftotext", path, PARSED_PATH])

    with open(PARSED_PATH) as parsed_file:
        parsed_text = (
            line.decode('utf-8').strip() for line in parsed_file.readlines()
        )

    # obj = cleaner.ContentCleaner(parsed_text)
    return normalize_text(' '.join(parsed_text))


if __name__ == '__main__':

    obj = pdf_to_text("../sample/resume.pdf")
