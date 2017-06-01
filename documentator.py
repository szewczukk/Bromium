#!/usr/bin/env python
import glob
import os
import sys

# Getting path of all files in directory
dir_path = os.path.dirname(os.path.relpath(__file__))

relative_path = ""
extension = ""
output_path = ""

try:
    arg = sys.argv[1]
except IndexError:
    arg = ""

if not os.path.exists(".documentator/settings.txt") or arg == "new":
    relative_path = raw_input("Give relative path of header files location (e.g headers/): ")
    extension = raw_input("Give extension of header files (e.g .h / .hpp): ")
    output_path = raw_input("Give path to catalog in witch create HTML documentation (e.g output/): ")

    if relative_path[-1:] != "/":
        relative_path += "/"

    if output_path[-1:] != "/":
        output_path += "/"

    if extension[:0] != ".":
        extension = "." + extension
else:
    settings_file = open(".documentator/settings.txt", "r").read().splitlines()
    for line in settings_file:
        if line[:3] == "rel":
            relative_path = line[4:]
        elif line[:3] == "ext":
            extension = line[4:]
        elif line[:3] == "out":
            output_path = line[4:]

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
    save_content += "<p>Name: " + o["name"] + "<br>"
    save_content += "Class: " + o["class"] + "<br>\n"
    save_content += "Description: " + o["description"] + "<br>"
    save_content += "<i>Arguments: " + o["arguments"] + "</i><br>"
    save_content += "<i>Returning: " + o["returns"] + "</i><br></p>"
    save_content += "<hr>"

after_html_file = "</div>" \
                  "</body>" \
                  "</html>"

save_file.write(html_util_content + save_content + after_html_file)

css_file = open(output_path + "styles.css", "w")
css_file.write(css_util_content)

# Independent file for one method
for o in objects:
    independent_file_for_method = open(output_path + o["name"] + ".html", "w")
    to_save = ""
    to_save += "<p>Name: " + o["name"] + "<br>"
    to_save += "Class: " + o["class"] + "<br>\n"
    to_save += "Description: " + o["description"] + "<br>"
    to_save += "<i>Arguments: " + o["arguments"] + "</i><br>"
    to_save += "<i>Returning: " + o["returns"] + "</i><br></p>"
    independent_file_for_method.write(html_util_content + to_save + after_html_file)
    independent_file_for_method.close()

#TODO: Independent file for one class

# Saving methods.html
method = open(output_path + "methods.html", "w")
method_content = ""

for o in objects:
    method_content += "<p><a href='" + o["name"] + ".html'>" + o["class"] + "</a></p>"

method.write(html_util_content + method_content + after_html_file)
method.close()

# Saving classes.html
cls = open(output_path + "classes.html", "w")
cls_content = ""

for o in objects:
    cls_content += "<p><a href='" + o["class"] + ".html'>" + o["class"] + "</a></p>"

cls.write(html_util_content + cls_content + after_html_file)
cls.close()

print("Writing html file completed.")

if not os.path.exists(".documentator/settings.txt") or arg == "new":
    settings_file = open(".documentator/settings.txt", "w")
    settings_file.write("rel " + relative_path + "\n" + "ext " + extension + "\n" + "out " + output_path)
    settings_file.close()
