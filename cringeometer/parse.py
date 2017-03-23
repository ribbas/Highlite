#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""parse
"""

# from __future__ import absolute_import, print_function, unicode_literals
import subprocess
import operator
from string import punctuation as PUNCTUATION

from nltk.stem import WordNetLemmatizer

from config import PARSED_PATH, STOPWORDS


class PDFToText(object):

    def __init__(self, path):

        self.path = path
        subprocess.call(["pdftotext", self.path, PARSED_PATH])

        with open(PARSED_PATH) as parsed_file:
            self.parsed_text = parsed_file.read()

        self.bow = {}

    def generate_bow(self):

        wordnet_lemmatizer = WordNetLemmatizer()
        normalized_text = self.parsed_text.replace(
            '\r', '\n').replace('\n', ' ').lower()

        punctuation = '!"#$%&\'()*+,/:;<=>?[\\]^_`{|}~'

        for p in punctuation:
            normalized_text = normalized_text.replace(p, '')

        words = filter(lambda x: x.strip() != '', normalized_text.split(' '))
        words = filter(lambda x: x not in STOPWORDS, words)

        for i in words:
            try:
                unicode(i)
            except UnicodeError:
                words.remove(i)

        with open("sample.txt", 'w') as samp:
            samp.write(' '.join(words))

        # stem words
        words = map(lambda x: wordnet_lemmatizer.lemmatize(x), words)
        bow = {}
        for w in words:
            if w not in bow.keys():
                bow[w] = 1
            else:
                bow[w] += 1
        # remove special words that are wrong
        fake_words = ('>', '<')
        bowwords = bow.keys()
        for bw in bowwords:
            if bw in fake_words:
                bow.pop(bw)
            elif bw.find(']') >= 0:
                bow.pop(bw)
            elif bw.find('[') >= 0:
                bow.pop(bw)
        # not big enough? remove instrumental ones among others
        if len(bow) <= 3:
            return None

        print(sorted(bow.items(), key=operator.itemgetter(1), reverse=True))
        return bow


if __name__ == '__main__':

    obj = PDFToText("../sample/resume.pdf")
    obj.generate_bow()
