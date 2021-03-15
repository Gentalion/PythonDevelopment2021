import tkinter as tk
from tkinter import messagebox
import random

N = 4
puzzle_name = str(N * N - 1) + "puzzle"
DEFAULT_HEIGHT = 5
DEFAULT_WIDTH = 10

class Puzzle (tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title(puzzle_name)
        self.control_frame = tk.Frame(self)
        self.puzzle_frame = tk.Frame(self)
        self.puzzle_buttons = []
        self.new_game()
        #self.new_game(setup = [i for i in range(1,15)] + [0, 15])
        
    def is_solvable(self):
        inversions = 0
        for i in range(N * N):
            for j in range(i, N * N):
                if self.positions[j] == 0:
                    continue
                if self.positions[i] > self.positions[j]:
                    inversions += 1
        print("inversions=" +str(inversions) + ", blank row=" + str(self.blank["row"]))
        if N % 2 == 0:
            if self.blank["row"] % 2 == 0:
                return inversions % 2 != 0
            else:
                return inversions % 2 == 0
        else:
            return inversions % 2 == 0
            
    def check_winning(self):
        for i in range(N * N - 1):
            if self.positions[i] != i + 1:
                return False
        return True
    
    def new_game(self, setup=None):
        if not setup:
            self.positions = [i for i in range(N * N)] # 0 as empty space
        else:
            print("setup" + str(setup))
            self.positions = setup
        while True:
            if not setup:
                random.shuffle(self.positions)
            blank = self.positions.index(0)
            self.blank = {"index": blank, "col": blank % N, "row": blank // N}
            if self.is_solvable() and not self.check_winning():
                break
            if setup:
                print("bad setup")
                setup = None
        self.rebuild_buttons()
    
    def rebuild_buttons(self):
        for button in self.puzzle_buttons:
            button.destroy()
        self.puzzle_buttons = []
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.control_frame.grid_columnconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure(1, weight=1)
        
        self.control_frame.grid(row=0, column=0, sticky='NESW')
        self.puzzle_frame.grid(row=1, column=0, sticky='NESW')
        
        new_button = tk.Button(self.control_frame, text="new", command=self.new_game)
        exit_button = tk.Button(self.control_frame, text = "exit", command=self.quit)
        
        new_button.grid(column=0, row=0)
        exit_button.grid(column=1, row=0)
        
        for i in range(N):
            self.puzzle_frame.grid_columnconfigure(i, weight=1)
            self.puzzle_frame.grid_rowconfigure(i, weight=1)
        
        for i in range(N * N):
            n = self.positions[i]
            if n != 0:
                self.puzzle_buttons.append(tk.Button(self.puzzle_frame, text=str(n), height=DEFAULT_HEIGHT, width=DEFAULT_WIDTH, command=self.move_button_func(n)))
                self.puzzle_buttons[-1].grid(column=(i % N), row=(i // N), sticky="NESW")
                #print(f"Added button #{n}")
        
    
    def move_button_func(this, n):
        def move_button(self=this):
            idx = self.positions.index(n)
            col = idx % N
            row = idx // N
            if abs(self.blank["col"] - col) + abs(self.blank["row"] - row) != 1:
                return
            
            self.positions[idx] = 0
            self.positions[self.blank["index"]] = n
            self.blank = {"index": idx, "col": col, "row": row}
            if self.check_winning():
                self.rebuild_buttons()
                messagebox.showinfo(puzzle_name, 'You won!')
                self.new_game()
            self.rebuild_buttons()
        return move_button
        
puzzle = Puzzle()
puzzle.mainloop()