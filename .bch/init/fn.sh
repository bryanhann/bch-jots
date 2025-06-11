::dbg:: () {
    [ -f ~/DEBUG ] && echo [:dbg:] $@
}

::lbin:: () {
    local real
    local link
    for real in $(ls $1/bch.*); do
        link=~/.local/bin/$(basename $real)
        [   -f ${link} ] && ::dbg:: [:lbin:] found $link
        [   -f ${link} ] && continue
        [ ! -f ${link} ] && ::dbg:: [:lbin:] create $link
        [ ! -f ${link} ] && ln -s $real $link
    done
}
