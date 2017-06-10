#!/usr/bin/env python

try:
    from sys import argv

    arg = argv[1]
except IndexError:
    arg = ""

# If argument "modify" was given
if arg == "modify":
    from os import system

    system("gedit .bromine/templates.xml")

# If there is no detectable argument
else:
    from logic import logic
    logic(arg)
