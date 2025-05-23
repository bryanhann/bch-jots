#!/usr/bin/env python3
from common import STANDARD, LINE, PARTS, OPENER, JOTS
import datetime
from pathlib import Path

import pytest

import bch_jots.lib.klasses as klasses


def test_names4line():
    assert klasses.names4line(LINE) == "zjot task push".split()

def test_prompt4jots():
    assert klasses.prompt4jots(JOTS) == "coding-deedoo|documenting-feature"

