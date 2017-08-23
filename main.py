#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from comparevitae.metrics import RateResume
from comparevitae.textutil import recreate_doc

if __name__ == "__main__":

    obj = RateResume(
        path="sample/sabbir2.pdf",
        areas=["data-science", "computer-science"],
        ignore_words=["sabbir", "ahmed", "baltimore", "maryland"],
        anon=False,
    )
    obj.generate_tfidf(stop_words="english")
    obj.get_score()
    # recreate_doc(tfidf_scores_path="resume_tfidf.json")
