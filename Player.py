class Player():
    """No uses"""

    def __init__(self, player_details:dict):
        """Initialises class with player details: unique id, name,"""
        self._id = player_details["id"]
        if "name" in player_details:
            self._name = player_details["name"]
        else:
            self._name = self.get_word()
            #clearing screen animation goes here

    def get_id(self):
        return self._id
    def change_nickname(self, new_name): #do not remove
        pass