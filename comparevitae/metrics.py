#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from getresume.buildcorpus import ResumeCorpus
from getresume.settings import paths as getresume_paths
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from .textio import pdf_to_text
from .textutil import normalize_text


class RateResume(object):

    def __init__(self, path, areas, proper_nouns, pages=1, anon=True,
                 build=False):

        self.path = path
        self.areas = areas
        self.corpus = []
        self.test_resumes = []
        self.proper_nouns = proper_nouns
        self.pages = pages
        self.anon = anon

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
                x, proper_nouns=self.proper_nouns),
            max_features=max_feats,
            ngram_range=ngram_range,
            stop_words=stop_words,
        )

        tfidf_matrix = tfidf.fit_transform(self.resume + self.corpus)
        cos_sim = linear_kernel(tfidf_matrix[:1], tfidf_matrix).flatten()[1:]

        x = np.asarray(self.test_resumes)
        print(x[cos_sim.argsort()[::-1]][0])
        y = np.asarray(self.corpus)
        print(y[cos_sim.argsort()[::-1]][0])
        print(cos_sim[cos_sim.argsort()[::-1]].shape)
        feats = tfidf.get_feature_names()

        feature_index = tfidf_matrix[0, :].nonzero()[1]
        tfidf_scores = zip(
            feature_index, (tfidf_matrix[0, i] for i in feature_index))

        tfidf_scores = ((feats[i], s) for (i, s) in tfidf_scores)
        for w, s in tfidf_scores:
            print w, s
