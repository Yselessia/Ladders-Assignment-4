import tkinter as tk

# -----------------------------
# CONFIG
# -----------------------------
theme_colours = {}
theme_colours["bg1"] = "#f0e0d0"
BOX_SIZE = 50                  # Square input box size
DEFAULT_COLUMNS = 4            # Boxes per row
WORD_LEN = 4                   #**boxes per row

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MMMM")
        self.geometry("900x700")
        self.configure(bg=theme_colours["bg1"])

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
                entry.bind("<KeyRelease>", lambda e, r=r, c=c: self.on_key(e, r, c))
                row_entries.append(entry)
            self.entries.append(row_entries)
            

        # Center the grid
        self.grid_container.update_idletasks()
        self.grid_container.pack()


    def on_key(self, event, row:int, col:int):
        """When keys pressed, moves cursor to next entrybox"""
        entry = self.entries[row][col]
        key = event.keysym
        text = entry.get()

        if key == "Return":
            pass

        elif key == "BackSpace":

            # --- Move backward on Backspace ---
            if text == "":
                #Previous column
                # never move to previous row
                if col > 0:
                    col -= 1
                self.entries[row][col].focus_set()
                self.entries[row][col].delete(0, tk.END)

        
        #If key is not backspace,
        # move forward when a character is typed
        # and always enforce a single character
        else: 
            while len(text) > 1:
                #delete any extra characters
                entry.delete(1, tk.END)
                text = text[1:]

                #if this is the last widget in the row
                # or the next is not empty (end coordinate = 0),
                if col + 1 == self.cols or self.entries[row][col + 1].index("end") > 0:
                    # replace the character with the last key hit and exit the loop
                    entry.insert(text[-1])
                    break

                else:
                    #if there is an available blank widget
                    #insert remaining extra text to blank widget
                    self.entries[row][col + 1].insert(0,text)
                    col +=1
            #finally, move cursor
            if col + 1 < self.cols:
                self.entries[row][col + 1].focus_set()
            

    def limit_char(self, new_value):
        return len(new_value) <= WORD_LEN

    def add_row(self):
        self.build_grid(self.rows + 1, self.cols)

    def add_column(self):
        """used when setting up game"""
        self.build_grid(self.rows, self.cols + 1)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()







if __name__ == "__main__":
    root = App()
    #root.overrideredirect(True) # remove window border 
    #root.config(bg="pink") 
    #root.wm_attributes("-transparentcolor", "pink")
    # ^ makes bg transparent and non-interactable, allows for custom window shape
    # ^ needs more finesse to consistently use the window menu bar (i.e. drag, close, minimise/maximise)
    root.mainloop()
