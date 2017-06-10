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

        if not relative_path.endswith("/"):
            relative_path += "/"

        if not output_path.endswith("/"):
            output_path += "/"

        if extension.startswith("."):
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
                operator = line[line.index("[") + 1:line.index("]")]
                content = line[line.rindex("[") + 1:line.rindex("]")]

                # If name comment was detect
                if operator == "sta" or operator == "start":
                    d = {"name": "", "description": "", "arguments": [], "returns": "", "class": "", "line": ""}
                    objects.append(d)

                # If description comment was detect
                if operator == "dec" or operator == "description":
                    objects[len(objects) - 1]["description"] = content

                # If argument comment was detect
                if operator == "arg" or operator == "argument":
                    argument = dict()
                    argument["name"] = line[line.index("<"):line.index(">")].replace("<", "").replace(">", "")
                    argument["description"] = \
                        content.replace("<", "").replace(">", "").replace("[", "").replace("]", "")
                    objects[len(objects) - 1]["arguments"].append(argument)

                # If returning comment was detect
                if operator == "ret" or operator == "returns":
                    objects[len(objects) - 1]["returns"] = content

                # If class comment was detect
                if operator == "cla" or operator == "class":
                    objects[len(objects) - 1]["class"] = content
            if line.count("//^header") > 0:
                objects[len(objects) - 1]["line"] = line.replace("//^header", "")

    print("Reading files completed.")

    for method in objects:
        n = method["line"].replace("void", "").replace("float", "").replace("int", "").replace("bool", "")
        name = n[:n.index("(")]
        method["name"] = name.strip()

    # Deleting all files in output
    rmtree(output_path)

    # Saving index.html
    makedirs(output_path)
    with open(output_path + "index.html", "w") as index_file:
        save_content = "<h2>All methods with details in the project:</h2>"

        for method in objects:
            save_content += "<br><p><i><div class='code'>" + method["line"] + "</div></i><br>"
            save_content += "Name: " + method["name"] + "<br>"
            if method["class"] != "":
                save_content += "Class: <a href = '" + method["class"] + ".html'>" + method["class"] + "</a><br>\n"
            if method["description"] != "":
                save_content += "Description: " + method["description"] + "<br>"
            if len(method["arguments"]) > 0:
                for argument in method["arguments"]:
                    save_content += "<i>Argument: " + argument["name"] + " - " + argument["description"] + "</i><br>"
            if method["returns"] != "":
                save_content += "<i>Returning: " + method["returns"] + "</i><br></p>"
            save_content += "<hr>"

        index_file.write(before_html + save_content + after_html)
        index_file.close()

    # Saving CSS file
    with open(output_path + "styles.css", "w") as stylesheet_file:
        stylesheet_file.write(stylesheet)

    # Independent file for one method
    for method in objects:
        with open(output_path + method["class"] + "_" +  method["name"] + ".html", "w") as method_file:
            to_save = "<p><i><div class='code'>" + method["line"] + "</div></i><br>"
            to_save += "Name: " + method["name"] + "<br>"
            to_save += "Class: <a href='" + method["class"] + ".html'>" + method["class"] + "</a><br>\n"
            to_save += "Description: " + method["description"] + "<br>"
            if len(method["arguments"]) > 0:
                for argument in method["arguments"]:
                    to_save += "<i>Arguments: " + argument["name"] + " - " + argument["description"] + "</i><br>"
            to_save += "<i>Returning: " + method["returns"] + "</i><br></p>"
            method_file.write(before_html + to_save + after_html)
            method_file.close()

    # Independent files for one class
    classes = []
    for o in objects:
        classes.append(o["class"])

    classes = list(set(classes))

    for clas in classes:
        with open(output_path + clas + ".html", "w") as class_file:
            to_save = "<h2>" + clas + "</h2>"
            for o in objects:
                if o["class"] == clas:
                    to_save += "<p><a href = '" + o["class"] + "_" + o["name"] + ".html'>" + \
                               o["class"] + " : " + o["name"] + "</a></p>"
                    class_file.write(before_html + to_save + after_html)
            class_file.close()

    # Saving classes.html
    with open(output_path + "classes.html", "w") as classes_file:
        class_file_content = "<h2>All classes in the project:</h2>"

        for clas in classes:
            class_file_content += "<p><a href='" + clas + ".html'>" + clas + "</a></p>"

        classes_file.write(before_html + class_file_content + after_html)
        classes_file.close()

    # Saving methods.html
    with open(output_path + "methods.html", "w") as method_file:
        method_content = "<h2>All methods in the project: </h2>"

        for method in objects:
            method_content += "<p><a href='" + method["class"] + "_" + method["name"] + ".html'>" + \
                              method["class"] + " : " + method["name"] + "</a></p>"

        method_file.write(before_html + method_content + after_html)
        method_file.close()

    print("Writing html file completed.")

    if not path.exists(".documentator/settings.txt") or arg == "new":
        with open(".documentator/settings.txt", "w") as settings_file :
            settings_file.write("rel " + relative_path + "\n" + "ext " + extension + "\n" + "out " + output_path)
            settings_file.close()
