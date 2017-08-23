#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""parse
"""

from __future__ import absolute_import, unicode_literals
import subprocess

from .settings import PARSED_PATH


def pdf_to_text(path):

    subprocess.call(["pdftotext", path, PARSED_PATH])

    with open(PARSED_PATH) as parsed_file:
        parsed_text = (
            line.decode("utf-8").strip() for line in parsed_file.readlines()
        )

    return " ".join(parsed_text)
