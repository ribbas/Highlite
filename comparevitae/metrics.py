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

    def __init__(self, path, areas, ignore_words=[], pages=1, anon=True,
                 build=False):

        self.ignore_words = ignore_words

        self.corpus = []
        self.train_resumes = []
        self.tfidf_matrix = None
        self.feature_names = None

        for area in areas:

            if build:
                resume_corpus = ResumeCorpus(
                    area=area,
                    pages=pages,
                    anon=anon,
                )
                resume_corpus.build()

            self.train_resumes.extend(getresume_paths.lsfile(
                getresume_paths.RAWCORPUS_DIR, area, "*.txt"))

        for resume_file_path in self.train_resumes:

            with open(resume_file_path) as resume_file:
                self.corpus.append(resume_file.read())

        self.train_resumes = [
            i.replace(getresume_paths.RAWCORPUS_DIR, "")
            for i in self.train_resumes
        ]
        self.resume = [pdf_to_text(path)]

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

    def get_score(self, filename="resume_tfidf", top=5):

        cos_sim = linear_kernel(
            self.tfidf_matrix[:1], self.tfidf_matrix).flatten()[1:]
        top_indicies = cos_sim.argsort()[:-(top + 1):-1]
        resume_names = np.asarray(self.train_resumes)
        feature_index = self.tfidf_matrix[0].nonzero()[1]
        tfidf_scores = zip(
            feature_index, (self.tfidf_matrix[0, i] for i in feature_index)
        )
        tfidf_scores_features = dict(
            (self.feature_names[i], s) for (i, s) in tfidf_scores
        )
        resume_names = list(resume_names[top_indicies])
        resume_names = [
            {
                "index": i,
                "area": j.split("/")[1],
                "url": j.split("/")[-1],
            } for i, j in enumerate(resume_names)
        ]

        data = {
            "top_resumes": resume_names,
            "tfidf_scores": tfidf_scores_features,
        }

        with open(filename + ".json", "w") as out_file:
            json.dump(data, out_file)
