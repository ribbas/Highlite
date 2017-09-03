#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json
from pprint import pprint

from scipy import stats


class Summary(object):

    def __init__(self, results_path):

        self.results = {}
        with open(results_path) as results_file:
            self.results = json.load(results_file)

    def get_top_resumes(self):

        pprint(self.results["top_resumes"], indent=2)

    def get_tfidf(self):

        tfidf_scores = sorted(
            self.results["tfidf_scores"].items(),
            key=lambda x: x[-1], reverse=True
        )
        pprint(tfidf_scores, indent=2)

    def get_tfidf_summary(self):

        tfidf_stats = stats.describe(self.results["tfidf_scores"].values())

        pprint({
            "min": tfidf_stats.minmax[0],
            "max": tfidf_stats.minmax[-1],
            "mean": tfidf_stats.mean,
            "variance": tfidf_stats.variance,
        })
