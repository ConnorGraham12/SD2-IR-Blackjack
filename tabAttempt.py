import tkinter as tk					
from tkinter import ttk
from tkinter.constants import S
from tkinter.font import Font, nametofont
from PIL import ImageTk, Image

#Import external functions
from test3 import startWebcam


root = tk.Tk()

#Window Name
root.title("SD2 GUI")


#Icon for window
root.iconphoto(False, tk.PhotoImage(file='favicon2.png'))

style = ttk.Style()
style.configure('TNotebook.Tab', padding=[20, 12], font=('Helvetica', 20))



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
tabControl.pack(expand = 1, fill ="both", anchor='center')
# root.wm_attributes('-alpha', 0.7) 

###########################
#						  #
# Welcome page components #
#						  #
###########################

#Logo
image1 = Image.open('blackjackLogo.png')
photo = ImageTk.PhotoImage(image1.resize((350, 252), Image.ANTIALIAS))
imgLabel = ttk.Label(tab1, image= photo).place(x=300,y=20)

#Lables
ttk.Label(tab1,text ="The Ultimate card counting trainer.").place(x=330,y=275)
ttk.Label(tab1,text ="Creators: Connor Graham, John Murphy, Tyler Vandermate, Paul Vicino  ").place(x=200,y=350)

##############################
#						     #
# Strategy Charts components #
#						     #
##############################



###########################
#						  #
#   Livefeed components   #
#						  #
###########################

startstream = ttk.Button(tab3, text="Start Livefeed", command=startWebcam).place(x=500,y=250)
root.mainloop()
