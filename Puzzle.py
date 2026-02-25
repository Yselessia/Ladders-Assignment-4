from gui import Interface
from nltk.stem import WordNetLemmatizer as wnl

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

#   ------------
# INTERACTION WITH APP
#   ------------

    def set_target(self, word:str):
        self._target = word
        self._len = len(self._target) # = DEFAULT_COLUMNS
        self._interactions.state = "get_start"
        self._interactions.print("Enter starting word.")

    def set_start(self, word:str):
        self._word_route = [word]
        self._interactions.state = "new_turn"
        self._interactions.print("")
 
    def _skip_back_to(self, word):
        """If a player enters a word that has already been used, 
        this deletes the guesses since then  - 
        decreasing distance from start"""
        index = self._word_route.index(word)
        self._word_route = self._word_route[:index + 1]
        self._interactions.skip_back(index)
    
#   ------------
# VALIDATION CHECKS
#   ------------

    def _match_int(self,prev,word):
        """Returns integer representing the number of matching letters between two words"""
        match = 0
        for i in range(self._len):
            if word[i]==prev[i]:
                match+=1
        return match

    def _rules(self,prev,word):
        """Checks that exactly one letter has been changed from the previous word"""
        if self._match_int(prev, word) == self._len-1:
            return True
        return False

    def _english(self, word):
        """Uses nltk function to check if it's a valid English word"""
        #Morphy checks to find a valid English lemma (root word) for the input, 
        # else returns None
        # must be lowercase
        if wnl().morphy(word.lower()):
            return True
    
#   ------------
# GAME TURN
#   ------------

    def user_turn(self, word:str):
        """Represents one turn of the game: input, validation check, win condition/continue check"""

        #validation check
        if not self._rules(self._word_route[-1], word):
            self._interactions.print("You need to change one letter, and keep all the other letters the same")
            self._skip_back_to(self._word_route[-1])

        # 2nd validation check
        elif not self._english(word):
            #invalid word - test
            self._interactions.print("Oops! I don't think that that's a real word")
            self._skip_back_to(self._word_route[-1])

        #win condition check
        elif word == self._target:
            self._word_route.append(word) #if u remove this, change score calculation as well
            
            #calculates score as (number of turns) minus (minimum number of turns to win)
            score = (len(self._word_route) - 2) - (self._len - self._match_int(self._word_route[0], self._target))
            
            self._interactions.state = "win"
            self._interactions.win(score=score, start=self._word_route[0], target=self._target)
        
        #for a valid move that's not the win condition, 
        # checks if the word has already been used
        elif word in self._word_route:
            self._interactions.print("I suppose you want to move backwards?")
            self._skip_back_to(word)
        
        #otherwise, adds the turn and continues.
        else:
            self._word_route.append(word)
            self._interactions.print("") #clears text
