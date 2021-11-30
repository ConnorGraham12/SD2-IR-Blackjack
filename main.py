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

from pandas.core import frame
from Resources.houseEdgeCalc.chart import Chart
# from Resources.houseEdgeCalc.chart import HardTable,SoftTable,SplitTable
from Resources.houseEdgeCalc.test2 import get_bs_stand_soft_17, get_bs_hit_soft_17

# Imported for Images
from PIL import ImageTk, Image
from numpy.random.mtrand import random

# For mathlib charts
from pandas import DataFrame as df
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# IR Imports
import torch 
from torch.autograd import Variable
from Resources.cardDetection.darknet import Darknet
import random
from Resources.cardDetection.util import *
from Resources.cardDetection.GPUir import IR
# IR Hand Suggestion imports 

from Resources.cardDetection.sim2.table import TableIR
from Resources.cardDetection.sim2.player import PlayerIR
from Resources.cardDetection.sim2.rule_set import RuleSet
from Resources.cardDetection.sim2.hand import Hand
from Resources.cardDetection.sim2.card import Card


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

def openWebsite():
    webbrowser.open(
        "https://sd2blackjack.herokuapp.com/", new=0, autoraise=True
    )



# endregion

###########################
# 						  #
# Welcome page components #
# 						  #
###########################


# Logo
image1 = Image.open("Resources/images/blackjackLogo.png")
photo1 = ImageTk.PhotoImage(image1.resize((490, 412), Image.ANTIALIAS))
imgLabel1 = ttk.Label(tab1, image=photo1).place(x=540, y=80)

ttk.Button(tab1, text = "Learn more about the app!",command = openWebsite, padding=15).place(x=650, y=630)

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

trueCountLabel.place(x=715, y=310)


def trueCountDown():
    global trueCount, trueCountLabel
    
    if trueCount <= -10:
        pass
    else:
        if trueCount == 0:
            trueCountLabel = ttk.Label(tab2, text="True Count: 0")
            trueCountLabel.place(x=715, y=310)
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
            trueCountLabel.place(x=715, y=310)
        trueCount += 1
        updateText = "True Count: " + str(trueCount)
        trueCountLabel.configure(text=updateText)
        trueCountLabel.update_idletasks()
        runEdgeCalc()




##
##CHART SIDE
##

graphFrame2 = tk.Frame(tab2)
t = Chart(graphFrame2, 'hit')



graphFrame2.place(x = 900, y = 20)


# Up Increment
upButtonImg = Image.open("Resources/images/upArrow.png")
upButtonImg2 = ImageTk.PhotoImage(upButtonImg.resize((70, 40), Image.ANTIALIAS))
upButton = ttk.Button(tab2, image=upButtonImg2, command=trueCountUp).place(x=750, y=240)

# Down Increment
downButtonImg = Image.open("Resources/images/downArrow.png")
downButtonImg2 = ImageTk.PhotoImage(downButtonImg.resize((70, 40), Image.ANTIALIAS))
downButton = ttk.Button(tab2, image=downButtonImg2, command=trueCountDown).place(
    x=750, y=380
)



##
##EDGE CALC SIDE
##
houseEdgeTag = ttk.Label(tab2, text="House Edge:", font=(default_font, 17))
houseEdgeTag.place(x=10, y=600)
stdDevTag = ttk.Label(tab2, text="Standard Deviation:", font=(default_font, 17))
stdDevTag.place(x=10, y=650)


playerEdgeLabel = ttk.Label(tab2, text="0", borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
playerEdgeLabel.place(x=240, y=600)
stdDevLabel = ttk.Label(tab2, text="0", borderwidth=3, relief="solid", width = 8, anchor= CENTER, font=(default_font, 17))
stdDevLabel.place(x=240, y=650)




def runEdgeCalc():
    global trueCount, graphFrame2
    houseText, stdDevText = edgeCalc(
        insuranceTC.get(),
        lateSurrenderTC.get(),
        doubleAfterSplitTC.get(),
        dealerStandTC.get(),
        resplitAcesTC.get(),
        basicStratDeviationsTC.get(),
        decks.get(),
    )
    
    playerEdge = str('{: .3f}'.format(float(houseText) + (-0.5) * trueCount) + "%")

    playerEdgeLabel.configure(text = playerEdge)
    playerEdgeLabel.update_idletasks()
    stdDevLabel.configure(text = stdDevText)
    stdDevLabel.update_idletasks()

    graphFrame2.destroy()
    if dealerStandTC.get() == 1:
        graphFrame2 = tk.Frame(tab2)
        t = Chart(graphFrame2, 'hit')
        graphFrame2.place(x = 900, y = 20)
    else:
        graphFrame2 = tk.Frame(tab2)
        t = Chart(graphFrame2, 'stand')
        graphFrame2.place(x = 900, y = 20)


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
).place(x=20, y=100)
tc2 = ttk.Checkbutton(
    tab2,
    text="Late Surrender Allowed",
    variable=lateSurrenderTC,
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc,
).place(x=20, y=170)
tc3 = ttk.Checkbutton(
    tab2, text="Double After Split", 
    variable=doubleAfterSplitTC,
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc,
).place(x=20, y=240)
tc4 = ttk.Checkbutton(
    tab2,
    text="Dealer Stands on soft 17 ",
    variable=dealerStandTC,
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc
).place(x=20, y=310)
tc5 = ttk.Checkbutton(
    tab2, text="Resplit aces", 
    variable=resplitAcesTC, 
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc
).place(x=20, y=380)
tc6 = ttk.Checkbutton(
    tab2,
    text="Basic Startegy Deviations",
    variable=basicStratDeviationsTC,
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc
).place(x=20, y=450)

helpButton = ttk.Button(tab2, image=helpPhoto, command=openWebsite).place(
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

l1 = tk.Label(tab3, text="Current Card(s):")
l2 = tk.Label(tab3, text="")
l3 = tk.Label(tab3, text="Decks Remaining:")
l4 = tk.Label(tab3, text="Current Bet:")
l5 = tk.Label(tab3, text="Reset page")


def startStream():
    global loadingBar
    loadingBar.place(x=220,y=450)
    loadingBar.start(10)

    # Change Buttons
    startStream.place(x=2000, y=800)
    endStream.place(x=1275, y=600)

    # Start/Stop Variables
    global stopIR
    stopIR = 0

    # Start thread for IR 
    T1 = threading.Thread(target=RunIR)
    T1.start()
    


def RunIR():
    detector = IR()
    loadingBar.destroy()
    # print("Starting with number" + str(playerIR.get()))
    
    # Frame counter for running count
    framecount = 0
    currentHand = []
    previousHand = []

    rules = RuleSet(8, 0.75, 10, 1000, late_surrender=True)
    table = TableIR(0, rules)
    player = PlayerIR(0, 5000000)
    table.add_player(0, player) 

    table.rules.hit_split_aces = True
    table.rules.resplit_aces = True
    dealer_upcard = ''
    player_hands = []


    frame_count = 0
    while stopIR == 0:
        frame_count+=1
        ret = detector(playerIR.get())
        if not ret:
            continue
        hands, img = ret
        im = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        im = Image.fromarray(im)
        im = ImageTk.PhotoImage(image=im)
        lmain.configure(image=im)
        lmain.update_idletasks()
        

        valid_up = False
        valid_hands = False
        num_hands = 0
        for hand in hands:
            if len(hand) == 1 and hand[0] != '': # valid dealer card
                valid_up = True
                num_hands += 1

            if len(hand) >= 2 and hand[0] != '' and hand[1] != '':
                valid_hands = True
                num_hands += 1


        if valid_up and valid_hands and num_hands >= playerIR.get():

            player_hands = []
            all_actions = []
        
            for hand in hands:
                # print(hand)
                if len(hand) == 1: # dealer hand, only 1 card
                    dealer_upcard = hand[0]
                    table.dealer.hand = Hand([Card(dealer_upcard, 's')])
                    continue
                # otherwise player hand
                this_hand = []
                for card in hand:
                    this_hand.append(Card(card, 's'))
                player_hands.append(Hand(this_hand))

            player.hands = player_hands # update player object's hand


            # dealermsg = (f"dealer upcard is: {dealer_upcard} \n")
            # st.insert('end', dealermsg)
            for i in range(len(player_hands)):

                action = table.get_player_action(player, i)
                # print(action)
                all_actions.append(action)
    
            # # print(all_actions)
            hand_value_tuples = []
            for hand in player_hands:
                hand_value_tuples.append(hand.get_hand_value())

            msg = (f"Upcard: {dealer_upcard} \n")
            q = 0
            for tuple in hand_value_tuples:
                msg += f'   {tuple[0]} {tuple[1]} should {all_actions[q]} \n'
                q +=1
            msg += '\n\n'
            # msg = (f'{} ' + str(all_actions) + "\n")
            # msg = ('All actions: ' + str(all_actions) + "\n")
            if frame_count % 9 == 0:
                st.insert('end', msg)
                st.yview(tk.END)
                # st.update_idletasks()
            
        # lmain.update_idletasks()

    cv2.destroyAllWindows()
    lmain.configure(image=placeholdPhoto) 





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

playerIR = tk.IntVar(tab3, 2)
# playerIR.set(tab3, 2)
ttk.Label(tab3, text="Number of hands", font=(default_font, 15)).place(x=1000, y = 600)
# Radio buttons return one more then label say to compensate for dealer 
t1 = ttk.Radiobutton(tab3, text="1", variable=playerIR, value=2,)
t2 = ttk.Radiobutton(tab3, text="2", variable=playerIR, value=3,)
t3 = ttk.Radiobutton(tab3, text="3", variable=playerIR, value=4,)

t1.place(x=1000, y=620)
t2.place(x=1040, y=620)
t3.place(x=1080, y=620)
# t1.invoke()



startStream = ttk.Button(tab3, text="Start Livefeed", padding=18, width = 17, command=startStream)
startStream.place(x=1275, y=600)
endStream = ttk.Button(tab3, text="End Livefeed", padding=18,  width = 17,command=endStream)

# trueCountLabel = ttk.Label(tab3, text="True Count:").place(x=10, y=600)
# runningCountLabel = ttk.Label(tab3, text="Running Count:").place(x=10, y=650)
# trueCountLabelBox = ttk.Label(tab3, text=0, borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
# trueCountLabelBox.place(x=200, y=610)
# runningCountLabelBox = ttk.Label(tab3, text=0, borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
# runningCountLabelBox.place(x=200, y=660)

##############################
# 						     #
#     Simulator components   #
# 						     #
##############################

#####TODO CHANGE TO SIMULATOR SPECIFIC INFO PAGE

graphFrame = tk.Frame(tab4, width='1000', height='500')

placeholderImageGraph = Image.open("Resources/images/graphPlaceholder.png")
placeholdPhotoGraph = ImageTk.PhotoImage(placeholderImageGraph.resize((1000, 562), Image.ANTIALIAS))

graphFrame.place(x=520, y = 60)

palceholdLabel = ttk.Label(graphFrame, borderwidth=2 , relief="solid")
palceholdLabel.grid(row=0, column=0, columnspan=15)
palceholdLabel.configure(image=placeholdPhotoGraph)
palceholdLabel.config(borderwidth=3, relief=tk.SOLID)

tk.Label(tab4, text = 'Settings:', font=(default_font, 30)).place(x= 10, y = 20)

bankrollvsTime = []

def runSim():
    global progress
    num_decks = 8
    
    num_players = current_valueNP.get()
    print(num_players)
    deck_pen = 0.75
    min_bet = 10
    max_bet = 1000
    # Must be mod 500 or wont work 
    total_rounds_played = current_valueRP.get() - (current_valueRP.get() % 500)
    # print(total_rounds_played)
    start_stack_size = float(bankroll())
    # print(start_stack_size, current_valueBR.get())
    betting_units = current_valueBU.get()
    # print(betting_units)
    num_bins = 500

    

    player_list = []
    tables = []
    for i in range(num_players):
        tables.append(Table(num_decks, deck_pen, min_bet, max_bet))
        player_list.append(Player(i, start_stack_size, betting_units, '1-12'))
        player_list[i].take_seat(0, tables[i])

    player_ids = ['round']
    for player in player_list:
        player_ids.append(player._id)

    bank_over_time_df = df(columns=player_ids)

    my_array = np.array([tables[0].play_n_rounds(total_rounds_played, num_bins)])

    for i in range(len(player_list)):
        if i == 0:
            continue
        my_array = np.insert(my_array, i, tables[i].play_n_rounds(total_rounds_played, num_bins), axis=0)


    for i in range(num_bins):
        bank_over_time_df = bank_over_time_df.append({'round': i}, ignore_index=True)

    for i in range(len(player_list)):
        bank_over_time_df[i] = my_array[i]

    fig = plt.figure(figsize=(10, 6), dpi=101)
    fig.add_subplot(111)
    

    bank_over_time_df['round'] = bank_over_time_df['round']*(total_rounds_played/num_bins)
    for i in range(len(player_list)):
        plt.plot(bank_over_time_df['round'], bank_over_time_df[i])

    num_bankrupts = 0
    for table in tables:
        if table.player_list[0].stack_size <= 0:
            num_bankrupts +=1

    max_y = 0
    for i in range(len(player_list)):
        tmp = bank_over_time_df[i].max()
        if tmp > max_y:
            max_y = tmp


    fig.set_facecolor('xkcd:grey')
    canvas = FigureCanvasTkAgg(fig, graphFrame)
    canvas.draw()
    plt.axis([0,total_rounds_played, 0 , (max_y*1.25)])
    plt.text(1, max_y*1.2, f'Num players: {num_players}')
    plt.text(1, (max_y*1.2) - max_y/16, f'Num bankrupt players: {num_bankrupts}')
    plt.title('Change in Player Bankrolls Over Time')
    plt.xlabel("Rounds Played")
    plt.ylabel("Bankroll in Dollars")
    progress.stop()
    canvas.get_tk_widget().place(x=0,y=0)
    



# Rule Variatiions
insurance = tk.IntVar()
lateSurrender = tk.IntVar()
doubleAfterSplit = tk.IntVar()
dealerStand = tk.IntVar()
resplitAces = tk.IntVar()
basicStratDeviations = tk.IntVar()


current_valueBU = tk.IntVar(value = 10)
current_valueBR = tk.IntVar(value = 0)
current_valueRP = tk.IntVar(value = 0)
current_valueNP = tk.IntVar(value = 1)

# Functions for Bankroll slider

def bankroll():
    val = current_valueBR.get()
    tmp = math.pow(val, 2)
    return str('{: .1f}'.format(tmp))

def slider_changedBR(event):
    s1Label = ttk.Label(tab4, text=bankroll(), borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
    s1Label.place(x=355, y=105)
    s1Label.configure(text=bankroll())
    s1Label.update_idletasks()

# Betting Units Slider
def slider_changedBU(event):
    s2Label = ttk.Label(tab4, text=current_valueBU, borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
    s2Label.place(x=355, y=185)
    s2Label.configure(text=current_valueBU.get())

# Function for rounds played slider

def slider_changedRP(event):
    s3Label = ttk.Label(tab4, text=current_valueRP, borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
    s3Label.place(x=355, y=265)
    s3Label.configure(text=current_valueRP.get())
    s3Label.update_idletasks()

def slider_changedNP(event):
    s4Label = ttk.Label(tab4, text=current_valueNP, borderwidth=3, relief="solid", width = 8, anchor=CENTER, font=(default_font, 17))
    s4Label.place(x=355, y=345)
    s4Label.configure(text=current_valueNP.get())
    s4Label.update_idletasks()    

# Sliders
s1 = ttk.Scale(tab4, from_=100, to=1000, orient="horizontal",command=slider_changedBR, variable=current_valueBR)
s1.set(0)
s1.place(x=240, y=110)

s2 = ttk.Scale(tab4, from_=10, to=1000, orient="horizontal", command=slider_changedBU, variable=current_valueBU)
s2.set(0.999)
s2.place(x=240, y=190)

s3 = ttk.Scale(tab4, from_=500, to=100000, orient="horizontal", command = slider_changedRP, variable = current_valueRP)
s3.set(0)
s3.place(x=240, y=270)

s4 = ttk.Scale(tab4, from_=1, to=10, orient="horizontal", command = slider_changedNP, variable = current_valueNP)
s4.set(0)
s4.place(x=240, y=350)


# Slider Labels
s1Label = ttk.Label(tab4, text="Starting Bankroll:").place(x=10, y=100)
s2Label = ttk.Label(tab4, text="Betting Units:").place(x=10, y=180)
s3Label = ttk.Label(tab4, text="Rounds Played:").place(x=10, y=260)
s4Label = ttk.Label(tab4, text="Number Players:").place(x=10, y=340)

# Progress Bar
progress = ttk.Progressbar(tab4, orient=HORIZONTAL, length=300, mode="indeterminate")
progress.place(x=70, y=520)

# Step Function to iterate loading bar 
fig = plt.figure()

def runGraph():
    global progress
    progress.start(10)
    runSim()
    # T2 = threading.Thread(target=runSim)
    # T2.start()

# Run Button
runButton = ttk.Button(tab4, text="Run", padding=19, command=runGraph)
runButton.place(x=150, y=560)


root.mainloop()
