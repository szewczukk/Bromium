import glob
import os

# Getting path of all files in directory
dir_path = os.path.dirname(os.path.relpath(__file__))

print("Give relative path of header files location (e.g headers/):")
relative_path = input()

print("Give extension of header files (e.g .h / .hpp):")
extension = input()
header_glob = glob.glob(dir_path + relative_path + "*" + extension)

# Printing content of files
for file in header_glob:
    print("\nFrom: " + file + "\n")
    f = open(file, 'r').read().splitlines()
    for line in f:
        line = line.strip()
        if line[:2] == "//":
            operator = line[2:7]
            if operator == "[nam]":
                print("Name:", line[8:len(line)-1])
            if operator == "[des]":
                print("Description:", line[8:len(line)-1])
            if operator == "[arg]":
                print("Argument")
            if operator == "[ret]":
                print("Argument")
