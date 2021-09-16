import tkinter as tk					
from tkinter import Button, StringVar, ttk
from tkinter import font
from tkinter.constants import ANCHOR, S
from tkinter.font import Font, nametofont
import webbrowser  

#Imported for Images
from PIL import ImageTk, Image

#For mathlib charts
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Import external functions
from test3 import startWebcam
from test3 import finished


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
tab1 = tk.Frame(tabControl, bg='#696969')
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
ttk.Label(tab1,text ="Creators: Connor Graham, John Murphy, Tyler Vandermate, Paul Vicino, Graham West  ").place(x=150,y=370)

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

if(finished == 1):
    print("FINSIHED")
##############################
#						     #
#     Simulator components   #
#						     #
##############################
def openWebsite():
    webbrowser.open("https://sd1-blackjack.herokuapp.com/login?next=%2F", new=0, autoraise=True)



#MathPlotLibData
#MathLib Testing Seciton
data2 = {'Time': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
         'Bankroll': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]}
df2 = DataFrame(data2,columns=['Time','Bankroll'])

#MathPlotLib Graph
figure2 = plt.Figure(figsize=(9,4), dpi=60)
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, tab4)
line2.get_tk_widget().place(x=350, y=25)
df2 = df2[['Time','Bankroll']].groupby('Time').sum()
df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
ax2.set_title('Time Vs. Bankroll')

#Rule Variatiions 
insurance = tk.IntVar()
lateSurrender = tk.IntVar()
doubleAfterSplit = tk.IntVar()
dealerStand = tk.IntVar()
resplitAces = tk.IntVar()
basicStratDeviations = tk.IntVar()

#Variation Label
label = ttk.Label(tab4, text='Rule Variations:', font=('Helvetica', 18, 'bold'))
label.place(x=20, y=10)

#Question Mark button leads to help website 
helpImage = Image.open('Resources/questionMark.png')
helpPhoto = ImageTk.PhotoImage(helpImage.resize((40, 40), Image.ANTIALIAS))
helpButton = tk.Button(tab4, image= helpPhoto, command=openWebsite, borderwidth=0).place(x=910,y=10)

# CheckButtons 
c1 = ttk.Checkbutton(tab4, text='Insurance',variable=insurance, onvalue=1, offvalue=0).place(x=20, y=40)
c2 = ttk.Checkbutton(tab4, text='Late Surrender Allowed',variable=lateSurrender, onvalue=1, offvalue=0).place(x=20, y=70)
c3 = ttk.Checkbutton(tab4, text='Double After Split',variable=doubleAfterSplit, onvalue=1, offvalue=0).place(x=20, y=100)
c4 = ttk.Checkbutton(tab4, text='Dealer Stands on soft 17 ',variable=dealerStand, onvalue=1, offvalue=0).place(x=20, y=130)
c5 = ttk.Checkbutton(tab4, text='Resplit aces',variable=resplitAces, onvalue=1, offvalue=0).place(x=20, y=160)
c6 = ttk.Checkbutton(tab4, text='Basic Startegy Deviations',variable=basicStratDeviations, onvalue=1, offvalue=0).place(x=20, y=190)

#Sliders
s1 = tk.Scale(tab4, from_=0, to=1000, orient='horizontal')
s1.set(0)
s1.place(x=140, y=230)

s2 = tk.Scale(tab4, from_=0, to=1000, orient='horizontal')
s2.set(0)
s2.place(x=140, y=280)

s3 = tk.Scale(tab4, from_=0, to=1000, orient='horizontal')
s3.set(0)
s3.place(x=140, y=330)

#Slider Labels
s1Label = ttk.Label(tab4, text='Slider 1 Label:').place(x=10, y=250)
s2Label = ttk.Label(tab4, text='Slider 2 Label:').place(x=10, y=300)
s3Label = ttk.Label(tab4, text='Slider 3 Label:').place(x=10, y=350)

#Run Button
runButton = ttk.Button(tab4, text="Run", padding=15).place(x=550, y=300)



root.mainloop()
