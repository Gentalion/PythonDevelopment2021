import tkinter as tk
import re
import random
from functools import partial

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.text_editor = CanvasTextEditor(self, undo=True, wrap=tk.WORD)
        self.text_editor.grid(row=0, column=0, sticky="news")

        self.canvas = CustomCanvas(self)
        self.canvas.grid(row=0, column=1, sticky="news")

class CanvasTextEditor(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tag_configure("error", background="red")
        self.bind("<KeyRelease>", self.update_canvas)
        
    def log_new_object(self, object_type, x1, y1, x2, y2, fill_color, outline_color):
        obj_info = {
            "type": object_type,
            "coord": (x1, y1, x2, y2),
            "fill_color": fill_color,
            "outline_color": outline_color
        }
        
        self.insert(
            tk.END,
            f"{object_type} {[x1, y1, x2, y2]} {fill_color} {outline_color} \n"
        )
    
    def change_text(self, tag, x1, y1, x2, y2):
        if tag == "":
            return
        cur = self.get(f"{tag}.0", f"{int(tag) + 1}.0")
        s = cur.find("[")
        e = cur.find("]")
        cur = cur[:s] + f"{[x1, y1, x2, y2]}" + cur[e+1:]
        self.delete(f"{tag}.0", f"{int(tag) + 1}.0")
        self.insert(f"{tag}.0", cur)
    
    def update_canvas(self, event):
        tag = int(self.index(tk.INSERT)[:1])
        cur = self.get(f"{tag}.0", f"{int(tag) + 1}.0")
        line_format = r"(?P<object_type>oval) (?P<coords>\[[0-9. ,]*\]) (?P<fill_color>\#[0-9a-f]*) (?P<outline_color>\#[0-9a-f]*)"
        #line_format = r"(?P<object_type>oval) (?P<coords>\[[0-9.]*\])"
        try:
            m = re.match(line_format, cur)
            if not m:
                raise Exception("Format exception")
            object_type, coords, fill_color, outline_color = m.group("object_type"), eval(m.group("coords")), m.group("fill_color"), m.group("outline_color")
            self.master.canvas.coords(tag, coords[0], coords[1], coords[2], coords[3])
            self.master.canvas.itemconfig(tag, fill=fill_color, outline=outline_color)
            self.tag_delete(f"red{tag}.0{int(tag) + 1}.0")
        except Exception as e:
            #print(e)
            self.tag_add(f"red{tag}.0{int(tag) + 1}.0", f"{tag}.0", f"{int(tag) + 1}.0")
            self.tag_configure(f"red{tag}.0{int(tag) + 1}.0", background="red")

class CustomCanvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_object = None
        self.current_moving_object = None
        self.bind("<Button-1>", self.click)
        self.bind("<Button1-Motion>", self.motion)
        self.bind("<ButtonRelease-1>", self.release)
        
    def click(self, event):
        overlap = self.find_overlapping(event.x, event.y, event.x, event.y)
        if overlap:
            return
        self.new_object(event.x, event.y)
        
    def release(self, event):
        self.current_moving_object = None
        self.current_object = None
    
    def new_object(self, x, y):
        self.current_start = (x, y)
        current_fill = "#%06x" % random.randint(0, 16581374)
        current_outline = "#%06x" % random.randint(0, 16581374)
        self.current_object = self.create_oval(x, y, x, y, fill=current_fill, outline=current_outline)
        self.master.text_editor.log_new_object("oval", x, y, x, y, current_fill, current_outline)
        self.tag_bind(self.current_object, "<Button-1>", partial(self.click_object, self.current_object))
    
    def click_object(self, tag, event):
        self.current_moving_object = tag
        self.current_object_coords = self.coords(tag)
        self.current_object_start = event.x, event.y
        self.current_obj = ""
        self.tag_bind(tag, "<Button1-Motion>", partial(self.move_object, tag))
    
    def move_object(self, tag, event):
        x1, y1, x2, y2 = self.current_object_coords
        sx, sy = self.current_object_start
        dx = event.x - sx
        dy = event.y - sy

        w, h = self.winfo_width(), self.winfo_height()
        if x1 + dx >= 0 and x2 + dx <= h and y1 + dy >= 0 and y2 + dy <= w:
            self.coords(tag, x1 + dx, y1 + dy, x2 + dx, y2 + dy)
            self.master.text_editor.change_text(tag, int(x1 + dx), int(y1 + dy), int(x2 + dx), int(y2 + dy))
    
    def motion(self, event):
        if self.current_moving_object:
            return
        self.coords(self.current_object, *self.current_start, event.x, event.y)
        self.master.text_editor.change_text(self.current_object, *self.current_start, event.x, event.y)
        
app = Application()
app.mainloop()