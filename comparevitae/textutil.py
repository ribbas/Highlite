#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json
import re
from string import punctuation

from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from nltk import pos_tag
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

lemma = WordNetLemmatizer()
stemmer = PorterStemmer()


def color(str0, i=2):
    return "\x1b[6;30;4{}m".format(i) + str0 + "\x1b[0m"


def penn_to_wn(tag):

    if tag in ("JJ", "JJR", "JJS"):
        return wn.ADJ

    elif tag in ("RB", "RBR", "RBS"):
        return wn.ADV

    elif tag in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ"):
        return wn.VERB

    return wn.NOUN


def normalize_text(content, ignore_words=[]):

    norm_text = content.encode("ascii", "ignore").lower()

    for punc in punctuation:
        norm_text = norm_text.replace(punc, " ")

    words = norm_text.split()

    words = (
        word for word in words if not any([x in word for x in ignore_words])
    )
    words = [word for word in words if not word.isdigit()]
    words = pos_tag(words)
    words = [
        lemma.lemmatize(word[0], penn_to_wn(word[-1]))
        for word in words
    ]

    for i, word in enumerate(words):
        if any(p in word for p in ("(", ")")):
            words[i] = word[word.find("(") + 1:word.find(")")]

    time_filtered = []

    for word in words:
        try:
            if date_parser.parse(word):
                pass

        except (TypeError, ValueError):
            time_filtered.append(word)

    return " ".join(filter(None, time_filtered))


def find_index(word, normalized_sent, sentence, score):

    if len(sentence) == len(normalized_sent):
        start = normalized_sent.find(word)
        end = start + len(word)
        return sentence.replace(
            sentence[start:end],
            "<div style=\"{}\">".format(score) + sentence[start:end] + "</div>"
        )

    re_str = " ".join(
        stemmer.stem(i) for i in word.split()
    ).replace(" ", ".*") + "([.-]|[^\s]+|[^\s]*?)"
    regex = re.compile(re_str, re.I)
    matches = regex.search(sentence)
    # print(re_str)
    try:
        return sentence.replace(
            matches.group(),
            # TODO: LEARN HTML
            "<div style=\"background-color: rgba(255, 0, 0, {})\">".format(20 * score + 5) +
            matches.group() + "</div>"
        )
    except AttributeError:
        print "failed \x1b[3;31;40m" + re_str + "\x1b[0m"


def __merge_strings(final_str, version):

    final_soup = BeautifulSoup(final_str, "html.parser")
    version_div = BeautifulSoup(version, "html.parser").find("div")

    for fixed_div in final_soup.find_all("div"):
        if not fixed_div.text == version_div.text:
            return final_str.replace(
                version_div.text, unicode(version_div)
            )

    return final_str


def __merge_versions(grouped_found_terms):

    merged_divs = []
    for found_terms in grouped_found_terms:
        found_terms = sorted(
            found_terms,
            key=lambda x: len(BeautifulSoup(x, "html.parser").find("div").text),
            reverse=True
        )

        cursor = found_terms[0]
        for i in xrange(1, len(found_terms)):
            cursor = __merge_strings(cursor, found_terms[i])

        merged_divs.append(cursor)

    return merged_divs


def recreate_doc(tfidf_scores_path, parsed_html):

    tfidf_scores = {}
    FAILED = 0
    SUCCESS = 0

    with open(tfidf_scores_path) as tfidf_scores_file:
        tfidf_scores = json.load(tfidf_scores_file)

    tfidf_terms = tfidf_scores["tfidf_scores"]

    parsed_html = " ".join(parsed_html).replace("&#160;", " ")
    parsed_soup = BeautifulSoup(parsed_html, "html.parser")

    tagged_divs = []
    for p_tag in parsed_soup.find_all("p"):
        for term in tfidf_terms:
            if term in normalize_text(p_tag.text):
                x = find_index(term, normalize_text(p_tag.text),
                               p_tag.text, tfidf_terms[term])
                if not x:
                    FAILED += 1
                else:
                    SUCCESS += 1
                    tagged_divs.append(x)

    grouped_found_terms = {}
    for elem in tagged_divs:
        key = BeautifulSoup(elem, "html.parser").text
        grouped_found_terms.setdefault(key, []).append(elem)

    grouped_found_terms = grouped_found_terms.values()

    final_divs = __merge_versions(grouped_found_terms)

    for p_tag in parsed_soup.find_all("p"):
        for final_div in final_divs:
            final_div = BeautifulSoup(final_div, "html.parser")
            if final_div.text == p_tag.text:
                p_tag.insert(1, final_div)
                break

    print parsed_soup.prettify()
