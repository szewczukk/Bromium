from xml.etree import ElementTree
from shutil import rmtree
from os import makedirs
from glob import glob
from os import path


def logic(arg):
    # Getting path of all files in directory
    dir_path = path.dirname(path.relpath(__file__))

    relative_path = ""
    extension = ""
    output_path = ""

    if not path.exists(".bromine/settings.txt") or arg == "new":
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
        settings_file = open(".bromine/settings.txt", "r").read().splitlines()
        for line in settings_file:
            if line.startswith("rel"):
                relative_path = line[line.index(":") + 1:]
            elif line.startswith("ext"):
                extension = line[line.index(":") + 1:]
            elif line.startswith("out"):
                output_path = line[line.index(":") + 1:]

    header_glob = glob(dir_path + relative_path + "*" + extension)

    if len(header_glob) < 1:
        print("Error! No files to documentation")
        exit(1)

    if not path.exists(output_path):
        makedirs(output_path)

    # Getting templates from XML
    tree = ElementTree.parse(".bromine/templates.xml")
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
            if line.startswith("^"):
                operator = line[line.index("[") + 1:line.index("]")]
                content = line[line.rindex("[") + 1:line.rindex("]")]

                # If name comment was detect
                if operator == "nam" or operator == "name":
                    d = {"name": "", "description": "", "arguments": [], "returns": "", "class": "", "line": ""}
                    objects.append(d)
                    objects[len(objects) - 1]["name"] = content

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

    # Deleting all files in output
    rmtree(output_path)

    # Saving index.html
    template = tree.find("method_template").text
    makedirs(output_path)
    with open(output_path + "index.html", "w") as index_file:
        save_content = "<h2>All methods with details in the project:</h2>"

        for obj in objects:
            args = ""
            if len(obj["arguments"]) > 0:
                for argument in obj["arguments"]:
                    args += tree.find("argument_template").text.format(name=argument["name"],
                                                                       description=argument["description"])
                save_content += template.format(line=obj["line"], name=obj["name"], cla=obj["class"],
                                                description=obj["description"], arg=args, returns=obj["returns"])

        index_file.write(before_html + save_content + after_html)
        index_file.close()

    # Saving CSS file
    with open(output_path + "styles.css", "w") as stylesheet_file:
        stylesheet_file.write(stylesheet)
        stylesheet_file.close()

    # Independent file for one method
    template = tree.find("method_template").text
    for method in objects:
        args = ""
        with open(output_path + method["class"] + "_" + method["name"] + ".html", "w") as method_file:
            if len(method["arguments"]) > 0:
                for argument in method["arguments"]:
                    args += tree.find("argument_template").text.format(name=argument["name"],
                                                                       description=argument["description"])
            to_save = template.format(line=method["line"], name=method["name"], cla=method["class"],
                                      description=method["description"], returns=method["returns"], arg=args)

            method_file.write(before_html + to_save + after_html)
            method_file.close()

    # Independent files for one class
    classes = []
    for obj in objects:
        classes.append(obj["class"])

    classes = list(set(classes))

    template = tree.find("class_template").text
    for cla in classes:
        with open(output_path + cla + ".html", "w") as class_file:
            to_save = "<h2>" + cla + "</h2>"
            for obj in objects:
                if obj["class"] == cla:
                    to_save += template.format(cla=obj["class"], name=obj["name"])
                    class_file.write(before_html + to_save + after_html)
            class_file.close()

    # Saving classes.html
    template = tree.find("classes_template").text
    with open(output_path + "classes.html", "w") as classes_file:
        class_file_content = "<h2>All classes in the project:</h2>"

        for cla in classes:
            class_file_content += template.format(cla=cla)

        classes_file.write(before_html + class_file_content + after_html)
        classes_file.close()

    # Saving methods.html
    template = tree.find("class_template").text
    with open(output_path + "methods.html", "w") as method_file:
        method_content = "<h2>All methods in the project: </h2>"

        for method in objects:
            method_content += template.format(cla=method["class"], name=method["name"])

        method_file.write(before_html + method_content + after_html)
        method_file.close()

    print("Writing html file completed.")

    if not path.exists(".bromine/settings.txt") or arg == "new":
        with open(".bromine/settings.txt", "w") as settings_file:
            settings_file.write("rel :" + relative_path + "\n" + "ext :" + extension + "\n" + "out :" + output_path)
            settings_file.close()
