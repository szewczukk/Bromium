#!/usr/bin/env python
import glob
import os

import object

# Getting path of all files in directory
dir_path = os.path.dirname(os.path.relpath(__file__))

relative_path = input("Give relative path of header files location (e.g headers/): ")
extension = input("Give extension of header files (e.g .h / .hpp): ")
output_path = input("Give path to catalog in witch create HTML documentation (e.g output/): ")

header_glob = glob.glob(dir_path + relative_path + "*" + extension)

objects = []

iterator = -1
# Printing content of files
for file in header_glob:
    f = open(file, 'r').read().splitlines()
    iterator += 1
    a = object
    objects.append(a)
    for line in f:
        line = line.strip()
        if line[:2] == "//":
            operator = line[2:7]
            if operator == "[nam]":
                objects[iterator].nam = line[8:len(line)-1]
            if operator == "[des]":
                objects[iterator].des = line[8:len(line) - 1]
            if operator == "[arg]":
                objects[iterator].arg = line[8:len(line) - 1]
            if operator == "[ret]":
                objects[iterator].ret = line[8:len(line) - 1]
            if operator == "[cla]":
                objects[iterator].cla = line[8:len(line) - 1]

print("Reading files completed.")

# Reading utils
html_util = open("utils/raw.html", "r")
html_util_content = html_util.read()

css_util = open("utils/styles.css", "r")
css_util_content = css_util.read()

print("Reading utls completed.")

# Saving final files
save_file = open(output_path + "index.html", "w")
save_content = ""

for o in objects:
    save_content += "<p>\nName: " + o.nam + "<br>\n"
    save_content += "Class: " + o.cla + "<br>\n"
    save_content += "Description: " + o.des + "<br>\n"
    save_content += "Arguments: " + o.arg + "<br>\n"
    save_content += "Returning: " + o.ret + "<br>\n</p>\n"

after_html_file = "</div>" \
                  "</body>" \
                  "</html>"

save_file.write(html_util_content + save_content + after_html_file)

css_file = open(output_path + "styles.css", "w")
css_file.write(css_util_content)

print("Writing html file completed.")