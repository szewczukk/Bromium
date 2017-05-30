# !/usr/bin/env python
import glob
import os

# Getting path of all files in directory
DIR_PATH = os.path.dirname(os.path.relpath(__file__))

RELATIVE_PATH = input("Give relative path of header files location (e.g headers/): ")
EXTENSION = input("Give extension of header files (e.g .h / .hpp): ")
OUTPUT_PATH = input("Give path to catalog in witch create HTML documentation (e.g output/): ")

if RELATIVE_PATH[-1:] != "/":
    RELATIVE_PATH += "/"

if OUTPUT_PATH[-1:] != "/":
    OUTPUT_PATH += "/"

if EXTENSION[:0] != ".":
    EXTENSION = "." + EXTENSION

HEADER_GLOB = glob.glob(DIR_PATH + RELATIVE_PATH + "*" + EXTENSION)

if len(HEADER_GLOB) < 1:
    print("Error! No files to documentation")
    exit(1)

objects = []

# Printing content of files
for file in HEADER_GLOB:
    f = open(file, 'r').read().splitlines()
    for line in f:
        line = line.strip()
        if line[:2] == "//":
            operator = line[2:7]
            content = line[8:len(line) - 1]
            if operator == "[nam]":
                objects.append({"name": "", "desc": "", "args": "", "returns": "", "class": ""})
                objects[len(objects) - 1]["name"] = content
            if operator == "[des]":
                objects[len(objects) - 1]["desc"] = content
            if operator == "[arg]":
                objects[len(objects) - 1]["args"] = content
            if operator == "[ret]":
                objects[len(objects) - 1]["returns"] = content
            if operator == "[cla]":
                objects[len(objects) - 1]["class"] = content

print("Reading files completed.")

# Reading templates
html_util = open("templates/raw.html", "r")
html_util_content = html_util.read()

css_util = open("templates/styles.css", "r")
css_util_content = css_util.read()

print("Reading templates completed.")

# Saving final files
save_file = open(OUTPUT_PATH + "index.html", "w")
save_content = ""

for o in objects:
    save_content += "<p>\nName: " + o["name"] + "<br>\n"
    save_content += "Class: " + o["class"] + "<br>\n"
    save_content += "Description: " + o["desc"] + "<br>\n"
    save_content += "Arguments: " + o["args"] + "<br>\n"
    save_content += "Returning: " + o["returns"] + "<br>\n</p>\n"
    save_content += "<hr>"

after_html_file = "</div>" \
                  "</body>" \
                  "</html>"

save_file.write(html_util_content + save_content + after_html_file)

css_file = open(OUTPUT_PATH + "styles.css", "w")
css_file.write(css_util_content)

print('Writing html file completed.')

css_file.close()
html_util.close()
