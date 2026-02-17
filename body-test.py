from nltk.stem import WordNetLemmatizer as wnl
import csv
import Player, Puzzle, Files
"""
puzzle_id,player_id,target,start,hiscore,attempts
"""
ERRORS = {1:"file is corrupted", 2:"file not found"}
#FILENAME = "ladders_hiscore.txt" #.csv, reader = csv.reader(f)
 #try:with open(FILENAME,'r') as f:
puzzle = {"words":{"meat","book"}, "hiscore":3, "player_id":1, "attempts":1}

"""def save_puzzle(self):
    puzzle_dict = {}
    word_route = ["a","b","c"]
    score = len(word_route)-2
    puzzle_dict["words"]={word_route[0],word_route[-1]}
    if "hiscore" in puzzle_dict:
        if puzzle_dict["hiscore"] < score:
            puzzle_dict["hiscore"] = score
    #puzzle_dict["player_id"]=self._player.get_id()"""

#test - working test
player1 = Player({"greet":"hiya", "name":"Ruben", "id":1})
puzzle1 = Puzzle(player1, start="meat", target="book")
puzzle1.user_turn()