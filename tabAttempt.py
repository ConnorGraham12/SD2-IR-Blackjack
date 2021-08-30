import tkinter as tk					
from tkinter import ttk


root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)
root.wm_geometry("1000x500")
root.resizable(False, False)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Welcome')
tabControl.add(tab2, text ='Simulator')
tabControl.add(tab3, text ='LiveFeed')

tabControl.pack(expand = 1, fill ="both")

ttk.Label(tab1,
		text ="Arf").grid(column = 0,
							row = 0,
							padx = 30,
							pady = 30)
ttk.Label(tab2,
		text ="Lets dive into the\
		world of computers").grid(column = 0,
									row = 0,
									padx = 30,
									pady = 30)

root.mainloop()
