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

    def get_top_docs(self):

        print("\x1b[1;34;40mTop closest documents:\x1b[0m")
        pprint(self.results["top_resumes"], indent=2)

    def get_top_tfidf(self):

        top_tfidf_scores = list(set(self.results["tfidf_scores"].values()))
        top_tfidf_scores.sort()
        top_tfidf_scores = top_tfidf_scores[:-6:-1]

        top_tfidf_terms = self.results["tfidf_scores"].items()
        top_tfidf_terms = [
            i for i in top_tfidf_terms if i[-1] in top_tfidf_scores]
        top_tfidf_terms.sort(key=lambda x: x[-1])

        print("\x1b[1;34;40mTop TF-IDF scored terms:\x1b[0m")
        pprint(top_tfidf_terms[::-1], indent=2)

    def get_tfidf_summary(self):

        tfidf_stats = stats.describe(self.results["tfidf_scores"].values())

        print("\x1b[1;34;40mTF-IDF scores summary statistics:\x1b[0m")
        pprint({
            "min": tfidf_stats.minmax[0],
            "max": tfidf_stats.minmax[-1],
            "mean": tfidf_stats.mean,
            "variance": tfidf_stats.variance,
        })

    def get_buzzwords(self):

        buzzwords = self.results["buzzwords"].values()
        buzzwords_summary = {i: buzzwords.count(i) for i in buzzwords}

        print("\x1b[1;34;40mBuzzwords frequency statistics:\x1b[0m")
        pprint(buzzwords_summary, indent=2)
