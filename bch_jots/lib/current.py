#!/usr/bin/env python3
import os
from subprocess import run
from functools import cache
import sys
import datetime
import inspect
import itertools
from pathlib import Path


def open4jots(jots):
    return [jot for jot in jots if isOpen(jot)]

def outstanding4jots(jots):
    jots = [jot for jot in jots if isOpener(jot) and not jot.is_closed() ]
    return jots

#    for jot in jots:
#        if isResetisinstance(jot,myReset):
#            acc = []
#            continue
#        if not jot.is_closed():
#            acc.append(jot)
#    for jot in acc:

NOW = datetime.datetime.now()
class Namespace: pass
def lmap(*a,**b): return list(map(*a,**b))
def lfilter(*a,**b): return list(lfilter(*a,**b))
def things4pth(pth): return [ thing4line(line) for line in lines4pth(pth) ]
def names4line(line): return [ name4tag(tag) for tag in parts4line(line).tags.split() ]
def is_zjot_line(line): return line.startswith('2')
def lines4pth(pth): return filter( is_zjot_line, Path(pth).read_text().split('\n') )

def parts4line(line):
    parts=Namespace()
    parts.stamp, _, line = line.partition(' ')
    parts.tags, _, line = line.partition( '|' )
    parts.lines = line
    return parts

def tasks4jots(jots): return [xx for xx in jots if isinstance(xx,myTask)]
def prompt4jots(jots):
    prep(jots)
    jots = open4jots(jots)
    prompt = '|'.join( jot.desc() for jot in jots )
    return prompt

def isOpen(task): return isOpener(task) and not task.is_closed()
def isClosed(task): return isOpener(task) and task.is_closed()
def isOpener(task): return isinstance(task, myPush)
def isCloser(task): return isinstance(task, myPop)
def isReset(task): return isinstance(task, myReset)
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

def thing4line(line):
    dots='.'.join(names4line(line)) + '.'
    if dots.startswith('zjot.task.push'):
        return myPush(line)
    if dots.startswith('zjot.task.pop'):
        return myPop(line)
    if dots.startswith('zjot.task.reset'):
        return myReset(line)
    else:
        return myZjot(line)



def peel_while(fn,parts):
    while parts and fn(parts[0]):
        yield parts.pop(0)

def bch_zjot_show():
    cmd = "bch.zjot show".split()
    return run(cmd, text=True, capture_output=True)

def jots4pth(pth=None):
    def name4tag(tag): return tag[1:-1]
    def names4tags(tags): return list((name4tag,tags))
    def name4obj(obj): return (names4tags(obj.tags) + [''])[0]
    def _pair( pair ): return inspect.isclass(pair[1]) and issubclass(pair[1],Zjot)
    def _dict(): return dict( filter( _pair, globals().items() ) )
    def klass4obj(obj): return _dict().get( name4obj(obj) , Zjot)
    def zjot4obj(obj): return klass4obj( obj )( obj )
    def zjot4line(line):
        if not line.startswith('2'):
            return None
        return zjot4obj(obj4line(line))

    text = pth and pth.read_text() or bch_zjot_show().stdout
    lines = text.split('\n')
    #lines = [line for line in lines if line and line[0] in '12']
    return list(map( zjot4line, lines ))

def seconds4delta(delta):
    return delta and int(delta.total_seconds())

def dt4stamp(stamp):
    return datetime.datetime.strptime(stamp,"%Y%m%dT%H%M%S")

def obj4line(line):
    def is_tag(tag): return tag and tag[0]=='{'
    parts = line.split() + ['']
    obj = Namespace()
    obj.line = line
    obj.stamp = parts.pop(0)
    obj.zjot = parts.pop(0)
    obj.tags = list(peel_while(is_tag, parts))
    obj.prefix = list(peel_while(lambda x: not x=='|', parts))
    obj.content = parts
    return obj

def name4tag(tag):
    return tag[1:-1]
class myZjot:
    def __init__(self, line):
        parts = parts4line(line)
        self._line = line
        self._stamp = parts.stamp
        self._tags = parts.tags
        self._lines = parts.lines
        self._t0 = dt4stamp(self._stamp)
        self._t1 = None
    def name(self): return self.__class__.__name__
    def tags(self): return lmap(name4tag, self._tags.split())
    def dt(self): return self._t0
    def t0(self): return self._t0
    def lines(self): return self._lines.split('|')
    def short(s):
        return f"{s.tags()} {s.lines()}"

    def __repr__(s):
        return f"{s.stamp()} {s.short()} <{s.name()}>"

    def words(s): return s.lines()[0].strip().split()
    #return datetime.datetime.strptime(stamp,"%Y%m%dT%H%M%S")
    def stamp(s): return s.dt().strftime('%Y-%m-%d-T-%H:%M:%S')


class myTask(myZjot):
    def __repr__(s):
        return f"{s.stamp()} {s.short()}"
    def desc(s): return '-'.join(s.words())
    def __init__(self, *a, **b):
        myZjot.__init__(self, *a, **b)
        self._depth = 0
        self._partner = None
    def set_partner(self, partner):
        self._partner = partner
        self.close(partner.dt())
    def set_depth(self, depth):
        self._depth = depth
    def depth(self):
        return self._depth
    def close(self, dt):
        #print( self._t1 )
        #print( dt )
        self._t1 = dt
    def t1(self):
        return self._t1 and self._t1 or NOW
    def age(self): return self.t1() - self.t0()
    def s_age(s): return s.age().seconds
    def is_closed(s): return s._partner is not None

class myPush(myTask):
    def short(self):
        closed = self.closed() and '<closed>' or ''
        pad = '  ' * self.depth()
        return f"{pad}+[{self.desc()}] [{self.s_age()}] {closed}"
    def __init__(self, *a, **b):
        myTask.__init__(self, *a, **b)
        self._closer = None
    def set_closer(self, closer):
        self._closer = closer
    def closed(self):
        return bool(self._partner)
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
    pass
    #def __init__(*a, **b): myTask.__init__(*a, **b)
class myReset(myTask):
    pass
    #def __init__(*a, **b): myTask.__init__(*a, **b)
class Zjot:
    def __init__(self, obj):
        self._line = obj.line
        self._stamp = obj.stamp
        self._zjot = obj.zjot
        self._tags = obj.tags
        self._prefix = ' '.join(obj.prefix)
        self._content = ' '.join(obj.content)
        self._dt = dt4stamp(self._stamp)
    def __repr__(self):
        klass = self.__class__.__name__
        line = f"{self._dt} {' '.join(self._tags)} {self._prefix} {self._content}"
        line = f"{line:60} --- <{klass}>"
        return line
    def tags(self): return [ x[1:-1] for x in self._tags ] + [''] * 5
    def age(self): return NOW - self._dt
    def time(self): return str(self._dt).split()[1]


class task(Zjot):
    def __init__(self,obj):
        Zjot.__init__(self,obj)
        self._t1 = None
        self._depth = 0
    def report_active(self): print( f"{self.indent()}++{self._prefix}" )

    def report_closed(s):
        seconds = s.seconds() or 0
        print( f"{seconds:5} | {s.indent()}{s._prefix}" )

    def indent(s):      return '  ' * (self._depth)
    def report(s):      s.report_closed()
    def is_push(s):     return s._tags[1] == '{+}'
    def is_pop(s):      return s._tags[1] == '{-}'
    def is_reset(s):    return s._tags[1] == '{reset}'
    def is_active(s):   return s.is_push() and not s._t1
    def finish(s, o):   s._t1 = o._dt
    def push(s,depth):  s._depth = depth
    def show(s):        print(f"{s._depth} {s}")
    def elapsed(s):     return s._t1 and s._t1 - s._dt or None
    def completed(s):   return s._t1 is not None
    def seconds(s):     return seconds4delta(s.elapsed())
    def set_depth(s,d): s._d = depth
    def __repr__(s):    return f"{s._prefix} {s._content} : {s.time()} [{s.elapsed()}]"

