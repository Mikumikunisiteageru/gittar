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

def push_in(filename):
    subdir = os.path.join(".gittar", filename) + "^"
    if os.path.isdir(subdir):
        shutil.rmtree(subdir)
    os.mkdir(subdir)
    with zipfile.ZipFile(filename) as zip_file:
        for file in zip_file.namelist():
            print(file)
            zip_file.extract(file, subdir)
            try_expand_xml(os.path.join(subdir, file))

def pull_out(filename):
    subdir = os.path.join(".gittar", filename + "^", "")
    assert os.path.isdir(subdir)
    with zipfile.ZipFile(filename, mode="w") as zip_file:
        for path, dnames, fnames in os.walk(subdir):
            fpath = path.replace(subdir, "")
            print(path, dnames, fnames, fpath)
            for fname in fnames:
                zip_file.write(os.path.join(path, fname), os.path.join(fpath, fname))

def run_git(command):
    if not os.path.isdir(".gittar"):
        assert not os.path.isfile(".gittar")
        os.mkdir(".gittar")
    os.chdir(".gittar")
    os.system(f"git {command}")
    os.chdir("..")
