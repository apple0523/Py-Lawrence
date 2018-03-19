# -*- coding:utf-8 -*-

import sys
from cx_Freeze import setup,Executable

import os

os.environ['TCL_LIBRARY'] = r"C:\Program Files\Python36\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Program Files\Python36\tcl\tk8.6"

include_files = [
    r"C:\Program Files\Python36\DLLs\tcl86t.dll",
    r"C:\Program Files\Python36\DLLs\tk86t.dll"
]

build_exe_options = {
    "packages":["os","tkinter"],
    "include_files":include_files
}

base = None

if sys.platform == "win64":
    base = "Win64GUI"

setup(name = "fanyitools",
    version = "0.1",
    description = "fanyitools!",
    options = {"build_exe":build_exe_options},
    executables = {Executable("windows.py",base=base)}
    )