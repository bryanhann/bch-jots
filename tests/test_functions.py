#!/usr/bin/env python3
import common as FIX

import pytest

import bch_jots.lib.current as current
import bch_jots.lib.things as things


def test_names4line():
    assert things.names4line(FIX.LINE) == "zjot task push".split()

def test_prompt4jots():
    assert current.prompt4jots(FIX.JOTS) == "coding-deedoo|documenting-feature"

