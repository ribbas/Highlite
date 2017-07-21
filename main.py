#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from comparevitae.parse import pdf_to_text

if __name__ == '__main__':

    print(pdf_to_text("sample/resume.pdf"))
