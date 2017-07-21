# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# from __future__ import absolute_import, print_function, unicode_literals

# from comparevitae.parse import pdf_to_text

# if __name__ == '__main__':

#     print(pdf_to_text("sample/ana.pdf"))


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from comparevitae.metrics import RateResume

if __name__ == '__main__':

    obj = RateResume(
        path="sample/resume3.pdf",
        area="data-science",
        anon=False
    )
    print(obj.generate_tfidf())
