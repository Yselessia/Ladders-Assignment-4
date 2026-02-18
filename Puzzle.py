class Puzzle():
    """Handles the gameplay logic/rules for a game."""

    def __init__(self, interface, target:str="", start:str=""):
        """Initialises class with interactions object, calls \_init_*() function to set other properties"""
        self._interactions = interface
        if target and start:
            self._init_load(target, start)
        else: 
            #if the start and target words were not both given
            self._init_input()

    def _init_load(self, target, start):
        """Uses parameters to set start and end (target) words"""
        if len(target) != len(start):
            #all words must be the same length - otherwise there's an error.
            self._interactions.error(code=1)  #fix this
            self._init_input()
        else:
            self._target = target
            self._len = len(self._target)
            self._word_route = [start]
    def _init_input(self):
        """Uses interactions class to get start and end (target) words"""
        self._target = self._interactions.get_word()
        self._len = len(self._target)
        start = self._interactions.get_word(length=self._len)
        self._word_route = [start]
    
        
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

    def user_turn(self):
        """Each loop represents one turn of the game: input, validation check, win condition/continue check"""
        #I originally used recursion, but changed to a loop as it's better to avoid memory limitations
        
        while not exit: # type: ignore
            print(self._word_route) #testing
            #gets input of correct length
            word = self._interactions.get_word(length=self._len)
            #validation check
            if self._rules(self._word_route[-1], word):
                #if user has changed 1 letter, checks if the target word is reached
                if word == self._target:
                    self._word_route.append(word)
                    self.score = len(self._word_route)-2 #fix this
                    self._interactions.win(self.score)

                    exit=True
                else:
                    #for a valid move that's not the win condition, 
                    # checks if the word has already been used
                    if word in self._word_route:
                        self._skip_back_to(word)
                    #if not,
                    # 2nd validation check - tests if the new word to be added is a real word
                    elif self._english(word):
                        self._word_route.append(word)
                    else:
                        pass #fix this  -   invalid_word() 
