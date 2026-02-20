import gui#, csv, Files, Player 
from nltk.stem import WordNetLemmatizer as wnl
from Puzzle import Puzzle
"""
puzzle_id,player_id,target,start,hiscore,attempts
"""
ERRORS = {1:"file is corrupted", 2:"file not found"}
#FILENAME = "ladders_hiscore.txt" #.csv, reader = csv.reader(f)
 #try:with open(FILENAME,'r') as f:
puzzle = {"words":{"meat","book"}, "hiscore":3, "player_id":1, "attempts":1}
DEFAULT_COLUMNS = 4      

"""def save_puzzle(self):
    puzzle_dict = {}
    word_route = ["a","b","c"]
    score = len(word_route)-2
    puzzle_dict["words"]={word_route[0],word_route[-1]}
    if "hiscore" in puzzle_dict:
        if puzzle_dict["hiscore"] < score:
            puzzle_dict["hiscore"] = score
    #puzzle_dict["player_id"]=self.*.get_id()"""

#test - working test

interface1 = gui.Interface()
root_window = gui.App(interface1)
puzzle1 = Puzzle(interface1)
root_window.mainloop()