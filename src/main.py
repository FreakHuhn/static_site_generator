from tempfile import template
from textnode import TextNode, TextType
from functions import *
import os

template_path = "template.html"
# copy_directory kopiert alle Dateien und Unterverzeichnisse von src nach dst, wobei dst vorher gelöscht wird, wenn es bereits existiert
def main():
    src = "static"
    dst = "public"
    copy_directory(src, dst)
    generate_pages_recursive("content" , "template.html", "public")
    

if __name__ == "__main__":
    main()