import tkinter as tk					
from tkinter import Button, StringVar, ttk
from tkinter import font
from tkinter.constants import ANCHOR, S
from tkinter.font import Font, nametofont
#Imported for Images
from PIL import ImageTk, Image
#For mathlib charts
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Import external functions
from test3 import startWebcam


root = tk.Tk()

#Window Name
root.title("SD2 GUI")


#Icon for window
root.iconphoto(False, tk.PhotoImage(file='Resources/favicon2.png'))

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
tab1 = tk.Frame(tabControl)
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
image1 = Image.open('Resources/blackjackLogo.png')
photo1 = ImageTk.PhotoImage(image1.resize((350, 252), Image.ANTIALIAS))
imgLabel1 = ttk.Label(tab1, image= photo1).place(x=300,y=20)

#Lables
ttk.Label(tab1,text ="The ultimate card counting trainer.").place(x=325,y=285)
ttk.Label(tab1,text ="Creators: Connor Graham, John Murphy, Tyler Vandermate, Paul Vicino  ").place(x=200,y=370)

##############################
#						     #
# Strategy Charts components #
#						     #
##############################

image2 = Image.open('Resources/stratchart1.jpg')
photo2 = ImageTk.PhotoImage(image2.resize((330, 402), Image.ANTIALIAS))
imgLabel2 = ttk.Label(tab2, image= photo2).place(x=500,y=10)

###########################
#						  #
#   Livefeed components   #
#						  #
###########################

startstream = ttk.Button(tab3, text="Start Livefeed", command=startWebcam).place(x=400,y=100)

##############################
#						     #
#     Simulator components   #
#						     #
##############################

#MathLib Testing Seciton
data2 = {'Time': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
         'Bankroll': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]}
df2 = DataFrame(data2,columns=['Time','Bankroll'])


figure2 = plt.Figure(figsize=(9,4), dpi=50)
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, tab4)
line2.get_tk_widget().place(x=250, y=225)
df2 = df2[['Time','Bankroll']].groupby('Time').sum()
df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
ax2.set_title('Time Vs. Bankroll')


def simTest():
    print('This button starts the simulator')

#Logic to add instuctional text to entry fields 

#Entry 1
def on_entry_click1(event):
    if entry1.get() == 'Enter starting bankroll...':
       entry1.delete(0, "end") # delete all the text in the entry1
       entry1.insert(0, '') #Insert blank for user input
       entry1.config(fg = 'black')
def on_focusout1(event):
    if entry1.get() == '':
        entry1.insert(0, 'Enter starting bankroll...')
        entry1.config(fg = 'grey')

#Entry 2
def on_entry_click2(event):
    if entry2.get() == 'Enter hands per hour...':
       entry2.delete(0, "end") # delete all the text in the entry2
       entry2.insert(0, '') #Insert blank for user input
       entry2.config(fg = 'black')
       
def on_focusout2(event):
    if entry2.get() == '':
        entry2.insert(0, 'Enter hands per hour...')
        entry2.config(fg = 'grey')

#Entry 3
def on_entry_click3(event):
    if entry3.get() == 'Enter hours played...':
       entry3.delete(0, "end") # delete all the text in the entry3
       entry3.insert(0, '') #Insert blank for user input
       entry3.config(fg = 'black')
       
def on_focusout3(event):
    if entry3.get() == '':
        entry3.insert(0, 'Enter hours played...')
        entry3.config(fg = 'grey')


ttk.Label(tab4,text ="                             Welcome to the Blackjack Counting Simulator! \n This tab will show you longterm results of your bankroll from counting cards \n in Blackjack. If you follow our hi-lo counting method perfectly, you will see \n                                        similar results overtime.").place(x=170,y=20)
input_start_br = StringVar()
input_hand_per_hr = StringVar()
input_hrs_played = StringVar()

entry1 = tk.Entry(tab4, textvariable=input_start_br, takefocus=0)
entry1.place(x=100, y = 140)
entry1.config(fg = 'grey')
entry1.insert(0,'Enter starting bankroll...')
entry1.bind('<FocusIn>', on_entry_click1) 
entry1.bind('<FocusOut>', on_focusout1)

entry2 = tk.Entry(tab4, textvariable=input_hand_per_hr, takefocus=0)
entry2.place(x=350, y = 140)
entry2.config(fg = 'grey')
entry2.insert(0, 'Enter hands per hour...' )
entry2.bind('<FocusIn>', on_entry_click2) 
entry2.bind('<FocusOut>', on_focusout2)

entry3 = tk.Entry(tab4, textvariable=input_hrs_played, takefocus=0)
entry3.place(x=600, y = 140)
entry3.config(fg = 'grey')
entry3.insert(0,'Enter hours played...')
entry3.bind('<FocusIn>', on_entry_click3) 
entry3.bind('<FocusOut>', on_focusout3)



ttk.Button(tab4, text="Go", command=simTest).place(x=400, y = 180)




root.mainloop()
