from textnode import TextNode, TextType
from functions import *
import os


# copy_directory kopiert alle Dateien und Unterverzeichnisse von src nach dst, wobei dst vorher gelöscht wird, wenn es bereits existiert
def main():
    src = "static"
    dst = "public"
    copy_directory(src, dst)

if __name__ == "__main__":
    main()