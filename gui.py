import tkinter as tk
from tkinter import ttk

try:
    from ctypes import windll
    windll.shcore.SetProcessDPiAwareness(1)
except:
    pass

    
     
root = tk.Tk()

root.title("SD2 GUI") 
root.geometry("1000x500")
root.resizable(width=False, height=False)

# nav = ttk.Frame(root)
# nav.pack(side="left")

button1 = ttk.Button(root, text="test", padding=10)
button1.place(x=5,y=10)

button2 = ttk.Button(root, text="test2", padding=10)
button2.place(x=5,y=70)

button3 = ttk.Button(root, text="test", padding=10)
button3.place(x=5,y=140)


root.mainloop()
