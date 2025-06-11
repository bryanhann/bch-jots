#!/usr/bin/env bash

source $(dirname $BASH_SOURCE)/fn.sh

for pth in $(ls $(dirname ${BASH_SOURCE[0]})/[0-9]*); do
    ::dbg:: ". $(basename $pth)"
    source $pth
done

