#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from os import makedirs, path

from .settings import RAWCORPUS_DIR
from .textio import lsfile, pdf_to_text


class CustomCorpus(object):

    def __init__(self, area, path_to_dir, input_type="pdf"):

        self.area = area
        self.path_to_dir = path_to_dir
        self.input_type = input_type

        if not path.exists(path.join(RAWCORPUS_DIR, self.area)):
            makedirs(path.join(RAWCORPUS_DIR, self.area))

    def build(self):

        print("Building custom corpus \"{}\"...".format(self.area))
        input_file_paths = lsfile(self.path_to_dir, "*." + self.input_type)

        for input_file_path in input_file_paths:
            pdf_to_text(
                input_file_path,
                parsed_path=path.join(
                    RAWCORPUS_DIR,
                    self.area,
                    path.basename(input_file_path).replace(
                        self.input_type, "txt")
                )
            )
