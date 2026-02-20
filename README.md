# Ladders Assignment 4
"word ladders" puzzle game

# 19th Feb
Linked input and output of puzzle and app classes
Couldn't commit via github as i have no wifi to login to my git account, so saved to my OneDrive.

# AI use
https://copilot.microsoft.com/shares/41bvbwcqKaunBxa1m5pPy

^does not exist. how long does a share link last...? oops.
Used Copilot to generate a tkinter gui with a grid on entry-boxes

https://copilot.microsoft.com/shares/admTpDkm1qXsR4BWynohq
my prompt: *can the cursor move to the next box after one character has been typed? and then we return the full word (one letter per box) `multiple functions from previous ai-generated code`*

https://copilot.microsoft.com/shares/7T7pAemmn9MGcywEzNnQc
my prompt: *why isn't this working? `code snippet`*

response: If you want full control, you must:
*    Bind to KeyPress, not KeyRelease
*    Handle the key yourself
*    Return `"break"` to stop Tkinter from doing its own insert/delete
    Here’s the corrected pattern:
    ...

https://copilot.microsoft.com/shares/kz6jwrtVQVSfoRkMPjM7k
my prompt: *what method do i use to add a row without clearing the text from the entry widgets?* 
```
def add_row(self):
        self.build_grid(self.rows + 1, self.cols)
def build_grid()...
```

response: copilot suggested moving the widget creation loop into the add_row function. I copied the code, but changed the logic for row index as it was bugging

https://copilot.microsoft.com/shares/Z4LgWFEnYPVPxWV6SXNau
asked copilot about control flow logic, provided code snippets from `on_key()` and `Puzzle` class (`word = self._interactions.get_word(length=self._len)`)

https://copilot.microsoft.com/shares/Vx6x6hLi5sQwtihR6ekVz
asked copilot about callback functions: *my word processing is equivalent to a user turn. would i put             `self._interactions.on_submit(self.user_turn)` at the end of the user_turn function? will this mess with memory limit/callstack*

essentials of response: The call stack doesn’t grow (callbacks aren’t recursive), but the number of registered listeners does (...)
You just let user_turn handle the game state:
```
def user_turn(self, word):
    if self.state == "waiting_for_guess":
        self.handle_guess(word)
    elif self.state == "waiting_for_confirmation":
        self.handle_confirmation(word)
    # etc.
```
I implemented the suggestions, keeping the majority of logic in user_turn but adding a function to handle user input -\*