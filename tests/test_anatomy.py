import unittest
from tools.anatomy import css_surface

class AnatomyTest(unittest.TestCase):
    def test_comments_strings_and_data(self):
        classes,data=css_surface('/* KATA.md .fake */ .k-select[data-size="sm"] select{content:".fake2";background:url("a.svg")} .real::before{content:".fake3"}')
        self.assertEqual(classes,['k-select','real'])
        self.assertEqual(data,['data-size'])
    def test_grouped_selectors(self):
        self.assertEqual(css_surface('.a,.b{color:red}.a:hover{color:blue}')[0],['a','b'])
