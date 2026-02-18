import tkinter as tk
import re

# -----------------------------
# CONFIG
# -----------------------------
theme_colours = {}
theme_colours["bg1"] = "#f0e0d0"
BOX_SIZE = 50                  # Square input box size
DEFAULT_COLUMNS = 4            # Boxes per row
WORD_LEN = 4                   #**boxes per row

class Interface():
    """Handles interaction with the user/GUI."""
    
    def get_word(self, length:int=0):
        #test
        print("enter word")
        iw = input()
        if length>0:
            while len(iw) != length:
                iw=input()
        return iw
    def win(self, score):
        #test
        print(f"you win. score is {score}")
    def scores(self):
        pass

class App(tk.Tk):
    def __init__(self, interface:Interface):
        super().__init__()
        self.title("LLLL")
        self.geometry("900x700")
        self.configure(bg=theme_colours["bg1"])

        self.interface = interface
        self.game_screen()
    

    def game_screen(self):
        """Builds a canvas with gameplay visuals and interactables"""
        self.clear()
        canvas = tk.Canvas(self, width=400, height=400, bg=theme_colours["bg1"], highlightthickness=0)
        canvas = tk.Canvas(self)
        canvas.pack()#(expand=True, fill="both", padx=40, pady=40)

        title = tk.Label(canvas, text="MMMM", font=("Arial", 20), bg=theme_colours["bg1"])
        title.pack(pady=10)

        # Container for the dynamic grid
        self.grid_container = tk.Frame(canvas, bg=theme_colours["bg1"])
        self.grid_container.pack(pady=20)

        # Build initial grid of char entry-boxes
        self.build_grid(1, DEFAULT_COLUMNS)


    def build_grid(self, rows, cols):
        """Rebuilds the grid with given x y """
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        self.rows = rows
        self.cols = cols
        self.entries = []           #list of words

        
        for r in range(rows):
            row_entries = []        #represents one word (list of letters)
            for c in range(cols):
                entry = tk.Entry(
                    self.grid_container,
                    width=2,
                    font=("Arial", 20),
                    justify="center"
                )
                entry.grid(row=r, column=c, padx=5, pady=5, ipadx=10, ipady=10)
                entry.config(validate="key")
                entry['validatecommand'] = (entry.register(self.limit_char), "%P")

                # auto-advance binding
                #r = row (as in for loop); c, ditto
                entry.bind("<KeyPress>", lambda e, r=r, c=c: self.on_key(e, r, c))
                row_entries.append(entry)
            self.entries.append(row_entries)
            
        # Center the grid
        self.grid_container.update_idletasks()
        self.grid_container.pack()


    def on_key(self, event, row:int, col:int):
        """When keys pressed, moves cursor to next entrybox. 
        Calls function []  if enter key <RETURN> is pressed"""
        entry = self.entries[row][col]
        key = event.keysym

        if key == "Return":
            pass #needs to call function

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

    def limit_char(self, new_value):
        return len(new_value) <= WORD_LEN

    def add_row(self):
        self.build_grid(self.rows + 1, self.cols)

    def add_column(self):
        """used when setting up new game"""
        self.build_grid(self.rows, self.cols + 1)

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
