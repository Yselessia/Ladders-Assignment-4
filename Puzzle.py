from gui import Interface
DEFAULT_COLUMNS = 4            # Boxes per row

class Puzzle():
    """Handles the gameplay logic/rules for a game."""

    def __init__(self, interface:Interface):
        """Initialises class with interactions object, sets callbacks for this to get input/set other properties"""
        self._interactions = interface
        #to register callback functions
        callbacks = {
                "get_start": self.set_start
                ,"get_target": self.set_target
                ,"new_turn": self.user_turn
        }
        self._interactions.set_callbacks(callbacks)
        self._interactions.state = "get_target"

    def set_target(self, word:str):
        self._target = word
        self._len = len(self._target) # = DEFAULT_COLUMNS
        self._interactions.state = "get_start"
    def set_start(self, word:str):
        self._word_route = [word]
        self._interactions.state = "new_turn"
 
    def _rules(self,prev,word):
        """Checks that exactly one letter has been changed from the previous word"""
        match = 0
        #match represents the # of letters which match between the words
        for i in range(self._len):
            if word[i]==prev[i]:
                match+=1
        if match == self._len-1:
            return True

    def _english(self, word):
        """Uses nltk function to check if it's a valid English word"""
        #Morphy checks to find a valid English lemma (root word) for the input, 
        # else returns None
        if wnl().morphy(word):
            return True
         
    def _skip_back_to(self, word):
        """If a player enters a word that has already been used, 
        this deletes the guesses since then  - 
        decreasing distance from start"""
        self._word_route = self._word_route[0:self._word_route.index(word)+1]
        #deleting animation here
        #self._interactions.*("?") 
        

    def user_turn(self, word:str):
        """Represents one turn of the game: input, validation check, win condition/continue check"""

        #validation check
        if not self._rules(self._word_route[-1], word):
            self._interactions.print("You need to change one letter, and keep all the other letters the same")
        
        # 2nd validation check
        elif self._english(word):
            #invalid word - test
            self._interactions.print("Oops! I don't think that that's a real word")
            self._skip_back_to(self._word_route[-1])

        #win condition check
        elif word == self._target:
            self._word_route.append(word)
            self.score = len(self._word_route)-2 #better scoring system?
            self._interactions.win(self.score)
            self._interactions.state = "win"
        
        #for a valid move that's not the win condition, 
        # checks if the word has already been used
        elif word in self._word_route:
            self._skip_back_to(word)
        
        #otherwise, adds the turn and continues.
        else:
            self._word_route.append(word)
