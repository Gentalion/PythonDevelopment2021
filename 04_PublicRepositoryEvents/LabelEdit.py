import tkinter as tk
import tkinter.font as tkFont

class InputLabel(tk.Label):
    def __init__(self, master=None):
        self.text = tk.StringVar(value='')
        super().__init__(master, textvariable=self.text, takefocus=True, highlightthickness=1, anchor="w")
        self.font = tkFont.Font(font=self['font'])
        self.font.configure(family='Courier', size=10)
        self['font'] = self.font
        self.size = self.font.measure("a")
        self.cursor = tk.Frame(self, height=16, width=1, background="black")
        self.bind("<Key>", self.manageCursor)
        self.bind("<Button-1>", self.placeCursor)
        self.cursorPos = 0
        
    def updateCursorPos(self, newPos):
        self.cursorPos = min(max(newPos, 0), len(self.text.get()))
        self.cursor.place(x=self.size * self.cursorPos, y=1)
    
    def manageCursor(self, event):
        def addSymbol(key):
            if key == "space":
                key = " "
            elif not key.isalnum() or not len(key) == 1:
                return
            text = self.text.get()
            self.text.set(text[:self.cursorPos] + key + text[self.cursorPos:])
            self.updateCursorPos(self.cursorPos + 1)
            
        def removeSymbol(key):
            text = self.text.get()
            self.text.set(text[:self.cursorPos][:-1] + text[self.cursorPos:])
            self.updateCursorPos(self.cursorPos - 1)
        
        def goOneSymbolLeft(key):
            self.updateCursorPos(self.cursorPos - 1)
        
        def goOneSymbolRight(key):
            self.updateCursorPos(self.cursorPos + 1)
        
        def goLeftmostPlace(key):
            self.updateCursorPos(0)
        
        def goRightmostPlace(key):
            self.updateCursorPos(len(self.text.get()))
        
        cases = {"BackSpace": removeSymbol, "Left": goOneSymbolLeft, "Right": goOneSymbolRight, "Up": goLeftmostPlace, "Home": goLeftmostPlace, "Down": goRightmostPlace, "End": goRightmostPlace}
        
        cases.get(event.keysym, addSymbol)(event.keysym)
    
    def placeCursor(self, event):
        self.focus()
        self.updateCursorPos(event.x // self.size)

win = tk.Tk()
win.title("LabelEdit")

label = InputLabel(win)
label.grid(row=0, sticky="NESW")

quitButton = tk.Button(win, text="Quit", command=win.destroy)
quitButton.grid(row=1, sticky="W")

win.mainloop()