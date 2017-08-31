#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from comparevitae.metrics import RateResume
from comparevitae.recreate import ReconstructedHTML
from comparevitae.textio import pdf_to_html, save_html

if __name__ == "__main__":

    test_resume = "sample/sabbir1.pdf"

    obj = RateResume(
        path=test_resume,
        areas=["data-science", "computer-science"],
        ignore_words=["ana", "ortez", "rivera"],
        anon=False,
    )
    obj.generate_tfidf(stop_words="english")
    obj.get_score()
    x = pdf_to_html(test_resume)
    new_doc_obj = ReconstructedHTML(
        tfidf_scores_path="resume_tfidf.json", parsed_html=x)

    new_doc = new_doc_obj.recreate_doc()
    save_html(new_doc)
