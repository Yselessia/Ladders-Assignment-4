class Puzzle():
    """Handles the gameplay logic/rules for a game."""

    def __init__(self, player:Player, target:str=None, start:str=None):
        """Initialises class with player object, calls \_init_*() function to set other properties"""
        self._player = player
        if target and start:
            self._init_load(target, start)
        else:
            self._init_input()

    def _init_load(self, target, start):
        """Uses parameters to """
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
