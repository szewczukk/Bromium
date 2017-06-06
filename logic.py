from xml.etree import ElementTree
from shutil import rmtree
from os import makedirs
from glob import glob
from os import path


def logic(arg):
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
            if line[:1] == "^":
                operator_start = line.index("[") + 1
                operator_end = line.index("]")

                operator = line[operator_start:operator_end]

                content_start = line.rindex("[") + 1
                content_end = line.rindex("]")

                content = line[content_start:content_end]

                # If name comment was detect
                if operator == "nam" or operator == "name":
                    objects.append({"name": "", "description": "", "arguments": [], "returns": "", "class": "", "line": ""})
                    objects[len(objects) - 1]["name"] = content

                # If description comment was detect
                if operator == "dec" or operator == "description":
                    objects[len(objects) - 1]["description"] = content

                # If argument comment was detect
                if operator == "arg" or operator == "argument":
                    argument = {"name": "", "description": ""}
                    start = line.index("<")
                    end = line.index(">")
                    argument["name"] = line[start:end].replace("<", "").replace(">", "")
                    argument["description"] = content.replace("<", "").replace(">", "").replace("[", "").replace("]", "")
                    objects[len(objects) - 1]["arguments"].append(argument)

                # If returning comment was detect
                if operator == "ret" or operator == "returns":
                    objects[len(objects) - 1]["returns"] = content

                # If class comment was detect
                if operator == "cla" or operator == "class":
                    objects[len(objects) - 1]["class"] = content
            if line.count("//header") > 0:
                objects[len(objects) - 1]["line"] = line.replace("//header", "")

    print("Reading files completed.")

    # Deleting all files in output
    rmtree(output_path)

    # Saving index.html
    makedirs(output_path)
    save_file = open(output_path + "index.html", "w")
    save_content = "<h2>All methods with details in the project:</h2>"

    for o in objects:
        save_content += "<br><p><i><div class='code'>" + o["line"] + "</div></i><br>"
        save_content += "Name: " + o["name"] + "<br>"
        save_content += "Class: <a href = '" + o["class"] + ".html'>" + o["class"] + "</a><br>\n"
        if o["description"] != "":
            save_content += "Description: " + o["description"] + "<br>"
        if len(o["arguments"]) > 0:
            for argument in o["arguments"]:
                save_content += "<i>Argument: " + argument["name"] + " - " + argument["description"] + "</i><br>"
        if o["returns"] != "":
            save_content += "<i>Returning: " + o["returns"] + "</i><br></p>"
        save_content += "<hr>"

    save_file.write(before_html + save_content + after_html)

    css_file = open(output_path + "styles.css", "w")
    css_file.write(stylesheet)

    # Independent file for one method
    for o in objects:
        independent_file_for_method = open(output_path + o["class"] + "_" +  o["name"] + ".html", "w")
        to_save = "<p><i><div class='code'>" + o["line"] + "</div></i><br>"
        to_save += "Name: " + o["name"] + "<br>"
        to_save += "Class: <a href='" + o["class"] + ".html'>" + o["class"] + "</a><br>\n"
        to_save += "Description: " + o["description"] + "<br>"
        if len(o["arguments"]) > 0:
            for a in o["arguments"]:
                to_save += "<i>Arguments: " + a["name"] + " - " + a["description"] + "</i><br>"
        to_save += "<i>Returning: " + o["returns"] + "</i><br></p>"
        independent_file_for_method.write(before_html + to_save + after_html)
        independent_file_for_method.close()

    # Independent files for one class
    classes = []
    for o in objects:
        classes.append(o["class"])

    classes = list(set(classes))

    for c in classes:
        independent_file_for_class = open(output_path + c + ".html", "w")
        to_save = "<h2>" + c + "</h2>"
        for o in objects:
            if o["class"] == c:
                to_save += "<p><a href = '" + o["class"] + "_" + o["name"] + ".html'>" + o["class"] + " : " + o["name"] + "</a></p>"
        independent_file_for_class.write(before_html + to_save + after_html)
        independent_file_for_class.close()

    # Saving classes.html
    class_file = open(output_path + "classes.html", "w")
    class_file_content = "<h2>All classes in the project:</h2>"

    for c in classes:
        class_file_content += "<p><a href='" + c + ".html'>" + c + "</a></p>"

    class_file.write(before_html + class_file_content + after_html)
    class_file.close()

    # Saving methods.html
    method = open(output_path + "methods.html", "w")
    method_content = "<h2>All methods in the project: </h2>"

    for o in objects:
        method_content += "<p><a href='" + o["class"] + "_" + o["name"] + ".html'>" + o["class"] + " : " + o["name"] + "</a></p>"

    method.write(before_html + method_content + after_html)
    method.close()

    print("Writing html file completed.")

    if not path.exists(".documentator/settings.txt") or arg == "new":
        settings_file = open(".documentator/settings.txt", "w")
        settings_file.write("rel " + relative_path + "\n" + "ext " + extension + "\n" + "out " + output_path)
        settings_file.close()
