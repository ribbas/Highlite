#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json

from getresume.buildcorpus import ResumeCorpus
from getresume.settings import paths as getresume_paths
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from .textio import pdf_to_text
from .textutil import normalize_text


class RateResume(object):

    def __init__(self, path, areas, ignore_words, pages=1, anon=True,
                 build=False):

        self.path = path
        self.areas = areas
        self.ignore_words = ignore_words
        self.pages = pages
        self.anon = anon

        self.corpus = []
        self.test_resumes = []
        self.tfidf_matrix = None
        self.feature_names = None

        for area in self.areas:

            if build:
                self.resume_corpus = ResumeCorpus(
                    area=area,
                    pages=self.pages,
                    anon=self.anon,
                )
                self.resume_corpus.build()

            self.test_resumes.extend(getresume_paths.lsfile(
                getresume_paths.RAWCORPUS_DIR, area, "*.txt"))

        for resume_file_path in self.test_resumes:

            with open(resume_file_path) as resume_file:
                self.corpus.append(resume_file.read())

        self.test_resumes = [
            i.replace(getresume_paths.RAWCORPUS_DIR, "")
            for i in self.test_resumes
        ]
        self.resume = [pdf_to_text(self.path)]

    def build(self):

        if self.build:
            self.resume_corpus.build()

    def generate_tfidf(self, max_feats=None, ngram_range=(1, 3),
                       stop_words=None):

        tfidf = TfidfVectorizer(
            preprocessor=lambda x: normalize_text(
                x, ignore_words=self.ignore_words),
            max_features=max_feats,
            ngram_range=ngram_range,
            stop_words=stop_words,
        )

        self.tfidf_matrix = tfidf.fit_transform(self.resume + self.corpus)
        self.feature_names = tfidf.get_feature_names()

    def get_score(self, filename="resume_tfidf", top_indicies=5):

        cos_sim = linear_kernel(
            self.tfidf_matrix[:1], self.tfidf_matrix).flatten()[1:]
        self.top_indicies = cos_sim.argsort()[:-(top_indicies + 1):-1]
        resume_names = np.asarray(self.test_resumes)
        feature_index = self.tfidf_matrix[0].nonzero()[1]
        tfidf_scores = zip(
            feature_index, (self.tfidf_matrix[0, i] for i in feature_index)
        )
        tfidf_scores_features = (
            (self.feature_names[i], s) for (i, s) in tfidf_scores
        )

        data = {
            "top_resumes": list(resume_names[self.top_indicies]),
            "tfidf_scores": dict(tfidf_scores_features),
        }

        with open(filename + ".json", "w") as out_file:
            json.dump(data, out_file)
