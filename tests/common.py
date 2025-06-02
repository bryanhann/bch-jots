#!/usr/bin/env python3

from pathlib import Path
import bch_jots.lib.things as things
import bch_jots.lib.tasking as tasking

STANDARD = Path(__file__).parent/'samples'/'standard'
LINE = "20250523T090102 {zjot} {task} {push} |  a  b  |  c  d  "
PARTS = things.parts4line(LINE)
OPENER = things.thing4line(LINE)
JOTS = things.things4pth(STANDARD)
