#!/usr/bin/env python3

import typer
import bch_jots.ui as ui
cli = typer.Typer()

@cli.command()
def tasks():
    ui.cmd_tasks()

@cli.command()
def all():
    ui.cmd_all()


