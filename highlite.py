#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import argparse
from os import path
from pprint import pprint

from highlite import _version, buzzwords, customcorpus, metrics, recreate, \
    settings, stats, textio

if __name__ == "__main__":

    class CapitalisedHelpFormatter(argparse.HelpFormatter):
        def add_usage(self, usage, actions, groups):
            return super(CapitalisedHelpFormatter, self).add_usage(
                usage, actions, groups, "Usage: ")

    parser = argparse.ArgumentParser(
        formatter_class=CapitalisedHelpFormatter,
        description="The main executable script for Highlite",
        add_help=False
    )

    # arguments for metadata on program
    parser._positionals.title = "Positional parameters"
    parser._optionals.title = "Optional parameters"
    parser.add_argument("-h", "--help", action="help",
                        default=argparse.SUPPRESS,
                        help="| Show this help message and exit")
    parser.add_argument("-v", "--version", action="version",
                        version="Highlite {}".format(
                            _version.__version__),
                        help="| Show version and exit")

    # positional arguments
    parser.add_argument("input_doc", metavar="<PATH TO INPUT FILE>", nargs="?",
                        help="| Input document for analysis")

    # options for building corpus
    parser.add_argument("--build", choices=("getresume", "custom"),
                        help="| Method of building corpus")

    parser.add_argument("--corpus", nargs="*", metavar="LABEL",
                        help="| Labels of corpora to analyze against")

    parser.add_argument("--anon", action="store_true",
                        help="| Anonymize IP (getresume)")

    parser.add_argument("--pages", default=0, metavar="N",
                        type=int, help="| Search pages to crawl (getresume)")

    parser.add_argument(
        "--dir_input", default="", metavar="PATH",
        help="| Path of input files to be converted into the corpus (custom)")

    parser.add_argument("--input_t", default="pdf", metavar="TYPE",
                        help="| Type of input sample files (custom)")

    # options for scoring document
    parser.add_argument("--score", action="store_true",
                        help="| Score input document")

    parser.add_argument("--ignore_terms", nargs="+", metavar="TERM",
                        help="| List of words to ignore in scoring document")

    parser.add_argument(
        "--max_feats", default=None, metavar="N", type=int,
        help="| Maximum number of features for the TF-IDF vectorizer"
    )

    parser.add_argument(
        "--ngram_range", default=(1, 3), metavar="N", nargs=2,
        help="| n-grams range for the TF-IDF vectorizer"
    )

    parser.add_argument("--use_stop_words", action="store_true",
                        help="| Stopwords for the TF-IDF vectorizer")

    parser.add_argument("--recreate", action="store_true",
                        help="| Create HTML output of the scored document")

    parser.add_argument(
        "--stats", default=None,
        choices=("closest_docs", "top_tfidf_terms", "tfidf_summary",
                 "buzzwords"), metavar="OPT",
        nargs="*", help="| Get summary of resume analysis"
    )

    parser.add_argument(
        "--preview", action="store_true",
        help="| Opens up the tagged document of the browser for preview"
    )

    # extra options
    parser.add_argument("--buzzwords", action="store_true",
                        help="| Update buzzwords corpus")

    parser.add_argument(
        "--get_corpus_dir", action="store_true",
        help="| Get the location of the directory of the generated corpus"
    )

    # parse arguments to pass into function
    args = parser.parse_args()
    results_path = "resume_scores.json"

    print("\x1b[1;31;40mParameters chosen:\x1b[0m")
    pprint(args.__dict__, indent=2)
    print()

    if args.build == "getresume":

        if not(args.corpus):
            argparse.ArgumentError(
                "Corpus label not specified for building corpus")

        try:

            from getresume.buildcorpus import ResumeCorpus

            for corpus in args.corpus:
                resume_corpus = ResumeCorpus(
                    area=corpus,
                    pages=args.pages,
                    anon=bool(args.anon),
                )
                resume_corpus.build()

        except ImportError:
            raise ImportError(
                "getresume is not installed, try building a custom corpus")

    elif args.build == "custom" and path.exists(args.dir):

        if not(args.corpus):
            argparse.ArgumentError(
                "Corpus label not specified for building corpus")

        for corpus in args.corpus:
            resume_corpus = customcorpus.CustomCorpus(
                area=corpus,
                path_to_dir=args.dir,
                input_type=args.input_t
            )
            resume_corpus.build()

    if args.score:

        if not(args.corpus):
            raise argparse.ArgumentError(
                args.corpus, "Corpus label not specified for document analysis"
            )

        metrics_obj = metrics.ScoreDoc(
            doc_path=args.input_doc,
            corpora=args.corpus,
            ignore_terms=args.ignore_terms,
            corpus_path=settings.RAWCORPUS_DIR,
        )
        metrics_obj.generate_tfidf(
            max_feats=args.max_feats,
            ngram_range=args.ngram_range,
            stop_words="english" if args.use_stop_words else None,
        )
        metrics_obj.get_score()

    if args.recreate:

        if not path.exists(results_path):
            raise IOError("Document has not been processed yet.")

        parsed_html = textio.pdf_to_html(args.input_doc)
        new_doc_obj = recreate.ReconstructedHTML(
            results_path=results_path, parsed_html=parsed_html
        )

        new_doc_obj.recreate_doc()
        new_doc = new_doc_obj.get_new_html()

        textio.save_html(new_doc)

    if args.stats is not None:

        results_path = "resume_scores.json"
        if not path.exists(results_path):
            raise IOError("Document has not been processed yet.")

        results_obj = stats.Summary(results_path=results_path)

        if args.stats == [] or "closest_docs" in args.stats:
            results_obj.get_top_docs()

        if args.stats == [] or "top_tfidf_terms" in args.stats:
            results_obj.get_top_tfidf()

        if args.stats == [] or "tfidf_summary" in args.stats:
            results_obj.get_tfidf_summary()

        if args.stats == [] or "buzzwords" in args.stats:
            results_obj.get_buzzwords()

    if args.buzzwords:

        buzzwords.generate_buzzwords()

    if args.preview:

        import webbrowser
        webbrowser.get().open(settings.HTML_CONVERTED_PATH)

    if args.get_corpus_dir:

        print(
            "Location of generated corpus: \x1b[1;31;40m%s\x1b[0m"
            % settings.RAWCORPUS_DIR
        )
