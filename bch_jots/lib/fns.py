#!/usr/bin/env python3
import os
import subprocess
from functools import cache
import sys
import datetime
import inspect
import itertools
from pathlib import Path

NOW = datetime.datetime.now()

def lmap (*args): return list(map(*args))
def lfilter(*args): return list(filter(*args))
def dt4stamp(stamp): return datetime.datetime.strptime(stamp,"%Y%m%dT%H%M%S")
def zjot4obj(obj): return klass4obj( obj )( obj )
def zjot4line(line): return zjot4obj(obj4line(line))
def is_zjot_class(v): return inspect.isclass(v) and issubclass(v,Zjot)
def good_pair( pair ): return inspect.isclass(pair[1]) and issubclass(pair[1],Zjot)
def good_dict(): return dict( filter( good_pair, globals().items() ) )
def name4obj(obj): return (names4tags(obj.tags) + [''])[0]
def klass4obj(obj): return good_dict().get( name4obj(obj) , Zjot)
def name4tag(tag): return tag[1:-1]
def names4tags(tags): return lmap(name4tag,tags)
def is_tag(tag): return tag.startswith('{') and tag.endswith('}')
def seconds4delta(delta): return delta and int(delta.total_seconds())

def prep_current():
    stack = []
    for task in current_tasks():
        if task.is_push():
            task.set_depth(len(stack))
            stack.append(task)
        elif task.is_pop():
            stack and stack.pop(-1).finish(task)

def is_head(task): return bool(task.is_push())
def heads(): return lfilter(is_head, TASKS())
def is_active(task): return bool(task.is_active())
def heads(): return lfilter(is_head, TASKS())
def actives(): return lfilter(is_active, TASKS())
def dt4line(line): return dt4stamp(stamp4line(line))






import bch_jots.lib.klasses as KLASSES

jots4pth = KLASSES.jots4pth
#from bch_jots.lib.klasses import jots4pth

@cache
def all_tasks(_file=None):
    return [ x for x in jots4pth(_file) if isinstance(x,task) ]
    #return [ x for x in jots4file(_file) if isinstance(x,task) ]
    #if not _file:
    #    return [ x for x in JOTS() if isinstance(x,task) ]

@cache
def resets(): return lfilter( lambda x:x.is_reset(), all_tasks() )

def is_current(task): return task._dt > resets()[-1]._dt

def current_tasks(): yield from filter( is_current, all_tasks() )

######################################################################################
def cmd_foo(*args):
    for zjot in current_tasks():
        print( zjot.age(), zjot.tags()[1], zjot)

def cmd_all(*args): [ task.report() for task in heads() ]
def cmd_default(*args): cmd_active(*args)
def cmd_active(*args):
    for task in actives():
        task.report_active()

def cmd_prompt(*args):
    items = [ task._prefix for task in actives() ]
    line='|'.join(items)
    line = f"{line}"
    Q_PROMPT.write_text(line)

def fn4cmd(cmd):
    try:
        fn = eval( f"cmd_{cmd}" )
    except NameError:
        exit(f'commmand [{cmd}] not found' )
    return fn

def main (cmd='default', *args):
    #prep_buffer()
    fn4cmd(cmd)(args)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(*args)


