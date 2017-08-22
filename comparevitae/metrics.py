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

    def __init__(self, path, area, username, pages=1, anon=True, build=False):

        self.path = path
        self.area = area
        self.username = username
        self.pages = pages
        self.anon = anon

        self.resume_corpus = ResumeCorpus(
            area=self.area,
            pages=self.pages,
            anon=self.anon,
        )
        if build:
            self.resume_corpus.build()

        self.corpus = []
        self.test_resumes = getresume_paths.lsfile(
            getresume_paths.RAWCORPUS_DIR, self.area, "*.txt")

        for resume_file_path in self.test_resumes:

            with open(resume_file_path) as resume_file:
                self.corpus.append(resume_file.read())

        self.test_resumes = [
            i.replace(getresume_paths.RAWCORPUS_DIR, "")
            for i in self.test_resumes
        ]
        self.resume = pdf_to_text(self.path)
        # self.corpus = [
        #     pdf_to_text("sample/science-tech-resumes2.pdf"),
        #     pdf_to_text("sample/science-tech-resumes3.pdf"),
        #     pdf_to_text("sample/science-tech-resumes4.pdf"),
        #     pdf_to_text("sample/science-tech-resumes5.pdf"),
        #     pdf_to_text("sample/science-tech-resumes6.pdf"),
        #     pdf_to_text("sample/science-tech-resumes7.pdf"),
        #     pdf_to_text("sample/science-tech-resumes8.pdf"),
        #     pdf_to_text("sample/ana.pdf"),
        #     pdf_to_text("sample/sabbir2.pdf"),
        #     pdf_to_text("sample/ana.pdf"),
        #     pdf_to_text("sample/ana.pdf"),
        # ]

    def build(self):

        if self.build:
            self.resume_corpus.build()

    def generate_tfidf(self, max_feats=None, ngram_range=(1, 3),
                       stop_words=None):

        vectorizer = TfidfVectorizer(
            preprocessor=lambda x: normalize_text(x, username=self.username),
            max_features=max_feats,
            ngram_range=ngram_range,
            stop_words="english"
        )

        tfidf = vectorizer.fit_transform([self.resume] + self.corpus)
        cos_sim = linear_kernel(tfidf[:1], tfidf).flatten()[1:]

        # x = np.asarray(self.test_resumes)
        # print(x[cos_sim.argsort()[::-1]][:5])
        # y = np.asarray(self.corpus)
        # print(y[cos_sim.argsort()[::-1]][:5])
        print(cos_sim.argsort()[::-1])
        feats = vectorizer.get_feature_names()

        doc = 17
        feature_index = tfidf[doc, :].nonzero()[1]
        tfidf_scores = zip(
            feature_index, [tfidf[doc, g] for g in feature_index])
        # print(tfidf_scores)

        tfidf_scores = [(feats[i], s) for (i, s) in tfidf_scores]
        for w, s in tfidf_scores:
            print w, s
