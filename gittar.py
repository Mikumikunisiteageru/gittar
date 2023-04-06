# gittar.py

import codecs
import os
import shutil
import sys
import zipfile
import xml.dom.minidom

def try_expand_xml(filename):
    try:
        with codecs.open(filename, "r", "utf-8") as f:
            xml_obj = xml.dom.minidom.parse(f)
        xml_str = xml_obj.toprettyxml()
        with codecs.open(filename, "w", "utf-8") as f:
            f.write(xml_str)
    except:
        pass

def try_compact_xml(filename):
    try:
        with codecs.open(filename, "r", "utf-8") as f:
            xml_obj = xml.dom.minidom.parse(f)
        xml_str = xml_obj.toxml().replace("\t", "").replace("\n", "")
        with codecs.open(filename, "w", "utf-8") as f:
            f.write(xml_str + "\n")
    except:
        pass

def encode_string(string, zip=True):
    new_string = string.replace("^", "^^")
    if zip:
        new_string += "^"
    return new_string

def decode_string(string):
    l = len(string)
    i = l - 1
    while i >= 0 and string[i] == '^':
        i -= 1
    j = l - i - 1
    if j & 1 == 1:
        zip = True
        return string[:l-1].replace("^^", "^"), True
    else:
        return string.replace("^^", "^"), False

def push_in(filename, zip=True):
    if zip:
        subdir = os.path.join(".gittar", encode_string(filename, True))
        if os.path.isdir(subdir):
            shutil.rmtree(subdir)
        os.mkdir(subdir)
        with zipfile.ZipFile(filename) as zip_file:
            for file in zip_file.namelist():
                zip_file.extract(file, subdir)
                try_expand_xml(os.path.join(subdir, file))
    else:
        subfile = os.path.join(".gittar", encode_string(string, False))
        shutil.copy(filename, subfile)

def pull_out(filename):
    subdir = os.path.join(".gittar", encode_string(filename, True), "")
    assert os.path.isdir(subdir)
    with zipfile.ZipFile(filename, mode="w") as zip_file:
        for path, dnames, fnames in os.walk(subdir):
            fpath = path.replace(subdir, "")
            for fname in fnames:
                zip_file.write(os.path.join(path, fname), os.path.join(fpath, fname), zipfile.ZIP_DEFLATED)

def run_git(command):
    if not os.path.isdir(".gittar"):
        assert not os.path.isfile(".gittar")
        os.mkdir(".gittar")
    os.chdir(".gittar")
    os.system(f"git {command}")
    os.chdir("..")

if __name__ == "__main__":
    if len(sys.argv) >= 2: 
        if sys.argv[1] in ["add", "diff"]:
            assert len(sys.argv) >= 3
            filename = sys.argv[2]
            assert os.path.isfile(filename)
            push_in(filename, zipfile.is_zipfile(filename))
            sys.argv[2] = "."
        elif sys.argv[1] in []:
            pass
    run_git(' '.join(f'"{s}"' for s in sys.argv[1:]))
