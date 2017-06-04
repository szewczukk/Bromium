#!/usr/bin/env python

try:
    from sys import argv

    arg = argv[1]
except IndexError:
    arg = ""

if arg == "modify":
    from os import system

    system("gedit .documentator/templates.xml")
else:
    from logic import logic
    logic(arg)
