#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-import

from __future__ import absolute_import, print_function, unicode_literals

from os import getcwd, path
import sys

with open(path.join(
    path.dirname(path.dirname(__file__)), "highlite", "basedir"
), "w") as custom_dir:
    custom_dir.write(unicode(path.dirname(getcwd())))

MODULE_PATH = path.join(path.dirname(path.abspath(path.dirname(__file__))))
sys.path.append(MODULE_PATH)

from highlite import BASE_DIR, RAWCORPUS_DIR
from highlite import customcorpus, metrics, recreate, textio

CORPUS_LABEL = "test_corpus"
SAMPLE_DIR = path.join(BASE_DIR, "sample")
TARGET_DOC = path.join(SAMPLE_DIR, "target", "science-tech-resumes1.pdf")
TEST_DOCS = path.join(SAMPLE_DIR, "test_docs")
RESULTS_PATH = path.join(TARGET_DOC.replace("pdf", "json"))


# def test_build():
#     """Build a custom corpus"""

#     resume_corpus = customcorpus.CustomCorpus(
#         corpus=CORPUS_LABEL,
#         path_to_dir=TEST_DOCS,
#     )
#     resume_corpus.build()

#     assert(textio.lsfile(RAWCORPUS_DIR, CORPUS_LABEL, "*.txt"))


def test_score():
    """Score target document"""

    metrics_obj = metrics.ScoreDoc(
        doc_path=TARGET_DOC,
        corpora=[CORPUS_LABEL],
        corpus_path=RAWCORPUS_DIR,
    )
    metrics_obj.generate_tfidf()
    metrics_obj.get_score(RESULTS_PATH)


def test_recreate():
    """Generate the tagged HTML document of the report"""

    parsed_html = textio.pdf_to_html(TARGET_DOC)
    new_doc_obj = recreate.ReconstructedHTML(
        results_path=RESULTS_PATH, parsed_html=parsed_html
    )

    new_doc_obj.recreate_doc()
    new_doc = new_doc_obj.get_new_html()

    textio.save_html(new_doc)
