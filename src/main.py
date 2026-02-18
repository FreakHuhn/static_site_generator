import sys
from tempfile import template
from textnode import TextNode, TextType
from functions import *
import os


template_path = "template.html"
# copy_directory kopiert alle Dateien und Unterverzeichnisse von src nach dst, wobei dst vorher gelöscht wird, wenn es bereits existiert
# Update your main.py to build the site into the docs directory instead of public. GitHub pages serves sites from the docs directory of your main branch by default.

def main():
    src = "static"
    dst = "docs"
    copy_directory(src, dst)
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    generate_pages_recursive("content" , "template.html", "docs", basepath)

if __name__ == "__main__":
    main()

