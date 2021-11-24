# # TODO

#   insurance thing under chart
#   True count
#   Expected value
#   Running Count
#   Starting decks? (Disable livefeed until > 0 1-8)


# Sim:
#   Empty graph before gen
#   bankroll go to 10mil
#   Rounds played label


# Adjust ticks to 1000
# Sqrt 10mil




# IMPORTS
# region
import tkinter as tk
from tkinter import Button, IntVar, Spinbox, StringVar, ttk
from tkinter import font
from tkinter.constants import ANCHOR, BOTH, CENTER, DISABLED, HORIZONTAL, RIDGE, S, VERTICAL, Y
from tkinter.font import Font, nametofont
import webbrowser
import time
import cv2
import numpy as np
import math
import threading
import tkinter.scrolledtext as ScrolledText
from Resources.houseEdgeCalc.chart import HardTable,SoftTable,SplitTable

# Imported for Images
from PIL import ImageTk, Image
from numpy.random.mtrand import random

# For mathlib charts
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# IR Imports
import torch 
from torch.autograd import Variable
from Resources.cardDetection.darknet import Darknet
import random
from Resources.cardDetection.util import *


##############
# DEMO ONLY IMPORTS
from Resources.simulator.blackjack_hi_low import Table
from Resources.simulator.player import Player
from Resources.simulator.dealer import Dealer
from Resources.simulator.card import Card
from Resources.simulator.hand import Hand
from Resources.houseEdgeCalc.EdgeCalc import edgeCalc
# endregion

# ROOT TK ITEMS
# region
root = tk.Tk()

# Window Name
root.title("SD Blackjack")

# Icon for window
root.iconphoto(False, tk.PhotoImage(file="Resources/images/favicon2.png"))
helpImage = Image.open("Resources/images/questionMark.png")
helpPhoto = ImageTk.PhotoImage(helpImage.resize((60, 60), Image.ANTIALIAS))

# Styling

style = ttk.Style(root)
# root.tk.call('source', 'Resources/Forest-ttk-theme-master/Forest-ttk-theme-master/forest-light.tcl')
root.tk.call(
    "source",
    "Resources/Forest-ttk-theme-master/Forest-ttk-theme-master/forest-dark.tcl",
)
style.theme_use("forest-dark")

# Notebook is basis of tabs
tabControl = ttk.Notebook(root)

# set Definite size for window
root.wm_geometry("1600x800")

# Makes window not Resizable
root.resizable(False, False)


# Set global font size
default_font = nametofont("TkDefaultFont")
default_font.configure(size=20)
root.option_add("*Font", default_font)

# Tab names/ Page Frames
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

# Add tabs to bar
tabControl.add(tab1, text="Welcome")
tabControl.add(tab2, text="Strategy Charts")
tabControl.add(tab3, text="LiveFeed")
tabControl.add(tab4, text="Simulator")


# Packing all tabs
tabControl.pack(expand=1, fill="both", anchor="center")


# endregion

###########################
# 						  #
# Welcome page components #
# 						  #
###########################
# TODO change to welcome site 
def openWebsiteWelcome():
    webbrowser.open(
        "https://sd1-blackjack.herokuapp.com/login?next=%2F", new=0, autoraise=True
    )

# Logo
image1 = Image.open("Resources/images/blackjackLogo.png")
photo1 = ImageTk.PhotoImage(image1.resize((490, 412), Image.ANTIALIAS))
imgLabel1 = ttk.Label(tab1, image=photo1).place(x=540, y=80)

ttk.Button(tab1, text = "Learn more about the app!",command = openWebsiteWelcome, padding=15).place(x=680, y=630)

# Lables
ttk.Label(tab1, text="The ultimate card counting trainer.",font=(default_font, 26)).place(x=525, y=505)
ttk.Label(
    tab1,
    text="Created by Connor Graham, John Murphy, Tyler Vandermate, Paul Vicino, Graham West  ", font=(default_font, 10)
).place(x=530, y=555)

##############################
# 						     #
# Strategy Charts components #
# 						     #
##############################

# True count incrementing Stystem

trueCount = 0
# Label GEts updated by TCUp  and TCDown
global trueCountLabel
trueCountLabel = ttk.Label(tab2, text="True Count: 0")

trueCountLabel.place(x=475, y=150)

# def updateText():
#     global trueCount
#     updateText = "True Count: " + str(trueCount)
#     return updateText

def trueCountDown():
    global trueCount, trueCountLabel
    
    if trueCount <= -10:
        pass
    else:
        if trueCount == 0:
            trueCountLabel = ttk.Label(tab2, text="True Count: 0")
            trueCountLabel.place(x=475, y=150)
        trueCount -= 1
        updateText = "True Count: " + str(trueCount)
        trueCountLabel.configure(text=updateText)
        trueCountLabel.update_idletasks()
        
        runEdgeCalc()


def trueCountUp():
    global trueCount, trueCountLabel
    if trueCount >= 10:
        pass
    else:
        if trueCount == 0:
            trueCountLabel = ttk.Label(tab2, text="True Count: 0")
            trueCountLabel.place(x=475, y=150)
        trueCount += 1
        updateText = "True Count: " + str(trueCount)
        trueCountLabel.configure(text=updateText)
        trueCountLabel.update_idletasks()
        runEdgeCalc()


#####TODO CHANGE TO STRATEGY CHARTS SPECIFIC INFO PAGE
def openWebsiteStrat():
    webbrowser.open(
        "https://sd1-blackjack.herokuapp.com/login?next=%2F", new=0, autoraise=True
    )


##
##CHART SIDE
##

graphFrame = tk.Frame(tab2)
hardFrame = tk.Frame(graphFrame)
softFrame = tk.Frame(graphFrame)
splitframe = tk.Frame(graphFrame)

t = HardTable(hardFrame)
t2 = SoftTable(softFrame)
t3 = SplitTable(splitframe)

hardFrame.pack()
softFrame.pack()
splitframe.pack()

graphFrame.place(x = 1000, y = 20)


# Up Increment
upButtonImg = Image.open("Resources/images/upArrow.png")
upButtonImg2 = ImageTk.PhotoImage(upButtonImg.resize((70, 40), Image.ANTIALIAS))
upButton = ttk.Button(tab2, image=upButtonImg2, command=trueCountUp).place(x=500, y=80)

# Down Increment
downButtonImg = Image.open("Resources/images/downArrow.png")
downButtonImg2 = ImageTk.PhotoImage(downButtonImg.resize((70, 40), Image.ANTIALIAS))
downButton = ttk.Button(tab2, image=downButtonImg2, command=trueCountDown).place(
    x=500, y=200
)



##
##EDGE CALC SIDE
##
houseEdgeTag = ttk.Label(tab2, text="Player Edge:", font=(default_font, 17))
houseEdgeTag.place(x=20, y=340)
stdDevTag = ttk.Label(tab2, text="Standard Deviation:", font=(default_font, 17))
stdDevTag.place(x=20, y=375)


playerEdgeLabel = ttk.Label(tab2, text="0", borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
playerEdgeLabel.place(x=230, y=340)
stdDevLabel = ttk.Label(tab2, text="0", borderwidth=3, relief="solid", width = 8, anchor= CENTER, font=(default_font, 17))
stdDevLabel.place(x=230, y=375)




def runEdgeCalc():
    global trueCount
    houseText, stdDevText = edgeCalc(
        insuranceTC.get(),
        lateSurrenderTC.get(),
        doubleAfterSplitTC.get(),
        dealerStandTC.get(),
        resplitAcesTC.get(),
        basicStratDeviationsTC.get(),
        decks.get(),
    )
    
    playerEdge = str('{: .3f}'.format(1 - float(houseText) + (0.5) * trueCount) + "%")

    playerEdgeLabel.configure(text = playerEdge)
    playerEdgeLabel.update_idletasks()
    stdDevLabel.configure(text = stdDevText)
    stdDevLabel.update_idletasks()


# CheckBoxes
insuranceTC = tk.IntVar()
lateSurrenderTC = tk.IntVar()
doubleAfterSplitTC = tk.IntVar()
dealerStandTC = tk.IntVar()
resplitAcesTC = tk.IntVar()
basicStratDeviationsTC = tk.IntVar()
decks = tk.IntVar()

ttk.Label(tab2, text="Number of Decks:").place(x=150, y=10)

# Radio Buttons
ttk.Radiobutton(tab2, text="1", variable=decks, value=0, command=runEdgeCalc).place(x=160, y=50)
ttk.Radiobutton(tab2, text="2", variable=decks, value=1, command=runEdgeCalc).place(x=200, y=50)
ttk.Radiobutton(tab2, text="4", variable=decks, value=2, command=runEdgeCalc).place(x=240, y=50)
ttk.Radiobutton(tab2, text="6", variable=decks, value=4, command=runEdgeCalc).place(x=280, y=50)

# Check Buttons
tc1 = ttk.Checkbutton(
    tab2,
    text="Insurance",
    variable=insuranceTC,
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc,
).place(x=20, y=80)
tc2 = ttk.Checkbutton(
    tab2,
    text="Late Surrender Allowed",
    variable=lateSurrenderTC,
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc,
).place(x=20, y=120)
tc3 = ttk.Checkbutton(
    tab2, text="Double After Split", 
    variable=doubleAfterSplitTC,
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc,
).place(x=20, y=160)
tc4 = ttk.Checkbutton(
    tab2,
    text="Dealer Stands on soft 17 ",
    variable=dealerStandTC,
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc
).place(x=20, y=200)
tc5 = ttk.Checkbutton(
    tab2, text="Resplit aces", 
    variable=resplitAcesTC, 
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc
).place(x=20, y=240)
tc6 = ttk.Checkbutton(
    tab2,
    text="Basic Startegy Deviations",
    variable=basicStratDeviationsTC,
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc
).place(x=20, y=280)

helpButton = ttk.Button(tab2, image=helpPhoto, command=openWebsiteStrat).place(
    x=1480, y=10
)


###########################
# 						  #
#   Livefeed components   #
# 						  #
###########################

stopIR = 0

imageFrame = tk.Frame(tab3, width='1000', height='500')

placeholderImage = Image.open("Resources/images/webcamPlacehold2.png")
placeholdPhoto = ImageTk.PhotoImage(placeholderImage.resize((600, 500), Image.ANTIALIAS))


imageFrame.place(x=50, y = 50)
lmain = ttk.Label(imageFrame, borderwidth=2 , relief="solid")
lmain.grid(row=0, column=0, columnspan=15)
lmain.configure(image=placeholdPhoto)
lmain.config(borderwidth=3, relief=tk.SOLID)
running_Count = 0

def updateRunningCount(running_Count):
    l2.configure(text=running_Count)
    l2.update_idletasks()

loadingBar = ttk.Progressbar(
        tab3,
        orient='horizontal',
        mode='indeterminate',
        length=280
    )


def prep_image(img, inp_dim):

    orig_im = img
    dim = orig_im.shape[1], orig_im.shape[0]
    img = cv2.resize(orig_im, (inp_dim, inp_dim))
    img_ = img[:,:,::-1].transpose((2,0,1)).copy()
    img_ = torch.from_numpy(img_).float().div(255.0).unsqueeze(0)
    return img_, orig_im, dim

count = 0

def write(x, img, classes, colors):
    global count, st
    c1 = tuple(x[1:3].int())
    c1 = int(c1[0]), int(c1[1])
    c2 = tuple(x[3:5].int())
    c2 = int(c2[0]), int(c2[1])
    cls = int(x[-1])
    label = "{0}".format(classes[cls])
    if count == 90:
        msg = 'Card Seen: ' + label + '\n'
        st.insert('end', msg)
        st.update_idletasks()
        st.yview(tk.END)
        
        count == 0
    else:
        count += 1


    color = random.choice(colors)
    cv2.rectangle(img, c1, c2,(255,0,0), 1)
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
    c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
    cv2.rectangle(img, c1, c2,(0,0,0), -1)
    cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225,255,255], 1);
    return img


def RunIR():
    
    
    cfgfile = "Resources/cardDetection/train.cfg"
    weightsfile = "Resources/cardDetection/card_chip.weights"
    num_classes = 18

    confidence = 0.5
    nms_thesh = 0.3
    start = 0
    CUDA = torch.cuda.is_available()
    

    
    
    bbox_attrs = 5 + num_classes
    
    model = Darknet(cfgfile)
    model.load_weights(weightsfile)
    
    model.net_info["height"] = 640
    inp_dim = int(model.net_info["height"])
    
    assert inp_dim % 32 == 0 
    assert inp_dim > 32

    if CUDA:
        model.cuda()
            
    model.eval()
    
    cap = cv2.VideoCapture(0)
    
    assert cap.isOpened(), 'Cannot capture source'
    
    frames = 0
    start = time.time()  
    loadingBar.destroy()  
    while stopIR == 0:
        
        ret, frame = cap.read()
    
        
        img, orig_im, dim = prep_image(frame, inp_dim)
        
        im_dim = torch.FloatTensor(dim).repeat(1,2)                        
        
        
        if CUDA:
            im_dim = im_dim.cuda()
            img = img.cuda()
      
        output = model(Variable(img), CUDA)
        output = write_results(output, confidence, num_classes, nms = True, nms_conf = nms_thesh)

        output[:,1:5] = torch.clamp(output[:,1:5], 0.0, float(inp_dim))/inp_dim
        output[:,[1,3]] *= frame.shape[1]
        output[:,[2,4]] *= frame.shape[0]

        
        classes = load_classes('Resources/cardDetection/classes.names')
        colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')
        
        list(map(lambda x: write(x, orig_im, classes, colors), output))

        im = cv2.cvtColor(orig_im, cv2.COLOR_BGR2RGBA)
        im = Image.fromarray(im)
        im = ImageTk.PhotoImage(image=im)
        lmain.configure(image=im)
        lmain.update_idletasks()

    cap.release()
    cv2.destroyAllWindows()
    lmain.configure(image=placeholdPhoto)        



l1 = tk.Label(tab3, text="Current Card(s):")
l2 = tk.Label(tab3, text="")
l3 = tk.Label(tab3, text="Decks Remaining:")
l4 = tk.Label(tab3, text="Current Bet:")
l5 = tk.Label(tab3, text="Reset page")


def startStream():
    global loadingBar
    loadingBar.place(x=380,y=410)
    loadingBar.start(10)

    # Change Buttons
    startStream.place(x=2000, y=800)
    endStream.place(x=1275, y=600)

    # l1.place(x=1050, y=50)
    # l2.place(x=880, y=50)

    # Start/Stop Variables
    global stopIR
    stopIR = 0

    # Start thread for IR 
    T1 = threading.Thread(target=RunIR)
    T1.start()
    


def endStream():
    global stopIR
    global loadingBar
    stopIR = 1
    try:
        loadingBar.stop()
    except:
        print("")
    lmain.update_idletasks()
    # Change Buttons
    endStream.place(x=2000, y=800)
    startStream.place(x=1275, y=600)


st = ScrolledText.ScrolledText(tab3, state='normal')

st.configure(font=(default_font, 12),width=75, height = 28, bg='black', fg='white')
st.place(x=800,y=40)
st.update_idletasks()

playerBox = ttk.Spinbox(tab3, from_=1,to = 3, width=8, wrap='true', justify=CENTER, takefocus='false', exportselection = 'true')
playerBox.place(x=975, y=600)


startStream = ttk.Button(tab3, text="Start Livefeed", padding=18, width = 17, command=startStream)
startStream.place(x=1275, y=600)
endStream = ttk.Button(tab3, text="End Livefeed", padding=18,  width = 17,command=endStream)

trueCountLabel = ttk.Label(tab3, text="True Count:").place(x=10, y=600)
runningCountLabel = ttk.Label(tab3, text="Running Count:").place(x=10, y=650)
trueCountLabelBox = ttk.Label(tab3, text=0, borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
trueCountLabelBox.place(x=200, y=610)
runningCountLabelBox = ttk.Label(tab3, text=0, borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
runningCountLabelBox.place(x=200, y=660)

##############################
# 						     #
#     Simulator components   #
# 						     #
##############################

#####TODO CHANGE TO SIMULATOR SPECIFIC INFO PAGE
def openWebsiteSim():
    webbrowser.open(
        "https://sd1-blackjack.herokuapp.com/login?next=%2F", new=0, autoraise=True
    )


# MathPlotLibData

bankrollvsTime = []
def demoDay():
    
    #TODO DELETE DEMO ONLY TEST 
    global progress
    
    num_decks = 8
    deck_pen = 0.75
    min_bet = 10
    max_bet = 1000

    total_rounds_played = 15000
    start_stack_size = 50000
    betting_units = 200
    num_bins = 500

    game = Table(num_decks, deck_pen, min_bet, max_bet)
    player_list = []

    player_list.append(Player(0, start_stack_size, betting_units, '1-12'))
    player_list[0].take_seat(0, game)


    # ONLY WORKS WHEN 1 PLAYER IS SITTING AND MUST BE IN SEAT INDEX ZERO!!!
    # (hotfix for demo)
    # try:
    bankroll_over_time = game.play_n_rounds(total_rounds_played, num_bins)
    # except:
    #     
    #     return
        
        


    rounds = np.linspace(0, total_rounds_played, retstep=True, num=num_bins, dtype=int, axis=0)
  
    
    global bankrollvsTime


    bankrollvsTime = DataFrame(data = np.column_stack((rounds[0],bankroll_over_time)), columns=['Rounds', 'Bankroll']).groupby("Rounds").sum()

    #####
 
    # progress.stop()
    # MathPlotLib Graph
    figure2 = plt.Figure(figsize=(9, 4), dpi=85)

    ax2 = figure2.add_subplot(111)

    line2 = FigureCanvasTkAgg(figure2, tab4)

    line2.get_tk_widget().place(x=650, y=25)

    # df2 = bankrollvsTime[["Rounds", "Bankroll"]].groupby("Time").sum()

    bankrollvsTime.plot(kind="line", legend=True, ax=ax2, color="g", marker="o", fontsize=20)

    figure2.set_facecolor('xkcd:grey')

    ax2.set_facecolor('xkcd:white')

    ax2.set_title("Time Vs. Bankroll")

    progress.stop()

    # END DELETE

# Rule Variatiions
insurance = tk.IntVar()
lateSurrender = tk.IntVar()
doubleAfterSplit = tk.IntVar()
dealerStand = tk.IntVar()
resplitAces = tk.IntVar()
basicStratDeviations = tk.IntVar()

# Variation Label
label = ttk.Label(tab4, text="Rule Variations:", font=("Helvetica", 18, "bold"))
label.place(x=20, y=10)

# Question Mark button leads to help website
helpButton = ttk.Button(tab4, image=helpPhoto, command=openWebsiteSim).place(
    x=1480, y=10
)

# CheckButtons
c1 = ttk.Checkbutton(
    tab4, text="Insurance", variable=insurance, onvalue=1, offvalue=0
).place(x=20, y=40)
c2 = ttk.Checkbutton(
    tab4, text="Late Surrender Allowed", variable=lateSurrender, onvalue=1, offvalue=0
).place(x=20, y=80)
c3 = ttk.Checkbutton(
    tab4, text="Double After Split", variable=doubleAfterSplit, onvalue=1, offvalue=0
).place(x=20, y=120)
c4 = ttk.Checkbutton(
    tab4, text="Dealer Stands on soft 17 ", variable=dealerStand, onvalue=1, offvalue=0
).place(x=20, y=160)
c5 = ttk.Checkbutton(
    tab4, text="Resplit aces", variable=resplitAces, onvalue=1, offvalue=0
).place(x=20, y=200)
c6 = ttk.Checkbutton(
    tab4,
    text="Basic Startegy Deviations",
    variable=basicStratDeviations,
    onvalue=1,
    offvalue=0,
).place(x=20, y=240)

#Kelly Bets Radio
ttk.Radiobutton(tab4, text="Kelly Bet", variable=decks, value=0).place(x=20, y=650)
ttk.Radiobutton(tab4, text="Flat Bet", variable=decks, value=1).place(x=130, y=650)
# value = 0
# current_value = 0.1
current_valueROR = tk.DoubleVar(value = .1)
current_valueBR = tk.IntVar(value = 0)
current_valueRP = tk.IntVar(value = 0)

#Functions for Risk of Ruin slider

def riskOfRuin():
    # print(current_value.get())
    tmp = -math.log(current_valueROR.get(), 2)
    ror = math.exp(-2/tmp)
    return str('{: .3f}'.format(ror))
    
def slider_changedRor(event):
    s2Label = ttk.Label(tab4, text=riskOfRuin(), borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
    s2Label.place(x=355, y=555)
    s2Label.configure(text=riskOfRuin())

# Functions for Bankroll slider

def bankroll():
    val = current_valueBR.get()
    tmp = math.pow(val, 4)
    return str('{: .1f}'.format(tmp))

def slider_changedBR(event):
    s1Label = ttk.Label(tab4, text=bankroll(), borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
    s1Label.place(x=355, y=505)
    s1Label.configure(text=bankroll())
    s1Label.update_idletasks()

# Function for rounds played slider

def slider_changedRP(event):
    s3Label = ttk.Label(tab4, text=current_valueRP, borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
    s3Label.place(x=355, y=605)
    s3Label.configure(text=current_valueRP.get())
    s3Label.update_idletasks()

# Sliders
s1 = ttk.Scale(tab4, from_=0, to=47.2870805, orient="horizontal",command=slider_changedBR, variable=current_valueBR)
s1.set(0)
s1.place(x=240, y=510)

s2 = ttk.Scale(tab4, from_=0.999, to=0.5, orient="horizontal", command=slider_changedRor, variable=current_valueROR)
s2.set(0.999)
s2.place(x=240, y=560)

s3 = ttk.Scale(tab4, from_=0, to=5000000, orient="horizontal", command = slider_changedRP, variable = current_valueRP)
s3.set(0)
s3.place(x=240, y=610)

# Slider Labels
s1Label = ttk.Label(tab4, text="Starting Bankroll:").place(x=10, y=500)
s2Label = ttk.Label(tab4, text="Risk of Ruin:").place(x=10, y=550)
s3Label = ttk.Label(tab4, text="Rounds Played:").place(x=10, y=600)


# Progress Bar
progress = ttk.Progressbar(tab4, orient=HORIZONTAL, length=300, mode="indeterminate")
progress.place(x=870, y=380)

# Step Function to iterate loading bar 


def runGraph():
    global progress
    progress.start(10)
    T2 = threading.Thread(target=demoDay)
    T2.start()

# Run Button
runButton = ttk.Button(tab4, text="Run", padding=15, command=runGraph)
runButton.place(x=950, y=420)

# Add player button
add_player_button = ttk.Button(tab4, text="Add Player", padding=5)
add_player_button.place(x=810, y=520)
#   Add table button
add_table_button = ttk.Button(tab4, text="Add Table", padding=5)
add_table_button.place(x=960, y=520)
#   clear all button
clear_all_button = ttk.Button(tab4, text="Clear", padding=5)
clear_all_button.place(x=1110, y=520)



root.mainloop()
