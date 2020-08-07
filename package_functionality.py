#!usr/bin/env python3

import fileio
import graphics
import solvers


def getdata(filename):
    specs = fileio._read_schrodinger(filename)