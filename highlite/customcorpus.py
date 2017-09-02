#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from os import makedirs, path

from .settings import RAWCORPUS_DIR
from .textio import lsfile, pdf_to_text


class CustomCorpus(object):

    def __init__(self, area, path_to_dir, input_type="pdf"):

        self.area = area
        self.corpus_path = path.join(RAWCORPUS_DIR, self.area)
        self.path_to_dir = path_to_dir
        self.input_type = input_type

        if not path.exists(self.corpus_path):
            makedirs(self.corpus_path)

    def build(self):

        print("Building custom corpus \'%s\'..." % self.area)
        input_file_paths = lsfile(self.path_to_dir, "*." + self.input_type)

        if self.input_type == "pdf":
            for input_file_path in input_file_paths:
                pdf_to_text(
                    file_path=input_file_path,
                    parsed_path=path.join(
                        self.corpus_path,
                        "txt".join(
                            path.basename(input_file_path).rsplit("pdf", 1)
                        )
                    )
                )

        print("'%s' corpus built\n" % self.area)
