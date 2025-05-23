#!/usr/bin/env python3

from pathlib import Path
import bch_jots.lib.klasses as klasses

STANDARD = Path(__file__).parent/'samples'/'standard'
LINE = "20250523T090102 {zjot} {task} {push} |  a  b  |  c  d  "
PARTS = klasses.parts4line(LINE)
OPENER = klasses.thing4line(LINE)
JOTS = klasses.things4pth(STANDARD)
