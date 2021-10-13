import tkinter as tk
from tkinter import Button, StringVar, ttk
from tkinter import font
from tkinter.constants import ANCHOR, HORIZONTAL, S
from tkinter.font import Font, nametofont
import webbrowser
import time

# Imported for Images
from PIL import ImageTk, Image

# For mathlib charts
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import external functions
from CardDetect.test3 import startWebcam
# from carddetection import start

root = tk.Tk()

# Window Name
root.title("SD Blackjack")
# Icon for window
root.iconphoto(False, tk.PhotoImage(file='Resources/favicon2.png'))
helpImage = Image.open('Resources/questionMark.png')
helpPhoto = ImageTk.PhotoImage(helpImage.resize((40, 40), Image.ANTIALIAS))

#Styling 

style = ttk.Style(root)
root.tk.call('source', 'Resources/Forest-ttk-theme-master/Forest-ttk-theme-master/forest-dark.tcl')
style.theme_use('forest-dark')
# style.configure('TNotebook.Tab', padding=[20, 12], font=('Helvetica', 20))



def finished():
    print("DEF FINISHED")


# Notebook is basis of tabs
tabControl = ttk.Notebook(root, style='Custom.TNotebook')


# set Definite sieze for window
root.wm_geometry("1000x500")

# Makes window not Resizable
root.resizable(False, False)


# Set global font size
default_font = nametofont("TkDefaultFont")
default_font.configure(size=15)
root.option_add("*Font", default_font)

# Tab names/ Page Frames
tab1 = tk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

# Add tabs to bar
tabControl.add(tab1, text='Welcome')
tabControl.add(tab2, text='Strategy Charts')
tabControl.add(tab3, text='LiveFeed')
tabControl.add(tab4, text='Simulator')

# Packing all tabs
tabControl.pack(expand=1, fill="both", anchor='center')
# root.wm_attributes('-alpha', 0.7)

# Style the tabs
background_label = tk.Label(tab1).pack()
background_label = tk.Label(tab2).pack()
background_label = tk.Label(tab3).pack()
background_label = tk.Label(tab4).pack()



###########################
#						  #
# Welcome page components #
#						  #
###########################


# Logo
image1 = Image.open('Resources/blackjackLogo.png')
photo1 = ImageTk.PhotoImage(image1.resize((350, 252), Image.ANTIALIAS))
imgLabel1 = ttk.Label(tab1, image=photo1).place(x=300, y=20)

# Lables
ttk.Label(tab1, text="The ultimate card counting trainer.").place(x=325, y=285)
ttk.Label(tab1, text="Creators: Connor Graham, John Murphy, Tyler Vandermate, Paul Vicino, Graham West  ").place(x=150, y=370)

##############################
#						     #
# Strategy Charts components #
#						     #
##############################

#True count incrementing Stystem
trueCount = 0

def trueCountDown():
    global trueCount
    if trueCount <= 0:
        pass 
    else:
        trueCount -= 1
        updateText = ("True Count: " + str(trueCount))
        trueCountLabel.configure(text=updateText)
        trueCountLabel.update()

def trueCountUp():
    global trueCount
    trueCount+= 1
    updateText = ("True Count: " + str(trueCount))
    trueCountLabel.configure(text=updateText)
    trueCountLabel.update()


#####TODO CHANGE TO STRATEGY CHARTS SPECIFIC INFO PAGE 
def openWebsiteStrat():
    webbrowser.open("https://sd1-blackjack.herokuapp.com/login?next=%2F", new=0, autoraise=True)


image2 = Image.open('Resources/stratchart1.jpg')
photo2 = ImageTk.PhotoImage(image2.resize((280, 370), Image.ANTIALIAS))
imgLabel2 = ttk.Label(tab2, image=photo2).place(x=610, y=10)

#Up Increment
upButtonImg = Image.open('Resources/upArrow.png')
upButtonImg2 = ImageTk.PhotoImage(upButtonImg.resize((70, 40), Image.ANTIALIAS))
upButton = ttk.Button(tab2, image=upButtonImg2, command=trueCountUp).place(x=500, y = 80)

#Down Increment
downButtonImg = Image.open('Resources/downArrow.png')
downButtonImg2 = ImageTk.PhotoImage(downButtonImg.resize((70, 40), Image.ANTIALIAS))
downButton = ttk.Button(tab2, image=downButtonImg2, command=trueCountDown).place(x=500, y = 200)

#Label GEts updated by TCUp  and TCDown
trueCountLabel = ttk.Label(tab2, text="True Count: 0")
trueCountLabel.place(x=475, y = 150)


#CheckBoxes
insuranceTC = tk.IntVar()
lateSurrenderTC = tk.IntVar()
doubleAfterSplitTC = tk.IntVar()
dealerStandTC = tk.IntVar()
resplitAcesTC = tk.IntVar()
basicStratDeviationsTC = tk.IntVar()

tc1 = ttk.Checkbutton(tab2, text='Insurance', variable=insuranceTC,
                     onvalue=1, offvalue=0).place(x=20, y=40)
tc2 = ttk.Checkbutton(tab2, text='Late Surrender Allowed', 
                     variable=lateSurrenderTC, onvalue=1, offvalue=0).place(x=20, y=70)
tc3 = ttk.Checkbutton(tab2, text='Double After Split',
                     variable=doubleAfterSplitTC, onvalue=1, offvalue=0).place(x=20, y=100)
tc4 = ttk.Checkbutton(tab2, text='Dealer Stands on soft 17 ',
                     variable=dealerStandTC, onvalue=1, offvalue=0).place(x=20, y=130)
tc5 = ttk.Checkbutton(tab2, text='Resplit aces', variable=resplitAcesTC,
                     onvalue=1, offvalue=0).place(x=20, y=160)
tc6 = ttk.Checkbutton(tab2, text='Basic Startegy Deviations',
                     variable=basicStratDeviationsTC, onvalue=1, offvalue=0).place(x=20, y=190)


helpButton = ttk.Button(tab2, image=helpPhoto,
                       command=openWebsiteStrat).place(x=910, y=10)
###########################
#						  #
#   Livefeed components   #
#						  #
###########################
l1 = tk.Label(tab3, text="Running Count:")
l2 = tk.Label(tab3, text="True Count:")
l3 = tk.Label(tab3, text="Decks Remaining:")
l4 = tk.Label(tab3, text="Current Bet:")
l5 = tk.Label(tab3, text="Reset page")


def changePage():
    l1.place(x=100,y=20)
    l1.update()
    l2.place(x=650,y=20)
    l3.place(x=100,y=300)
    l4.place(x=650,y=300)
    startstream.place(x=10000,y=10000)
    startWebcam()



startstream = ttk.Button(tab3, text="Start Livefeed",
                         command=changePage).place(x=400, y=100)

##############################
#						     #
#     Simulator components   #
#						     #
##############################

#####TODO CHANGE TO SIMULATOR SPECIFIC INFO PAGE 
def openWebsiteSim():
    webbrowser.open(
        "https://sd1-blackjack.herokuapp.com/login?next=%2F", new=0, autoraise=True)


# MathPlotLibData
# MathLib Testing Seciton
data2 = {'Time': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
         'Bankroll': [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]}
df2 = DataFrame(data2, columns=['Time', 'Bankroll'])

# MathPlotLib Graph
figure2 = plt.Figure(figsize=(9, 4), dpi=60)
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, tab4)
line2.get_tk_widget().place(x=350, y=25)
df2 = df2[['Time', 'Bankroll']].groupby('Time').sum()
df2.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
ax2.set_title('Time Vs. Bankroll')

# Rule Variatiions
insurance = tk.IntVar()
lateSurrender = tk.IntVar()
doubleAfterSplit = tk.IntVar()
dealerStand = tk.IntVar()
resplitAces = tk.IntVar()
basicStratDeviations = tk.IntVar()

# Variation Label
label = ttk.Label(tab4, text='Rule Variations:',
                  font=('Helvetica', 18, 'bold'))
label.place(x=20, y=10)

# Question Mark button leads to help website
# helpImage = Image.open('Resources/questionMark.png')
# helpPhoto = ImageTk.PhotoImage(helpImage.resize((40, 40), Image.ANTIALIAS))
helpButton = ttk.Button(tab4, image=helpPhoto,
                       command=openWebsiteSim).place(x=910, y=10)

# CheckButtons
c1 = ttk.Checkbutton(tab4, text='Insurance', variable=insurance,
                     onvalue=1, offvalue=0).place(x=20, y=40)
c2 = ttk.Checkbutton(tab4, text='Late Surrender Allowed', 
                     variable=lateSurrender, onvalue=1, offvalue=0).place(x=20, y=70)
c3 = ttk.Checkbutton(tab4, text='Double After Split',
                     variable=doubleAfterSplit, onvalue=1, offvalue=0).place(x=20, y=100)
c4 = ttk.Checkbutton(tab4, text='Dealer Stands on soft 17 ',
                     variable=dealerStand, onvalue=1, offvalue=0).place(x=20, y=130)
c5 = ttk.Checkbutton(tab4, text='Resplit aces', variable=resplitAces,
                     onvalue=1, offvalue=0).place(x=20, y=160)
c6 = ttk.Checkbutton(tab4, text='Basic Startegy Deviations',
                     variable=basicStratDeviations, onvalue=1, offvalue=0).place(x=20, y=190)

# Sliders
s1 = tk.Scale(tab4, from_=0, to=1000, orient='horizontal')
s1.set(0)
s1.place(x=170, y=230)

s2 = tk.Scale(tab4, from_=0, to=1000, orient='horizontal')
s2.set(0)
s2.place(x=170, y=280)

s3 = tk.Scale(tab4, from_=0, to=1000, orient='horizontal')
s3.set(0)
s3.place(x=170, y=330)

# Slider Labels
s1Label = ttk.Label(tab4, text='Starting Bankroll:').place(x=10, y=250)
s2Label = ttk.Label(tab4, text='Hands per hour:').place(x=10, y=300)
s3Label = ttk.Label(tab4, text='Hours Played:').place(x=10, y=350)

#Progress Bar


progress = ttk.Progressbar(tab4, orient=HORIZONTAL,
              length = 300, mode = 'determinate')
progress.place(x=475, y=275)

def step():
    for i in range(11):
        root.update_idletasks()
        progress['value'] += 10
        time.sleep(0.2)
    progress['value'] = 0

        
# Run Button
runButton = ttk.Button(tab4, text="Run", padding=15, command=step).place(x=575, y=300)


root.mainloop()
