#!/usr/bin/env python3

import bch_jots.lib.things as XX
import bch_jots.lib.tasking as TT
import bch_jots.lib.fns as FN

def setprompt():
    FN.lines4cmd( f"bch.prompt.echo {prompt4jots(XX.things4today())}" )

def prompt4jots(jots):
    PIPE = '|'
    outstanding = TT.outstanding(jots)
    descriptions = [ xx.desc() for xx in outstanding ]
    return PIPE.join(descriptions)


