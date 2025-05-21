#!/usr/bin/env bash

__hyph__=bch-jots
__pref__=BCH_JOTS
__caller__=$(basename $1)
__temp__=${HOME}/.tmp/tmp.${__hyph__}
__init__=$(dirname $BASH_SOURCE[0]})
__dots__=$(dirname ${__init__})
__root__=$(dirname ${__dots__})
__lib__=${__dots__}/lib
__bin__=${__dots__}/bin
__user__=${__dots__}/user
__fVerbose__=${__dots__}/flag.verbose

__verbose__ () {
    [ -f $__fVerbose__ ] || return
    echo "$@"
}

__export__ () {
    export ${__pref__}_$1=$2;
}

__append__ () {
    [[ ":$PATH:" == *":${1}:"* ]] && return
    echo "# PATH += $1"
    export PATH=${PATH}:${1}
}


for pth in $(ls ${__init__}/[0-9]*); do
    __verbose__ "        . ${pth}"
    . ${pth} ${__caller__}
done

unset __hyph__
unset __pref__
unset __caller__
unset __temp__
unset __init__
unset __dots__
unset __root__
unset __lib__
unset __bin__
unset __user__
unset __fVerbose__
unset __export__
unset __append__





