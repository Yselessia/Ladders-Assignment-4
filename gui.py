import tkinter as tk
from tkinter import Entry, Label
from typing import Callable
from TkGifWidget import AnimatedGif #add to main
# -----------------------------
# CONFIG
# -----------------------------
theme_colours = {}
theme_colours["bg1"] = "#f0e0d0"
theme_colours["highlight"] = "#020202"
theme_colours["bg2"] = "#f999a9"
theme_colours["accent"] = "#55c5a5"
BOX_SIZE = 50                  # Square input box size
DEFAULT_COLUMNS = 4            # Boxes per row
INSTRUCTIONS = ""

class Interface():
    """Handles interaction with the user/GUI."""
    def __init__(self, ):
        self.word_length = 4
        self._callbacks = {}
        self.state = ""

    def set_callbacks(self, callbacks:dict[str, Callable]):
        """Updates dictionary with callback functions"""
        self._callbacks.update(callbacks)

    def submit(self, new_word:str):
        """Passes a string to the Puzzle class"""
        self._callbacks[self.state](new_word)

    def print(self, message:str):
        """Passes a string to the App class"""
        self._callbacks["output"](message)
    def skip_back(self,row:int):
        """Deletes rows from App class"""
        self._callbacks["skip_back"](row)
    def win(self, score:int, start:str, target:str):
        """Switches App class to victory screen"""
        self._callbacks["win"](str(score))
    def reset_game(self):
        """Resets state to reinitialise puzzle properties. Calls game screen from App"""
        self.state = "get_target"
        self._callbacks["restart"]()

class CharEntry(Entry):
    def disable_entry(self):
        self.configure(state="disabled", disabledbackground=theme_colours["bg1"])

class App(tk.Tk):
    def __init__(self, interface:Interface, instructions:str):
        super().__init__()
        self.title("LLLL")
        self.geometry("540x600") #should be 800x600?

        self._interface = interface
        self._output = tk.StringVar()
        callbacks = {
                "output":self._output.set
                ,"skip_back":self.skip_back_to
                ,"win":self.win_screen
                ,"restart":self.game_screen
                     }
        self._interface.set_callbacks(callbacks)
        self.intro_screen(instructions)
    
#   ------------
# CLEARING THE SCREEN
#   ------------

    def clear(self):
        """Destroys all widgets"""
        for widget in self.winfo_children():
            widget.destroy()

#   ------------
# APP ACTIVITIES
#   ------------

    def win_screen(self, score:str="Unknown"):
        self.clear()
        canvas = tk.Canvas(self, bg=theme_colours["bg1"], highlightthickness=0)
        canvas.pack(expand=True, fill="both", padx=40, pady=40)
        title = tk.Label(canvas, text="Victory!", font=("Arial", 20), bg=theme_colours["bg1"])
        title.pack(pady=10)
        if score == "0":
            win_message = f"You got a perfect score!\n Your score is 0."
        else:
            win_message = f"Your score was: {score}! Nice!\nPlay again to get closer to 0"

        label_output = tk.Label(canvas, text=win_message, font=("Arial", 12,"bold"), bg=theme_colours["accent"])
        label_output.pack(pady=10)

        # Create a celebratory GIF widget
        confetti = AnimatedGif(file_path='confetti.gif', play_mode='hover', loop=1)
        confetti.pack(fill="x")
        play_button = tk.Button(canvas, text="New Game", command=self._interface.reset_game, bg=theme_colours["accent"])
        play_button.pack(pady=10) #fix padding later !!

    def intro_screen(self, instructions:str):
        """Builds a canvas with instructions and button to progress to new game"""        
        self.clear()
        self.configure(bg=theme_colours["bg2"])
        canvas = tk.Canvas(self, bg=theme_colours["bg2"], highlightthickness=0)
        canvas.pack(expand=True, fill="both", padx=40, pady=40)
   
        title = tk.Label(canvas, text="How to Play", font=("Arial", 20), bg=theme_colours["bg2"])
        title.pack(pady=10)

        label_output = tk.Label(canvas, text=instructions, font=("Arial", 12,"bold"), bg=theme_colours["bg2"], wraplength=400)
        label_output.pack(pady=10)

        play_button = tk.Button(canvas, text="New Game", command=self.game_screen, bg=theme_colours["accent"])#, fg=theme_colours["bg1"])
        play_button.pack(pady=10) #fix padding later !!

    def game_screen(self):
        """Builds a canvas with gameplay visuals and interactables"""        
        self.clear()
        self.configure(bg=theme_colours["bg1"])
        canvas = tk.Canvas(self, bg=theme_colours["bg1"], highlightthickness=0)
        canvas.pack(expand=True, fill="both", padx=40, pady=40)

        title = tk.Label(canvas, text="Ladders", font=("Arial", 20), bg=theme_colours["bg1"])
        title.pack(pady=10)

        label_output = tk.Label(canvas, textvariable=self._output, font=("Arial", 12,"bold"), bg=theme_colours["highlight"])
        label_output.pack(pady=10)
        
        # Container for the dynamic grid
        self.grid_container = tk.Frame(canvas, bg=theme_colours["bg1"])
        self.grid_container.pack(pady=20)

        # Build initial grid of char entry-boxes
        self.build_grid(DEFAULT_COLUMNS)

#   ------------
# CREATING THE ENTRYBOX GRID
#   ------------

    def build_grid(self, cols:int):
        """Rebuilds the grid with given x y """
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        self.rows = 0
        self.cols = cols
        self.entries = []           #list of words

        self.add_row(0)
        #move this
        self.grid_container.update_idletasks()
        self.grid_container.pack()

    def regrid(self, r:int):
        """Inserts to tkinter grid only the new inserted row and the last row."""
        # Re-grid the newly inserted row
        for c, entry in enumerate(self.entries[r]):
            entry.grid(row=r, column=c)
        # Re-grid the row that was pushed down
        if self.rows > 1:
            for c, entry in enumerate(self.entries[r + 1]):
                entry.grid(row=r + 1, column=c)

    def add_column(self):
        pass
    
    def add_row(self, r:int):
        """Create a new row at index r"""
        self.rows += 1  

        row_entries = []        #represents one word (list of letters)
        
        #creates row as list of widgets
        for c in range(self.cols):
            entry = CharEntry(self.grid_container, width=2, font=("Arial", 20), justify="center")
            #entry.grid(row=r, column=c, padx=5, pady=5, ipadx=10, ipady=10)
            entry.config(validate="key")
            #entry['validatecommand'] = (entry.register(self.limit_char), "%P")

            # auto-advance binding
            entry.bind("<KeyPress>", lambda e, rr=r, cc=c: self.on_key(e, rr, cc))
            row_entries.append(entry)

        self.entries.insert(r, row_entries)
        #adds widgets to window
        self.regrid(r)
        #set focus
        self.entries[r][0].focus_set()          

#   ------------
# CHANGING THE GRID
#   ------------

    def disable_row(self,row:int):
        for c in self.entries[row]:
            c.disable_entry()

    def insert_row(self):
        """Inserts row to the penultimate grid position and disables prev entrys"""
        #the number of rows is incremented,
        # a new row is added between the focus and the target word (last row),
        # and the previous row is disabled (cannot be typed in)
        r = self.rows - 1 #r will be inserted to the last row index (moving the last row to r+1)
        if r == 0:
            self.disable_row(r)
        else:
            self.disable_row(r - 1) #disables the penultimate row
        self.add_row(r)

    def skip_back_to(self, row:int=0):
        """Deletes rows until it encounters given index. 
        The row with given index is not deleted. 
        The last row is not deleted.
        A new row is inserted after the given index and before the last row"""
        while self.rows > row + 2:
            self.remove_row(self.rows - 2)

    def remove_row(self, row:int):
        """Removes a row with given index"""
        self.rows -= 1
        for widget in self.entries[row]:
            widget.destroy()
        del self.entries[row]

#   ------------
# USER INTERACTIONS
#   ------------

    def on_key(self, event, row:int, col:int):
        """When keys pressed, moves cursor to next entrybox. 
        Calls Interface.submit  if enter key <RETURN> is pressed"""
        key = event.keysym

        entry = self.entries[row][col]
        if key == "Return":
            #concatenates row into a string and passes it to interface submit
            new_word = ''.join(i.get() for i in self.entries[row])
            if len(new_word) == self._interface.word_length:
                self._interface.submit(new_word)

                #creates new row to continue the game
                if not self._interface.state == "win":
                    self.insert_row()  
                
        #Move to prev column on backspace
        # - never move to previous row
        # - only move if the widget is empty
        elif key == "BackSpace":
            if col > 0 and entry.get() == "":
                col -= 1
            self.entries[row][col].focus_set()          #set focus
            self.entries[row][col].delete(0, tk.END)    #clear widget
        
        #If key is not backspace,
        # move forward when an alphabetical character is typed
        # and always enforce a single character
        else:
            #clear widget - incase of very speedy typing! or slow execution ig
            entry.delete(0, tk.END)     
            #insert character if its a letter
            if event.char.isalpha():
                entry.insert(0,event.char.upper())
            #finally, move cursor if it can move on and the box is filled
            if col + 1 < self.cols and self.entries[row][col].get():
                self.entries[row][col + 1].focus_set()

        #tells tkinter the keypress has already been handled
        return "break" 

        


