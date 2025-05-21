#!/usr/bin/env bash

for pth in $(ls ${__user__}/[0-9]*); do
    __verbose__ "        . ${pth}"
    . ${pth} "$@"
done
