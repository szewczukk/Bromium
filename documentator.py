#!/usr/bin/env python
import glob
import os

# Getting path of all files in directory
dir_path = os.path.dirname(os.path.relpath(__file__))

relative_path = raw_input("Give relative path of header files location (e.g headers/): ")
extension = raw_input("Give extension of header files (e.g .h / .hpp): ")
output_path = raw_input("Give path to catalog in witch create HTML documentation (e.g output/): ")

if relative_path[-1:] != "/":
    relative_path += "/"

if output_path[-1:] != "/":
    output_path += "/"

if extension[:0] != ".":
    extension = "." + extension

header_glob = glob.glob(dir_path + relative_path + "*" + extension)

if len(header_glob) < 1:
    print("Error! No files to documentation")
    exit(1)

if not os.path.exists(output_path):
    os.makedirs(output_path)

objects = []

# Printing content of files
for curr_file in header_glob:
    f = open(curr_file, 'r').read().splitlines()
    for line in f:
        line = line.strip()
        if line[:2] == "//":
            operator = line[2:7]
            content = line[8:len(line) - 1]
            if operator == "[nam]":
                objects.append({"name": "", "description": "", "arguments": "", "returns": "", "class": ""})
                objects[len(objects) - 1]["name"] = content
            if operator == "[des]":
                objects[len(objects) - 1]["description"] = content
            if operator == "[arg]":
                objects[len(objects) - 1]["arguments"] = content
            if operator == "[ret]":
                objects[len(objects) - 1]["returns"] = content
            if operator == "[cla]":
                objects[len(objects) - 1]["class"] = content

print("Reading files completed.")

# Reading .documentator
html_util = open(".documentator/raw.html", "r")
html_util_content = html_util.read()

css_util = open(".documentator/styles.css", "r")
css_util_content = css_util.read()

print("Reading templates completed.")

# Saving final files
save_file = open(output_path + "index.html", "w")
save_content = ""

for o in objects:
    save_content += "<p>\nName: " + o["name"] + "<br>\n"
    save_content += "Class: " + o["class"] + "<br>\n"
    save_content += "Description: " + o["description"] + "<br>\n"
    save_content += "Arguments: " + o["arguments"] + "<br>\n"
    save_content += "Returning: " + o["returns"] + "<br>\n</p>\n"
    save_content += "<hr>"

after_html_file = "</div>" \
                  "</body>" \
                  "</html>"

save_file.write(html_util_content + save_content + after_html_file)

css_file = open(output_path + "styles.css", "w")
css_file.write(css_util_content)

print("Writing html file completed.")
