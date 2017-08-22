#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from comparevitae.metrics import RateResume

if __name__ == '__main__':

    obj = RateResume(
        path="sample/sabbir2.pdf",
        area="data-science",
        username="sabbir",
        anon=False,
        # build=True,
    )
    print(obj.generate_tfidf())
