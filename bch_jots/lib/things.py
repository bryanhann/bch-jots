#!/usr/bin/env python3

import datetime
from pathlib import Path
from bch_jots.lib.fns import lfilter, lmap
import bch_jots.lib.fns as FN
NOW = datetime.datetime.now()

def seconds4delta(delta): return delta and int(delta.total_seconds())
def dt4stamp(stamp): return datetime.datetime.strptime(stamp,"%Y%m%dT%H%M%S")
def name4tag(tag): return tag[1:-1]

def parts4line(line):
    class Namespace: pass
    parts=Namespace()
    parts.stamp, _, line = line.partition(' ')
    parts.tags, _, line = line.partition( '|' )
    parts.lines = line
    return parts

def names4line(line):
    return [ name4tag(tag) for tag in parts4line(line).tags.split() ]

def thing4line(line):
    if not line.startswith('2'): return None
    dots='.'.join(names4line(line)) + '.'
    if dots.startswith('zjot.task.push'): return myPush(line)
    if dots.startswith('zjot.task.pop'): return myPop(line)
    if dots.startswith('zjot.task.reset'): return myReset(line)
    return myZjot(line)

def things4pth(pth):
    def lines4pth(pth): return Path(pth).read_text().split('\n')
    return lmap( thing4line,lines4pth(pth) )
def things4lines(lines):
    def good(line): return line.startswith('2')
    return lmap( thing4line, lfilter(good,lines))
def things4today():
    return things4lines( FN.lines4cmd( 'bch.zjot.show.today' ))

def isOpen(task): return isOpener(task) and not task.is_closed()


class myZjot:
    def __init__(self, line):
        parts = parts4line(line)
        self._line = line
        self._stamp = parts.stamp
        self._tags = parts.tags
        self._lines = parts.lines
        self._t0 = dt4stamp(self._stamp)
        self._t1 = None
    def __repr__(s):    return f"{s.stamp()} {s.short()} <{s.name()}>"
    def name(s):    return s.__class__.__name__
    def tags(s):    return lmap(name4tag, s._tags.split())
    def dt(s):      return s._t0
    def t0(s):      return s._t0
    def lines(s):   return s._lines.split('|')
    def short(s):   return f"{s.tags()} {s.lines()}"
    def words(s):   return s.lines()[0].strip().split()
    def stamp(s):   return s.dt().strftime('%Y-%m-%d-T-%H:%M:%S')


class myTask(myZjot):
    def __init__(self, *a, **b):
        myZjot.__init__(self, *a, **b)
        self._depth = 0
        self._partner = None
    def set_partner(self, partner):
        self._partner = partner
        self.close(partner.dt())
    def set_depth(s,d): s._depth = d
    def close(s, dt):   s._t1 = dt
    def depth(s):       return s._depth
    def t1(s):          return s._t1 and s._t1 or NOW
    def age(s):         return s.t1() - s.t0()
    def s_age(s):       return s.age().seconds
    def is_closed(s):   return s._partner is not None
    def desc(s):        return '-'.join(s.words())
    def __repr__(s):    return f"{s.stamp()} {s.short()}"

class myPush(myTask):
    def short(self):
        closed = self.closed() and '<closed>' or ''
        pad = '  ' * self.depth()
        return f"{pad}+[{self.desc()}] [{self.s_age()}] {closed}"
    def __init__(s, *a, **b):
        myTask.__init__(s, *a, **b)
        s._closer = None
    def set_closer(s, closer): s._closer = closer
    def closed(s): return bool(s._partner)

class myPop(myTask):
    def __init__(self, *a, **b):
        myTask.__init__(self, *a, **b)
        self._opener = None
    def set_opener(self, opener):
        self._opener = opener
    def short(self):
        if self._partner:
            pad = '  ' * self._partner.depth()
            desc = self._partner.desc()
        else:
            pad = ''
            desc = []
        return f"{pad}-[{desc}] [{self.desc()}]"
    def inject(self, aPush):
        self._thepush = aPush

class myReset(myTask):
    pass


