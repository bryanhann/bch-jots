#!/usr/bin/env python3
import datetime

from common import  OPENER

import bch_jots.lib.klasses as klasses

def test__stamp () : assert OPENER.stamp() == "2025-05-23-T-09:01:02"
def test__tags  () : assert OPENER.tags() == "zjot task push".split()
def test__words () : assert OPENER.words() == ['a', 'b']
def test__close__age():
    delta = datetime.timedelta(seconds=20)
    OPENER.close(OPENER.dt() + delta)
    assert OPENER.age().seconds == 20



