# -*- coding: utf-8 -*-
##
## This file is part of Harvesting Kit.
## Copyright (C) 2014 CERN.
##
## Harvesting Kit is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Harvesting Kit is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Harvesting Kit; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
import unittest
from harvestingkit.utils import (record_add_field,
                                 create_record,
                                 format_arxiv_id,
                                 collapse_initials,
                                 fix_journal_name,
                                 escape_for_xml)
from harvestingkit.tests import journal_mappings


class UtilsTests(unittest.TestCase):

    def test_record_add_field(self):
        data = (u'In this paper we continue the study of Q -operators in'
                u' the six-vertex model and its higher spin generalizations.'
                u' In [1] we derived a new expression for the higher spin R'
                u' -matrix associated with the affine quantum algebra '
                u'<math altimg="si1.gif" xmlns="http://www.w3.org/1998/Math/MathML">'
                u'<msub><mrow><mi>U</mi></mrow><mrow><mi>q</mi></mrow></msub>'
                u'<mo stretchy="false">(</mo><mover accent="true"><mrow><mrow>'
                u'<mi mathvariant="italic">sl</mi></mrow><mo stretchy="false">'
                u'(</mo><mn>2</mn><mo stretchy="false">)</mo></mrow><mrow><mo>'
                u'^</mo></mrow></mover><mo stretchy="false">)</mo></math>'
                u' . Taking a special limit in this R -matrix we obtained new'
                u' formulas for the Q -operators acting in the tensor product'
                u' of representation spaces with arbitrary complex spin.')
        rec = create_record()
        record_add_field(rec, '520', subfields=[('a', data)])
        data = (u"<record><datafield ind1=\"\" ind2=\"\" tag=\"520\">"
                u"<subfield code=\"a\">") + data
        data += u"</subfield></datafield></record>"
        self.assertEqual(rec.toxml(), data)

    def test_format_arxiv_id(self):
        self.assertEqual(format_arxiv_id("arXiv:1312.1300"), "arXiv:1312.1300")
        self.assertEqual(format_arxiv_id("1312.1300"), "arXiv:1312.1300")
        self.assertEqual(format_arxiv_id("arxiv:hep/1312/1300", True), "hep/1312/1300")
        self.assertEqual(format_arxiv_id("arxiv:hep/1312/1300"), "arxiv:hep/1312/1300")

    def test_collapse_initials(self):
        self.assertEqual(collapse_initials("T. A. Adams"), "T.A. Adams")
        self.assertEqual(collapse_initials("T.   A. Adams"), "T.A. Adams")
        self.assertEqual(collapse_initials("T. A. V. Adams"), "T.A.V. Adams")

    def test_fix_journal_name(self):
        self.assertEqual(fix_journal_name("A&A", journal_mappings), ('Astron.Astrophys.', ""))
        self.assertEqual(fix_journal_name("A&A B", journal_mappings), ('Astron.Astrophys.', "B"))
        self.assertEqual(fix_journal_name("A&A.B", journal_mappings), ('A&A.', "B"))
        self.assertEqual(fix_journal_name("A&AB.", journal_mappings), ("A&AB.", ""))

    def test_escape_ampersand(self):
        self.assertEqual(escape_for_xml("A&A"), "A&amp;A")
        self.assertEqual(escape_for_xml("A&amp;A & B"), "A&amp;A &amp; B")
        self.assertEqual(escape_for_xml("A &amp; A.B"), "A &amp; A.B")
        self.assertEqual(escape_for_xml("asdasdsa &lt;1 A"), "asdasdsa &lt;1 A")
        self.assertEqual(escape_for_xml("asdasdsa <=1 A"), "asdasdsa &lt;=1 A")
        self.assertEqual(escape_for_xml("asdasdsa <.2 A"), "asdasdsa &lt;.2 A")
        self.assertEqual(escape_for_xml("asdasdsa < 2 A"), "asdasdsa &lt; 2 A")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UtilsTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
