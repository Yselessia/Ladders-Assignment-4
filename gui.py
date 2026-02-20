import tkinter as tk
from tkinter import Entry, Label
from typing import Callable

# -----------------------------
# CONFIG
# -----------------------------
theme_colours = {}
theme_colours["bg1"] = "#f0e0d0"
theme_colours["highlight"] = "#ff4f4f"
BOX_SIZE = 50                  # Square input box size
DEFAULT_COLUMNS = 4            # Boxes per row

class Interface():
    """Handles interaction with the user/GUI."""
    def __init__(self, ):
        self.word_length = 4
        self._callbacks = {}
        self.state = "" #should initialise this properly

    def set_callbacks(self, callbacks:dict[str, Callable]):
        self._callbacks.update(callbacks) #appends new callback mappings to dict

    def submit(self, new_word:str):
        """Passes a string to the Puzzle class"""
        print(self.state)
        self._callbacks[self.state](new_word)
    def print(self, message:str):
        """Passes a string to the App class"""
        self._callbacks["output"](message)
        
    def get_word(self, length:int=0):
        #testing
        print("enter word")
        iw = input()
        if length>0:
            while len(iw) != length:
                iw=input()
        return iw
    
    def win(self, score):
        print(f"you win. score is {score}")






class CharEntry(Entry):
    def disable_entry(self):
        self.configure(state="disabled", disabledbackground=theme_colours["bg1"])

class App(tk.Tk):
    def __init__(self, interface:Interface):
        super().__init__()
        self.title("LLLL")
        self.geometry("900x700")
        self.configure(bg=theme_colours["bg1"])

        self._interface = interface
        self._output = tk.StringVar()
        self._interface.set_callbacks({"output":self._output.set})

        self.game_screen()

    def game_screen(self):
        """Builds a canvas with gameplay visuals and interactables"""
        self.clear()
        canvas = tk.Canvas(self, width=400, height=400, bg=theme_colours["bg1"], highlightthickness=0)
        canvas = tk.Canvas(self)
        canvas.pack(expand=True, fill="both", padx=40, pady=40)

        title = tk.Label(canvas, text="MMMM", font=("Arial", 20), bg=theme_colours["bg1"])
        title.pack(pady=10)

        label_output = tk.Label(canvas, textvariable=self._output, font=("Arial", 12,"bold"), highlightcolor=theme_colours["highlight"], bg=theme_colours["bg1"])
        label_output.pack(pady=10)
        
        # Container for the dynamic grid
        self.grid_container = tk.Frame(canvas, bg=theme_colours["bg1"])
        self.grid_container.pack(pady=20)

        # Build initial grid of char entry-boxes
        self.build_grid()

    def build_grid(self, rows:int=1, cols:int=DEFAULT_COLUMNS):
        """Rebuilds the grid with given x y """
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        self.rows = rows
        self.cols = cols
        self.entries = []           #list of words

        for r in range(rows):
              self.add_row(r)

    def disable_row(self,row:int):
        for c in self.entries[row]:
            c.disable_entry()

    def add_row(self, r:int=-1):
        # r is the index of the new row in the grid
        # if a new row is added after grid creation, the number of rows is incremented
        # and the previous row is disabled (cannot be typed in)
        if r < 0:
            r = self.rows
            self.rows += 1 
            self.disable_row(r - 1)

        row_entries = []        #represents one word (list of letters)
        for c in range(self.cols):
            entry = CharEntry(self.grid_container, width=2, font=("Arial", 20), justify="center")
            entry.grid(row=r, column=c, padx=5, pady=5, ipadx=10, ipady=10)
            entry.config(validate="key")
            #entry['validatecommand'] = (entry.register(self.limit_char), "%P")

            # auto-advance binding
            #r = row (as in for loop); c, ditto
            entry.bind("<KeyPress>", lambda e, r=r, c=c: self.on_key(e, r, c))
            row_entries.append(entry)

        self.entries.append(row_entries)

        #should this move?
        # Center the grid
        self.grid_container.update_idletasks()
        self.grid_container.pack()

    def add_column(self):
        pass

    """
    def limit_char(self, new_value:str):
       is this used
        return len(new_value) <= 1"""

    def on_key(self, event, row:int, col:int):
        """When keys pressed, moves cursor to next entrybox. 
        Calls function []  if enter key <RETURN> is pressed"""
        entry = self.entries[row][col]
        key = event.keysym

        if key == "Return":
            #concatenates row into a string and passes it to interface submit
            new_word = ''.join(i.get() for i in self.entries[row])
            if len(new_word) == self._interface.word_length:
                self._interface.submit(new_word)
                self.add_row()                              #create new row
                self.entries[row+1][0].focus_set()          #set focus
                
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

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()








if __name__ == "__main__":
    root = App(Interface())
    #root.overrideredirect(True) # remove window border 
    #root.config(bg="pink") 
    #root.wm_attributes("-transparentcolor", "pink")
    # ^ makes bg transparent and non-interactable, allows for custom window shape
    # ^ needs more finesse to consistently use the window menu bar (i.e. drag, close, minimise/maximise)
    root.mainloop()
