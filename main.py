#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import argparse
from os import path
import sys

from highlite._version import __version__
from highlite.customcorpus import CustomCorpus
from highlite.metrics import ScoreDoc
from highlite.recreate import ReconstructedHTML
from highlite.settings import RAWCORPUS_DIR
from highlite.stats import Summary
from highlite.textio import pdf_to_html, save_html

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="The main executable script for highlite",
        add_help=False
    )

    # arguments for metadata on program
    parser._positionals.title = "Parameters"
    parser._optionals.title = "Optional parameters"
    parser.add_argument("-h", "--help", action="help",
                        default=argparse.SUPPRESS,
                        help="| Show this help message and exit")
    parser.add_argument("-v", "--version", action="version",
                        version="highlite {}".format(__version__),
                        help="| Show program's version and exit")

    # positional arguments
    parser.add_argument("input_doc", metavar="<PATH TO INPUT FILE>",
                        help="| Input document for analysis")

    parser.add_argument("areas", nargs="+", metavar="<LIST OF AREAS>",
                        help="| Disciplines to analyze against")

    # optional arguments
    # options for building corpus
    parser.add_argument("--build", choices=("getresume", "custom"),
                        help="| Method of building corpus")

    parser.add_argument("--anon", action="store_true",
                        help="| Anonymize IP (getresume)")

    parser.add_argument("--pages", default=0, metavar="INT",
                        type=int, help="| Search pages to crawl (getresume)")

    parser.add_argument("--dir", default="sample", metavar="<PATH>",
                        help="| Path of input sample files (custom)")

    parser.add_argument("--input_t", default="pdf", metavar="<TYPE>",
                        help="| Type of input sample files (custom)")

    # options for scoring document
    parser.add_argument("--score", action="store_true",
                        help="| Score input document")

    parser.add_argument("--recreate", action="store_true",
                        help="| Create HTML output of the scored document")

    parser.add_argument("--stats", action="store_true",
                        help="| Create HTML output of the scored document")

    # parse arguments to pass into function
    args = parser.parse_args()

    if args.build == "getresume":

        try:

            from getresume.buildcorpus import ResumeCorpus

            for area in args.areas:
                resume_corpus = ResumeCorpus(
                    area=area,
                    pages=args.pages,
                    anon=bool(args.anon),
                )
                resume_corpus.build()

        except ImportError:
            sys.exit("getresume is not installed, try building a custom corpus")

    elif args.build == "custom" and path.exists(args.dir):

        for area in args.areas:
            resume_corpus = CustomCorpus(
                area=area,
                path_to_dir=args.dir,
                input_type=args.input_t
            )
            resume_corpus.build()

    if args.score:
        obj = ScoreDoc(
            doc_path=args.input_doc,
            areas=args.areas,
            ignore_words=["ana", "ortez", "rivera"],
            corpus_path=RAWCORPUS_DIR,
        )
        obj.generate_tfidf(stop_words="english")
        obj.get_score()

    if args.recreate:
        parsed_html = pdf_to_html(args.input_doc)
        new_doc_obj = ReconstructedHTML(
            results_path="resume_scores.json", parsed_html=parsed_html)

        new_doc_obj.recreate_doc()
        new_doc = new_doc_obj.get_new_html()

        save_html(new_doc)

    if args.stats:

        results_obj = Summary(results_path="resume_scores.json")
        results_obj.get_top_resumes()
        results_obj.get_tfidf()
