import glob
import os

import object

# Getting path of all files in directory
dir_path = os.path.dirname(os.path.relpath(__file__))

print("Give relative path of header files location (e.g headers/):")
relative_path = input()

print("Give extension of header files (e.g .h / .hpp):")
extension = input()
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
save_file = open("index.html", "w+")
save_content = ""

html_file = "<DOCTYPE html>" \
            "<html lang='en'>" \
            "<head>" \
            "<meta charset='utf-8'>" \
            "<title>Documenator page</title>" \
            "</head>" \
            "<body>"

for o in objects:
    save_content += "<p>\nName: " + o.nam + "<br>\n"
    save_content += "Class: " + o.cla + "<br>\n"
    save_content += "Description: " + o.des + "<br>\n"
    save_content += "Arguments: " + o.arg + "<br>\n"
    save_content += "Returning: " + o.ret + "<br>\n</p>\n"

after_html_file = "</body>" \
                  "</html>"

save_file.write(html_file + save_content + after_html_file)
print("Writing html file completed.")