class FileSession():
    """?"""
    def load_puzzle(self):


    def save_puzzle(self):
        puzzle_dict = {}
        word_route = ["a","b","c"]
        score = len(word_route)-2
        puzzle_dict["words"]={word_route[0],word_route[-1]}
        if "hiscore" in puzzle_dict:
            if puzzle_dict["hiscore"] < score:
                puzzle_dict["hiscore"] = score
        #puzzle_dict["player_id"]=self._player.get_id()"""

class E2():