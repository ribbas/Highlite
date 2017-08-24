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


def penn_to_wn(tag):

    if tag in ("JJ", "JJR", "JJS"):
        return wn.ADJ

    elif tag in ("RB", "RBR", "RBS"):
        return wn.ADV

    elif tag in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ"):
        return wn.VERB

    return wn.NOUN


def normalize_text(content, ignore_words=[]):

    lemma = WordNetLemmatizer()
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


def find_index(word, normalized_sent, sentence):

    sentence = "Certificate in Data Science"
    normalized_sent = "certificate in data science"
    word = "data science"

    if len(sentence) == len(normalized_sent):
        start = normalized_sent.find(word)
        end = start + len(word)
        return sentence.replace(
            sentence[start:end], sentence[start:end] + "YOOOOOO")

    stemmer = PorterStemmer()
    re_pat = " ".join(
        stemmer.stem(i) for i in word.split()
    ).replace(" ", ".*") + "[^|\s]+"
    regex = re.compile(re_pat, re.I | re.M)
    return sentence.replace(
        regex.findall(sentence)[0],
        regex.findall(sentence)[0] + "YOOOOOOO"
    )


def recreate_doc(tfidf_scores_path, parsed_html):

    tfidf_scores = {}

    with open(tfidf_scores_path) as tfidf_scores_file:
        tfidf_scores = json.load(tfidf_scores_file)

    tfidf_terms = tfidf_scores["tfidf_scores"]

    parsed_html = " ".join(parsed_html).replace("&#160;", " ")
    parsed_soup = BeautifulSoup(parsed_html, "html.parser")

    for p_tag in parsed_soup.find_all("p"):
        for term in tfidf_terms:
            if term in normalize_text(p_tag.text):
                print term, tfidf_terms[term], "<=>", normalize_text(p_tag.text), "<=>", p_tag.text
                # p_tag.string = "YOOOOOOOOOOOO"

    # print(parsed_soup.find_all("p"))
    # return " ".join(i.text for i in parsed_soup.findAll("p"))
