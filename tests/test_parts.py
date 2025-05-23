#!/usr/bin/env python3

from common import PARTS

def test_stamp(): assert PARTS.stamp =="20250523T090102"
def test_tags():  assert PARTS.tags.split() == "{zjot} {task} {push}".split()
def test_lines(): assert PARTS.lines == "  a  b  |  c  d  "
