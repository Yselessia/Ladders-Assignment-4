import tkinter as tk
from tkinter import ttk

# -----------------------------
# CONFIG
# -----------------------------
theme_colours = {}
theme_colours["bg1"] = "#f0e0d0"
BOX_SIZE = 50                  # Square input box size
DEFAULT_COLUMNS = 4            # Boxes per row
DEFAULT_ROWS = 1               # Number of rows


#https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
#make a 
class RoundedFrame(tk.Canvas):
    """a rounded frame canvas covering most app level styling"""
    def __init__(self, parent, radius=25, bg=theme_colours["bg1"], **kwargs):
        super().__init__(parent, bg=bg, highlightthickness=0, **kwargs)
        self.radius = radius
        self.bg = bg

        # Create rounded rectangle
        self.rounded = self.create_round_rectangle(60, 50, 150, 100)

        # Internal frame for widgets
        self.inner = tk.Frame(self, bg=bg)
        self.create_window((0, 0), window=self.inner, anchor="nw")

        self.bind("<Configure>", self.resize)

    def create_round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def resize(self, event):
        w, h = event.width, event.height
        self.coords(self.rounded, 0, 0, w, h)
        self.itemconfig(self.rounded, width=0)


# -----------------------------
# MAIN APPLICATION
# -----------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu + Game GUI")
        self.geometry("900x700")
        self.configure(bg=theme_colours["bg1"])

        self.game_screen()
    

    def game_screen(self):
        self.clear()
        frame = RoundedFrame(self, radius=40, bg=theme_colours["bg1"])
        frame.pack()#(expand=True, fill="both", padx=40, pady=40)

        title = tk.Label(frame.inner, text="Game", font=("Arial", 20), bg=theme_colours["bg1"])
        title.pack(pady=10)

        # Container for the dynamic grid
        self.grid_container = tk.Frame(frame.inner, bg=theme_colours["bg1"])
        self.grid_container.pack(pady=20)

        # Build initial grid
        self.build_grid(DEFAULT_ROWS, DEFAULT_COLUMNS)


    def build_grid(self, rows, cols):
        """Rebuilds the grid with given rows/cols."""
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        self.rows = rows
        self.cols = cols
        self.entries = []

        for r in range(rows):
            row_entries = []
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
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Center the grid
        self.grid_container.update_idletasks()
        self.grid_container.pack()

    def limit_char(self, new_value):
        return len(new_value) <= 1

    def add_row(self):
        self.build_grid(self.rows + 1, self.cols)

    def add_column(self):
        self.build_grid(self.rows, self.cols + 1)

    # -------------------------
    # UTILITY
    # -------------------------
    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()






if __name__ == "__main__":
    root = App()
    #root.overrideredirect(True) # remove window border 
    root.config(bg="pink") 
    root.wm_attributes("-transparentcolor", "pink")
    # ^ makes bg transparent and non-interactable, allows for custom window shape
    # ^ needs more finesse to consistently use the window menu bar (i.e. drag, close, minimise/maximise)
    root.mainloop()
