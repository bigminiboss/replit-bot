import os
import sys
from typing import Dict, Callable as Function, Any


def __base_check_for_files(
    checker: Function[..., Any], folder: str = "replit_bot"
) -> Dict[str, int]:
    __temp = sys.getrecursionlimit()
    sys.setrecursionlimit(10**6)
    output = 0
    file_paths = {}
    for i in os.walk(folder):
        parent = i[0]
        for j in i[-1]:
            if j.endswith(".py") or j.endswith(".html"):
                current = checker(parent + "/" + j)  #
                output += current
                file_paths[parent + "/" + j] = current
    sys.setrecursionlimit(__temp)
    return file_paths, output


def get_lines(folder: str = "replit_bot") -> Dict[str, int]:
    __temp = __base_check_for_files(lambda x: len(open(x).read().split("\n")), folder)
    __temp[0]["totalNumberOfLines"] = __temp[1]
    return __temp[0]


def get_chars(folder: str = "replit_bot") -> Dict[str, int]:
    __temp = __base_check_for_files(lambda x: len(open(x).read()), folder)
    __temp[0]["totalNumberOfChars"] = __temp[1]
    return __temp[0]
