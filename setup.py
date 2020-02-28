import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "pygame"], "excludes": ["tkinter"], "include_files":["lol_winrates"]}


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "LoL Tierlist Tool",
        version = "1.0",
        description = "View Tierlist",
        options = {"build_exe": build_exe_options}, 
        executables = [Executable("run.py", base=base, shortcutName="LoL Tierlist Tool", shortcutDir="DesktopFolder",icon = 'lol_winrates/res/icon.ico')])