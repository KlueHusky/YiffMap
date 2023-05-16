#!/usr/bin/env python

# 29.04.2023
# YiffMap V4.0

from colorama import Fore
from sys import argv
from tools import Map, check_arguments


SPLASH_SCREEN = """
YiffMap V4.0
Made by Klue
"""



def main():
    # Check arguments
    check_arguments(argv)
    data_file = argv[1]
    output_file = argv[2]

    print(SPLASH_SCREEN)
    # 1) Initialisation...
    map = Map(data_file, True)
    # 2) Check the contents of the file
    map.check_file_contents()
    # 3) Display statistics
    map.display_stats()
    # 4) Create the graph
    map.graph(output_file, labels='--no-labels' not in argv)
    


if __name__ == '__main__':
    main()