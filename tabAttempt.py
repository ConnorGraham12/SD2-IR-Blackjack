import tkinter as tk					
from tkinter import ttk
from tkinter.constants import S
from tkinter.font import Font, nametofont


root = tk.Tk()

#Window Name
root.title("Tab Widget")

customed_style = ttk.Style()
customed_style.configure('Custom.TNotebook.Tab', padding=[12, 12], font=('Helvetica', 20))

#Notebook is basis of tabs 
tabControl = ttk.Notebook(root, style='Custom.TNotebook')

#set Definite sieze for window 
root.wm_geometry("1000x500")

#Makes window not Resizable
root.resizable(False, False)


#Set global font size
default_font = nametofont("TkDefaultFont")
default_font.configure(size = 15)

root.option_add("*Font", default_font)




#Tab names/ Page Frames
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

# Add tabs to bar
tabControl.add(tab1, text ='Welcome')
tabControl.add(tab2, text ='Strategy Charts')
tabControl.add(tab3, text ='LiveFeed')
tabControl.add(tab4, text ='Simulator')

#Packing all tabs
tabControl.pack(expand = 1, fill ="both")

###########################
#						  #
# Welcome page components #
#						  #
###########################

ttk.Label(tab1,
		text ="Creators: \n Connor Graham, John Murphy, Tyler Vandermate, Paul Vicino  ").grid(column = 2,
							row = 4,
							padx = 30,
							pady = 30)
						



##############################
#						     #
# Strategy Charts components #
#						     #
##############################

ttk.Label(tab2,
		text ="Lets dive into the\
		world of computers").grid(column = 0,
									row = 0,
									padx = 30,
									pady = 30)

###########################
#						  #
#   Livefeed components   #
#						  #
###########################

startstream = ttk.Button(tab3, text="Start Livefeed").grid(row =1, column=0)
root.mainloop()
