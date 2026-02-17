class Player():
    """Handles interaction with the user/GUI."""
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


"""def save_puzzle(self):
    puzzle_dict = {}
    word_route = ["a","b","c"]
    score = len(word_route)-2
    puzzle_dict["words"]={word_route[0],word_route[-1]}
    if "hiscore" in puzzle_dict:
        if puzzle_dict["hiscore"] < score:
            puzzle_dict["hiscore"] = score
    #puzzle_dict["player_id"]=self._player.get_id()"""

