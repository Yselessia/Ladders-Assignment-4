import gui#, csv, Files, Player 
from nltk.stem import WordNetLemmatizer as wnl
from Puzzle import Puzzle
"""
puzzle_id,player_id,target,start,hiscore,attempts
"""
ERRORS = {1:"file is corrupted", 2:"file not found"}
#FILENAME = "ladders_hiscore.txt" #.csv, reader = csv.reader(f)
 #try:with open(FILENAME,'r') as f:
DEFAULT_COLUMNS = 4      

try:
    f = open("intro.txt", "r")
    INSTRUCTIONS = '\n'.join(f.readlines())
except:
    INSTRUCTIONS = "File not read"

#test - working test

interface1 = gui.Interface()
root_window = gui.App(interface1, INSTRUCTIONS)
puzzle1 = Puzzle(interface1)
root_window.mainloop()