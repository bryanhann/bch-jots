#!/usr/bin/env python3

from functools import cache

import bch_jots.lib.klasses as KLASSES

@cache
def jots4pth(pth=None):
    return list(filter(None,KLASSES.jots4pth(pth)))

@cache
def tasks4pth(pth=None):
    return [ x for x in jots4pth(pth) if isinstance(x,task) ]

@cache
def reset4pth(pth):
    return lfilter( lambda x:x.is_reset(), tasks4pth() )

def prep_current(pth=None):
    def is_current(task): return task._dt > resets()[-1]._dt
    def current_tasks(pth=None): yield from filter( is_current, tasks(pth=None) )
    stack = []
    for task in current_tasks(pth):
        if task.is_push():
            task.set_depth(len(stack))
            stack.append(task)
        elif task.is_pop():
            stack and stack.pop(-1).finish(task)

def cmd_prompt(*args):
    def is_active(task): return bool(task.is_active())
    def actives(): return lfilter(is_active, TASKS())
    items = [ task._prefix for task in actives() ]
    line='|'.join(items)
    line = f"{line}"
    Q_PROMPT.write_text(line)
