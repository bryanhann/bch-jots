#!/usr/bin/env python3

from pathlib import Path

import bch_jots.lib.things as XX
from bch_jots.lib.fns import lmap, lfilter, lines4cmd

#def things4pth(pth#):
#    def lines4pth(pth): return Path(pth).read_text().split('\n')
#    return lmap( XX.thing4line,lines4pth(pth) )
#def things4lines(lines):
#    def good(line): return line.startswith('2')
#    return lmap(good,lines)
#def things4today():
#    return things4lines( lines4cmd( 'bch.zjot.show.today' ))
#
def isOpen(task): return isOpener(task) and not task.is_closed()
def isClosed(task): return isOpener(task) and task.is_closed()
def isOpener(task): return isinstance(task, XX.myPush)
def isCloser(task): return isinstance(task, XX.myPop)
def isReset(task): return isinstance(task, XX.myReset)


def index44(fn,xS): return [ i for (i,x) in enumerate(xS) if fn(x)]
def last(xS, d=None): return xS and xS[-1] or d

def open4jots(jots): return [jot for jot in jots if isOpen(jot)]
def tasks4jots(jots): return lfilter(XX.myTask, jots)
def current4(jots): return jots[last(index44(isReset,jots)):]
def jots4today(): return XX.things4lines(lines4cmd( 'bch.zjot.show.today' ))

def prep(jots):
    stack = []
    for jot in jots:
        if isOpener(jot):
            jot.set_depth(len(stack))
            stack.append(jot)
        elif isCloser(jot):
            if stack:
                stack[-1].set_partner(jot)
                jot.set_partner(stack[-1])
                stack.pop(-1)
        elif isReset(jot):
            stack = []
    return jots

def outstanding(jots):
    return lfilter(isOpen, prep(current4(jots)))
