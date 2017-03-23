#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from context import resquest
from parse import pdf_to_text
from resquest import buildcorpus


class Rate:

    def __init__(self, path, area, pages=[], anon=True, build=False):

        self.path = path
        self.area = area
        self.pages = pages
        self.anon = anon
        self.build = build
        self.resume_corpus = buildcorpus.ResumeCorpus(
            area=self.area,
            pages=self.pages,
            anon=self.anon
        )

    def build(self):

        if self.build:
            self.resume_corpus.build()

    def get_bow(self):

        print(self.resume_corpus.get_data(data="bow"))


if __name__ == '__main__':

    obj = Rate(path="", area="Computer Science")
    obj.get_bow()
