#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from context import resquest
from parse import pdf_to_text
from resquest import buildcorpus


class RateResume:

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

        self.glob_bow = self.resume_corpus.get_data(data="bow")
        self.bow = pdf_to_text(self.path)
        self.intersection = (set(self.bow.keys()) & set(self.glob_bow.keys()))

    def build(self):

        if self.build:
            self.resume_corpus.build()

    def get_glob_bow(self):

        return self.glob_bow

    def get_bow(self):

        return self.bow

    def get_intersection(self):

        return self.intersection

    def rate(self):

        ratios = {}
        local_total = 0
        global_total = 0

        for word in self.intersection:

            # if word in self.bow.keys():
            ratios[word] = {
                "local": self.bow[word],
                "global": self.glob_bow[word]
            }
            local_total += self.bow[word]
            global_total += self.glob_bow[word]

        print(local_total, global_total)
        return ratios


if __name__ == '__main__':

    from pprint import pprint

    obj = RateResume(path="../sample/resume.pdf", area="Data Science")
    pprint(obj.rate())
