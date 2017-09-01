#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json
import re

from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer
import numpy as np

from .settings import HEATMAP_CSS_PATH
from .textutil import normalize_text


class ReconstructedHTML(object):

    def __init__(self, tfidf_scores_path, parsed_html):

        tfidf_scores = {}
        with open(tfidf_scores_path) as tfidf_scores_file:
            tfidf_scores = json.load(tfidf_scores_file)

        self.tfidf_terms = tfidf_scores["tfidf_scores"]

        scores = np.unique(self.tfidf_terms.values())
        self.percentiles = [np.percentile(scores, 20 * i) for i in xrange(1, 5)]

        parsed_html = " ".join(parsed_html).replace("&#160;", " ")
        self.parsed_soup = BeautifulSoup(parsed_html, "html.parser")
        extra_css = self.parsed_soup.new_tag("style", type="text/css")
        with open(HEATMAP_CSS_PATH) as css_file:
            extra_css.string = unicode(css_file.read())
        self.parsed_soup.head.append(extra_css)
        self.stemmer = PorterStemmer()

        self.new_span_format = "<span class=\"{score}\">{text}</span>"
        self.new_html = ""

    def __span_class(self, score):

        if score <= self.percentiles[0]:
            return "first"
        elif score <= self.percentiles[1]:
            return "second"
        elif score <= self.percentiles[2]:
            return "third"
        elif score <= self.percentiles[3]:
            return "fourth"
        else:
            return "fifth"

    def __find_index(self, word, normalized_sent, sentence, score):

        if len(sentence) == len(normalized_sent):
            start = normalized_sent.find(word)
            end = start + len(word)
            return sentence.replace(
                sentence[start:end],
                self.new_span_format.format(
                    score=self.__span_class(score),
                    text=sentence[start:end]
                )
            )

        re_str = word.replace(" ", ".*") + "([.-]|[^\s]+|[^\s]*?)"
        regex = re.compile(re_str, re.I)
        matches = regex.search(sentence)

        try:
            return sentence.replace(
                matches.group(),
                self.new_span_format.format(
                    score=self.__span_class(score),
                    text=matches.group()
                )
            )
        except AttributeError:
            try:
                re_str = " ".join(
                    self.stemmer.stem(i) for i in word.split()
                ).replace(" ", ".*") + "([.-]|[^\s]+|[^\s]*?)"
                regex = re.compile(re_str, re.I)
                matches = regex.search(sentence)
                return sentence.replace(
                    matches.group(),
                    self.new_span_format.format(
                        score=self.__span_class(score),
                        text=matches.group()
                    )
                )

            except AttributeError:
                print "failed \x1b[3;31;40m" + re_str + "\x1b[0m"

    @staticmethod
    def __merge_strings(final_str, version):

        soup = BeautifulSoup(final_str, "html.parser")

        for fixed_span in soup.find_all("span"):
            if not fixed_span.text == version.text:
                return final_str.replace(
                    version.text, unicode(version)
                )

        return final_str

    def __merge_versions(self, grouped_found_terms):

        merged_spans = []
        for found_terms in grouped_found_terms:
            # list of pairs of the version and its span text
            found_terms = (
                (i, BeautifulSoup(i, "html.parser").find("span"))
                for i in found_terms
            )
            # sort on the length of the span text to avoid issues with
            # substrings
            found_terms = sorted(
                found_terms, key=lambda x: len(x[-1].text), reverse=True
            )

            # version with the largest span text
            current_span = found_terms[0][0]
            for i in xrange(1, len(found_terms)):
                current_span = self.__merge_strings(
                    current_span, found_terms[i][-1]
                )

            merged_spans.append(current_span)

        return merged_spans

    def recreate_doc(self):

        tagged_spans = []
        for p_tag in self.parsed_soup.find_all("p"):
            for term in self.tfidf_terms:
                normalize_p_tag = normalize_text(p_tag.text)
                if term in normalize_p_tag:
                    tagged_span = self.__find_index(
                        term, normalize_p_tag,
                        p_tag.text, self.tfidf_terms[term]
                    )
                    if tagged_span:
                        tagged_spans.append(tagged_span)

        grouped_found_terms = {}
        for tagged_span in tagged_spans:
            key = BeautifulSoup(tagged_span, "html.parser").text
            grouped_found_terms.setdefault(key, []).append(tagged_span)

        grouped_found_terms = grouped_found_terms.values()

        final_spans = self.__merge_versions(grouped_found_terms)

        for p_tag in self.parsed_soup.find_all("p"):
            for final_span in final_spans:
                final_span = BeautifulSoup(final_span, "html.parser")
                if final_span.text == p_tag.text:
                    p_tag.string = ""
                    p_tag.insert(0, final_span)
                    break

    def get_new_html(self):

        return self.parsed_soup.prettify().replace("&gt", ">").encode("utf-8")
