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
    from xml.etree import ElementTree
    from shutil import rmtree
    from os import makedirs
    from glob import glob
    from os import path

    # Getting path of all files in directory
    dir_path = path.dirname(path.relpath(__file__))

    if not path.exists(".documentator/settings.txt") or arg == "new":
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

    header_glob = glob(dir_path + relative_path + "*" + extension)

    if len(header_glob) < 1:
        print("Error! No files to documentation")
        exit(1)

    if not path.exists(output_path):
        makedirs(output_path)

    # Getting templates from XML
    tree = ElementTree.parse(".documentator/templates.xml")
    before_html = tree.find('before_html').text
    after_html = tree.find('after_html').text
    stylesheet = tree.find('stylesheet').text

    print("Reading templates completed.")

    # Printing content of files
    objects = []
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

    # Deleting all files in output
    rmtree(output_path)

    # Saving final files
    makedirs(output_path)
    save_file = open(output_path + "index.html", "w")
    save_content = ""

    for o in objects:
        save_content += "<p>Name: " + o["name"] + "<br>"
        save_content += "Class: <a href = '" + o["class"] + ".html'>" + o["class"] + "</a><br>\n"
        save_content += "Description: " + o["description"] + "<br>"
        save_content += "<i>Arguments: " + o["arguments"] + "</i><br>"
        save_content += "<i>Returning: " + o["returns"] + "</i><br></p>"
        save_content += "<hr>"

    save_file.write(before_html + save_content + after_html)

    css_file = open(output_path + "styles.css", "w")
    css_file.write(stylesheet)

    # Independent file for one method
    for o in objects:
        independent_file_for_method = open(output_path + o["name"] + ".html", "w")
        to_save = "<p>Name: " + o["name"] + "<br>"
        to_save += "Class: " + o["class"] + "<br>\n"
        to_save += "Description: " + o["description"] + "<br>"
        to_save += "<i>Arguments: " + o["arguments"] + "</i><br>"
        to_save += "<i>Returning: " + o["returns"] + "</i><br></p>"
        independent_file_for_method.write(before_html + to_save + after_html)
        independent_file_for_method.close()

    # Saving classes
    class_file = open(output_path + "classes.html", "w")
    class_file_content = ""

    for o in objects:
        class_file_content += "<p><a href='" + o["class"] +".html'>" + o["class"] + "</a></p>"

    class_file.write(before_html + class_file_content + after_html)
    class_file.close()

    # Saving methods.html
    method = open(output_path + "methods.html", "w")
    method_content = ""

    for o in objects:
        method_content += "<p><a href='" + o["name"] + ".html'>" + o["class"] + " : " + o["name"] + "</a></p>"

    method.write(before_html + method_content + after_html)
    method.close()

    print("Writing html file completed.")

    if not path.exists(".documentator/settings.txt") or arg == "new":
        settings_file = open(".documentator/settings.txt", "w")
        settings_file.write("rel " + relative_path + "\n" + "ext " + extension + "\n" + "out " + output_path)
        settings_file.close()
