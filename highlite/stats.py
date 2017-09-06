#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import json
from pprint import pprint

from scipy import stats


class Summary(object):

    def __init__(self, results_path):

        self.results = {}
        with open(results_path) as results_file:
            self.results = json.load(results_file)

    def get_top_resumes(self):

        print("\x1b[1;34;40mTop resumes:\x1b[0m")
        pprint(self.results["top_resumes"], indent=2)

    def get_tfidf(self):

        tfidf_scores = sorted(
            self.results["tfidf_scores"].items(),
            key=lambda x: x[-1], reverse=True
        )

        top_tfidf_scores = tfidf_scores[:5]

        print("\x1b[1;34;40mTop TF-IDF scored terms:\x1b[0m")
        pprint(top_tfidf_scores, indent=2)

    def get_buzzwords(self):

        buzzwords = self.results["buzzwords"].values()
        buzzwords_summary = {i: buzzwords.count(i) for i in buzzwords}

        print("\x1b[1;34;40mBuzzwords frequency statistics:\x1b[0m")
        pprint(buzzwords_summary, indent=2)

    def get_tfidf_summary(self):

        tfidf_stats = stats.describe(self.results["tfidf_scores"].values())

        print("\x1b[1;34;40mTF-IDF scores summary statistics:\x1b[0m")
        pprint({
            "min": tfidf_stats.minmax[0],
            "max": tfidf_stats.minmax[-1],
            "mean": tfidf_stats.mean,
            "variance": tfidf_stats.variance,
        })
