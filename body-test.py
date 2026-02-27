import gui
from Puzzle import Puzzle

#testing
#print( "TRUE" if wnl().morphy("this".lower()) else "FALSE")

try:
    f = open("intro.txt", "r")
    INSTRUCTIONS = '\n'.join(f.readlines())
except:
    INSTRUCTIONS = "File not read"


THEME = {"bg1"          : "#f0e0d0",
            "highlight"    : "#f94f4f",
            "bg2"          : "#f999a9",
            "accent"       : "#55c5a5"
}


interface = gui.Interface()
root_window = gui.App(interface, INSTRUCTIONS, THEME)
puzzle = Puzzle(interface)
root_window.mainloop()