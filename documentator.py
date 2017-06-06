#!/usr/bin/env python

try:
    from sys import argv

    arg = argv[1]
except IndexError:
    arg = ""

# If argument "modify" was given
if arg == "modify":
    from os import system

    system("gedit .documentator/templates.xml")

# If argument "author was given"
elif arg == "author":
    from os import system

    print ("Author of documentator is Dmitro Szewczuk")
    system("open https://bjornus.github.io")

# If there is no detectable argument
else:
    from logic import logic
    logic(arg)
