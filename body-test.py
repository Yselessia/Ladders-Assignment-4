from nltk.stem import WordNetLemmatizer as wnl
import csv#
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

class Player():
    def __init__(self, player_details:dict):
        self._id = player_details["id"]
        if "name" in player_details:
            self._name = player_details["name"]
        else:
            self._name = self.get_word()
            #clearing screen animation goes here
    def get_id(self):
        return self._id
    def get_word(self, length:int=None):
        #test
        print("enter word")
        iw = input()
        if length:
            while len(iw) != length:
                iw=input()
        return iw
    def win(self, score):
        #test
        print(f"you win. score is {score}")
    def scores(self):
        pass

class Puzzle():
    def __init__(self, player:Player, target:str=None, start:str=None):
        self._player = player
        if target and start:
            self._init_load(target, start)
        else:
            self._init_input()

    def _init_load(self, target, start):
        if len(target) != len(start):
            self._player.error(code=1)  #fix this
            self._init_input()
        else:
            self._target = target
            self._len = len(self._target)
            self._word_route = [start]
    def _init_input(self):
        self._target = self._player.get_word()
        self._len = len(self._target)
        start = self._player.get_word(length=self._len)
        self._word_route = [start]
    
        
    def _rules(self,prev,word):
        match = 0
        for i in range(self._len):
            if word[i]==prev[i]:
                match+=1
        if match == self._len-1:
            return True

    def _english(self, word):
         if wnl().morphy(word):
              return True
         
    def _skip_back_to(self, word):
        self._word_route = self._word_route[0:self._word_route.index(word)+1]
        #deleting animation here

    def user_turn(self):
        while not exit:
            print(self._word_route)
            word = self._player.get_word(length=self._len)
            if self._rules(self._word_route[-1], word):
                if word == self._target:
                    self._word_route.append(word)
                    self.score = len(self._word_route)-2 #fix this
                    self._player.win(self.score)

                    exit=True
                else:
                    if word in self._word_route:
                        self._skip_back_to(word)
                    elif self._english(word):
                        self._word_route.append(word)
                    else:
                        pass #fix this  -   invalid_word() 

#test - working test
player1 = Player({"greet":"hiya", "name":"Ruben", "id":1})
puzzle1 = Puzzle(player1, start="meat", target="book")
puzzle1.user_turn()