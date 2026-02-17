class Interface():
    """Handles interaction with the user/GUI."""
    
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