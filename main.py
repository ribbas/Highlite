#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from comparevitae.metrics import RateResume
from comparevitae.textutil import recreate_doc, find_index
from comparevitae.textio import pdf_to_html

if __name__ == "__main__":

    # obj = RateResume(
    #     path="sample/sabbir2.pdf",
    #     areas=["data-science", "computer-science"],
    #     ignore_words=["sabbir", "ahmed", "baltimore", "maryland"],
    #     anon=False,
    # )
    # obj.generate_tfidf(stop_words="english")
    # obj.get_score()
    # recreate_doc()
    # x = pdf_to_html("sample/sabbir1.pdf")
    # recreate_doc(tfidf_scores_path="resume_tfidf.json", parsed_html=x)
    # print(find_index(1, 2, 3))

    from textwrap import dedent
    TEST = dedent("""
        • Best Education Hack winning web application that predicted the discipline of the user’s <div style="0.016160527539">school</div> curriculums
        • <div style="0.04063447037">Best Education Hack</div> winning web application that predicted the discipline of the user’s school curriculums
        • Best Education <div style="0.0812689407401">Hack</div> winning web application that predicted the discipline of the user’s school curriculums
        • Best <div style="0.04063447037">Education Hack</div> winning web application that predicted the discipline of the user’s school curriculums
        • Best Education Hack winning web application that predicted the discipline of the <div style="0.0211116784262">user’s</div> school curriculums
        • Best Education Hack winning web application that predicted the discipline of the user’s school <div style="0.0252122523599">curriculums</div>
        • Best Education Hack winning web application that <div style="0.0470029256762">predicted</div> the discipline of the user’s school curriculums
        • Best Education Hack winning web application that predicted the discipline of the user’s <div style="0.0372937480598">school curriculums</div>
        • Best Education Hack winning web application that predicted the discipline of the <div style="0.04063447037">user’s school</div> curriculums
        • <div style="0.0230019623321">Best</div> Education Hack winning web application that predicted the discipline of the user’s school curriculums
        • Best Education Hack winning <div style="0.0749074302973">web</div> application that predicted the discipline of the user’s school curriculums
        • Best Education Hack winning <div style="0.0776152291155">web application</div> that predicted the discipline of the user’s school curriculums
        • Best Education Hack winning web application that predicted the discipline of the <div style="0.0864547991075">user’s</div> school curriculums
        • <div style="0.04063447037">Best Education</div> Hack winning web application that predicted the discipline of the user’s school curriculums
        • Best Education Hack winning web application that predicted the <div style="0.0303126618726">discipline</div> of the user’s school curriculums
        • Best Education Hack winning web application that predicted the discipline of the <div style="0.04063447037">user’s school curriculums</div>
        • Best <div style="0.0433258613599">Education</div> Hack winning web application that predicted the discipline of the user’s school curriculums
        • Best Education Hack winning web <div style="0.0629939197256">application</div> that predicted the discipline of the user’s school curriculums
    """)

    def color(str0, i=2):

        return "\x1b[6;30;4{}m".format(i) + str0 + "\x1b[0m"

    from bs4 import BeautifulSoup

    def merge_strings(final_str, version):

        final_soup = BeautifulSoup(final_str, "html.parser")
        version_div = BeautifulSoup(version, "html.parser").find("div")

        for fixed_div in final_soup.find_all("div"):
            if not fixed_div.text == version_div.text:
                return final_str.replace(
                    version_div.text, unicode(version_div)
                )

    found_terms = filter(None, TEST.split("\n"))
    found_terms = sorted(
        found_terms,
        key=lambda x: len(BeautifulSoup(x, "html.parser").find("div").text),
        reverse=True
    )

    cursor = found_terms[0]
    for i in xrange(1, len(found_terms)):
        print "\n", color("------------------" + str(i) + "------------------")
        print color("cur"), cursor
        print color("ver"), found_terms[i]
        cursor = merge_strings(cursor, found_terms[i])
        print color("fin"), cursor, "\n"
