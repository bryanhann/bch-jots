
<repo> : full pathname of repository root
<bch>  : <repo>/.bch
<user> : <bch>/user
<init> : <bch>/init
<bin>  : <bch>/bin

This repository is configured when either
    1. ~/.profile sources <bch>/dot-profile
    2. ~/.bashrc  sources <bch>/dot-profile

These sourced scripts, in turn, sources
    3. <init>/init.sh

This sources the numbered scripts
    4. <init>/NNN.description

The last of these sources
    5. <user>/config.sh

This sources the numbered scripts
    6. <user>/NNN.*


Scripts
-------
    These scripts are invoked indirectly by <init>/init.sh
    Their behaviour is controlled by flags <user>/flag.*

    <user>/config.sh
        : the initial script that calls the numbered scripts.

    <user>/000.verbose-notice
        : warn the user if the verbose flag is set

    <user>/100.append-bin-to-path
        : append __bin__ to environment PATH.
        : there is an example script in the bin.
        : remove this script to turn off.

    <user>/200.demo
        : demonstrate how to use __export__
        : useful for setting environment for the repo

    <user>/flag.verbose
        : the existance of this flag makes the sourcing verbose.
        : useful for initial testing, but you will probably want to remove it.


The user script have access to dunder functions and dunder environment
variables provided by <init>/init.sh

Functions
---------

     __append__ <path>
        : append <path> to $PATH if not already on it

     __export__ <name> <value>
        : same as export <prefix>_<name>=<value>
        : where <prefix> is preset for the repo

Variables
---------

     __hyph__
        : hyphenated project name

     __root__
        : full path to <repo>.

     __bin__
        :full path to <repo>/.bch/bin


