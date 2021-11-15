# # TODO
# Welcome:
#   Help button 
# Strat:
#   Bubble chart/ matrix (longer in width and height)--Maybe matplotliob?
#  Live:
#   Replicate side bar of browser game
#   	-Cards in hard
#   	-Suggesstion
#   		-Hit, stand double
#   insurance 
#   True count
#   Expected value
#   Running Count
#   Starting decks? (Disable livefeed until > 0 1-8)


# Sim:
#   Empty graph before gen
#   bankroll go to 10mil
#   Rounds played label

#   Buttons
#   Add player
#   Add table
#   clear all 




from logging import currentframe
import tkinter as tk
from tkinter import Button, IntVar, StringVar, ttk
from tkinter import font
from tkinter.constants import ANCHOR, BOTH, CENTER, DISABLED, HORIZONTAL, RIDGE, S, VERTICAL, Y
from tkinter.font import Font, nametofont
import webbrowser
import time
import cv2
import numpy as np
import math
import threading


# Imported for Images
from PIL import ImageTk, Image

# For mathlib charts
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

##############
# DEMO ONLY IMPORTS
from Resources.simulator.blackjack_hi_low import Table
from Resources.simulator.player import Player
from Resources.simulator.dealer import Dealer
from Resources.simulator.card import Card
from Resources.simulator.hand import Hand

from Resources.houseEdgeCalc.EdgeCalc import edgeCalc

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

def trueCountDown():
    global trueCount
    if trueCount <= 0:
        pass
    else:
        trueCount -= 1
        updateText = "True Count: " + str(trueCount)
        trueCountLabel.configure(text=updateText)
        trueCountLabel.update_idletasks()
        runEdgeCalc()


def trueCountUp():
    global trueCount
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

# Label GEts updated by TCUp  and TCDown
trueCountLabel = ttk.Label(tab2, text="True Count: 0")
trueCountLabel.place(x=475, y=150)

##
##EDGE CALC SIDE
##
houseEdgeTag = ttk.Label(tab2, text="House Edge:", font=(default_font, 17))
houseEdgeTag.place(x=20, y=340)
stdDevTag = ttk.Label(tab2, text="Standard Deviation:", font=(default_font, 17))
stdDevTag.place(x=20, y=375)


houseEdgeLabel = ttk.Label(tab2, text="0", borderwidth=3, relief="solid", width = 6, anchor=CENTER, font=(default_font, 17))
houseEdgeLabel.place(x=230, y=340)
stdDevLabel = ttk.Label(tab2, text="0", borderwidth=3, relief="solid", width = 6, anchor= CENTER, font=(default_font, 17))
stdDevLabel.place(x=230, y=375)

def runEdgeCalc():
    houseText, stdDevText = edgeCalc(
        insuranceTC.get(),
        lateSurrenderTC.get(),
        doubleAfterSplitTC.get(),
        dealerStandTC.get(),
        resplitAcesTC.get(),
        basicStratDeviationsTC.get(),
        decks.get(),
    )
    
    houseEdgeLabel.configure(text = houseText)
    houseEdgeLabel.update_idletasks()
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


tree = ttk.Treeview(tab2)
tree.place(x=1180, y=200)
# Inserted at the root, program chooses id:
tree.insert('', 'end', 'widgets', text='Widget Tour')
 
# Same thing, but inserted as first child:
tree.insert('', 0, 'gallery', text='Applications')

# Treeview chooses the id:
id = tree.insert('', 'end', text='Tutorial')

# Inserted underneath an existing node:
tree.insert('widgets', 'end', text='Canvas')
tree.insert(id, 'end', text='Tree')

###########################
# 						  #
#   Livefeed components   #
# 						  #
###########################

stopIR = 0

imageFrame = tk.Frame(tab3, width='1000', height='500')

placeholderImage = Image.open("Resources/images/webcamPlacehold.png")
placeholdPhoto = ImageTk.PhotoImage(placeholderImage.resize((1000, 500), Image.ANTIALIAS))


imageFrame.place(x=20, y = 50)
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

    

def RunIR():

    global stopIR, loadingBar
    
    camera = cv2.VideoCapture(0)

    # Preparing variables for spatial dimensions of the frames
    h, w = None, None
    # h, w = 1000, 500

    with open("Resources/cardDetection/classes.names") as f:
        # Getting labels reading every line
        # and putting them into the list
        labels = [line.strip() for line in f]

    network = cv2.dnn.readNetFromDarknet(
        "Resources/cardDetection/train.cfg", "Resources/cardDetection/card_chip.weights"
    )

    network.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    network.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    # Getting list with names of all layers from YOLO v3 network
    layers_names_all = network.getLayerNames()


    layers_names_output = [
        layers_names_all[i[0] - 1] for i in network.getUnconnectedOutLayers()
    ]

    # Setting minimum probability to eliminate weak predictions
    probability_minimum = 0.5

    threshold = 0.3

    colours = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

    # gives pairs of cards
    def pairs(results):
        cards = []
        for i, (N, X, Y) in enumerate(results):
            dist = 1000000000
            best_index = i
            for j, (n, x, y) in enumerate(results):
                cur_dist = abs(X - x) + abs(Y - y)
                if i != j:
                    if cur_dist < dist:
                        dist = cur_dist
                        best_index = j
            cards.append((best_index))

        return (
            {
                str(sorted((i, j))): (results[i][0], results[j][0])
                for i, j in enumerate(cards)
                if cards[j] == i
            }
        ).values()

    # Defining loop for catching frames
    loadingBar.stop()
    loadingBar.destroy()
    while stopIR == 0:
        
        
        # Capturing frame-by-frame from camera
        _, frame = camera.read()


        if w is None or h is None:
            # Slicing from tuple only first two elements
            try:
                h, w = frame.shape[:2]
            except:
                 tk.messagebox.showerror('Camera Error', 'Error: Make sure your camera is connected!')

        blob = cv2.dnn.blobFromImage(
            frame, 1 / 255.0, (416, 416), swapRB=True, crop=False
        )


        network.setInput(blob)  
        start = time.time()
        output_from_network = network.forward(layers_names_output)
        end = time.time()


        bounding_boxes = []
        confidences = []
        class_numbers = []
        
        # Going through all output layers after feed forward pass
        for result in output_from_network:
            # Going through all detections from current output layer
            for detected_objects in result:
                # Getting 80 classes' probabilities for current detected object
                scores = detected_objects[5:]
                # Getting index of the class with the maximum value of probability
                class_current = np.argmax(scores)
                # Getting value of probability for defined class
                confidence_current = scores[class_current]

                # Eliminating weak predictions with minimum probability
                if confidence_current > probability_minimum:
                    box_current = detected_objects[0:4] * np.array([w, h, w, h])
                    x_center, y_center, box_width, box_height = box_current
                    x_min = int(x_center - (box_width / 2))
                    y_min = int(y_center - (box_height / 2))

                    bounding_boxes.append(
                        [x_min, y_min, int(box_width), int(box_height)]
                    )
                    confidences.append(float(confidence_current))
                    class_numbers.append(class_current)
        
        results = cv2.dnn.NMSBoxes(
            bounding_boxes, confidences, probability_minimum, threshold
        )

        send = []
        
        if len(results) > 0:
            # Going through indexes of results
            for i in results.flatten():

                x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
                box_width, box_height = bounding_boxes[i][2], bounding_boxes[i][3]

                colour_box_current = colours[class_numbers[i]].tolist()

                # Drawing bounding box on the original current frame
                cv2.rectangle(
                    frame,
                    (x_min, y_min),
                    (x_min + box_width, y_min + box_height),
                    colour_box_current,
                    2,
                )

                # Preparing text with label and confidence for current bounding box
                text_box_current = "{}: {:.4f}".format(
                    labels[int(class_numbers[i])], confidences[i]
                )

                # Putting text with label and confidence on the original image
                cv2.putText(
                    frame,
                    text_box_current,
                    (x_min, y_min - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    colour_box_current,
                    2,
                )

                x, y, width, heighth = bounding_boxes[i]
                

                print(
                    "Location of",
                    labels[int(class_numbers[i])],
                    "=",
                    x,
                    y,
                    "Confidence =",
                    text_box_current[3:],
                )

                send.append((labels[int(class_numbers[i])], x, y))
            print("The pairs are", pairs(send))
            running_Count = labels[int(class_numbers[i])]
            updateRunningCount(running_Count)
            
        
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        im = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=im.resize((1000, 588)))
        lmain.configure(image=imgtk)
        lmain.update_idletasks()
        
        
        

    # Releasing camera
    camera.release()
    # Destroying all opened OpenCV windows
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

    startStream.place(x=2000, y=800)
    endStream.place(x=975, y=650)

    l1.place(x=675, y=50)
    l2.place(x=880, y=50)

    


    # Start/Stop Variables
    global stopIR
    global T1
    stopIR = 0
    T1 = threading.Thread(target=RunIR)
    T1.start()
  


def endStream():
    global stopIR
    stopIR = 1
    
    lmain.update_idletasks()
    # Change Buttons
    endStream.place(x=2000, y=800)
    startStream.place(x=2000, y=800)


startStream = ttk.Button(tab3, text="Start Livefeed", padding=18, command=startStream)
startStream.place(x=1275, y=600)
endStream = ttk.Button(tab3, text="End Livefeed", padding=15, command=endStream)

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
# MathLib Testing Seciton
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
    #     demoDay()
    #     return
        
        


    rounds = np.linspace(0, total_rounds_played, retstep=True, num=num_bins, dtype=int, axis=0)
    # print("bak_roll = " + str((bankroll_over_time)))
    # print("rounds[0]_len = " + str((rounds[0])))
    # plt.scatter(rounds[0], bankroll_over_time)
    # plt.xlabel("rounds")
    # plt.ylabel("bankroll")
    # plt.show(block=True)
    
    global bankrollvsTime


    bankrollvsTime = DataFrame(data = np.column_stack((rounds[0],bankroll_over_time)), columns=['Rounds', 'Bankroll']).groupby("Rounds").sum()

    #####
 
    # progress.stop()
    # MathPlotLib Graph
    figure2 = plt.Figure(figsize=(9, 4), dpi=65)

    ax2 = figure2.add_subplot(111)

    line2 = FigureCanvasTkAgg(figure2, tab4)

    line2.get_tk_widget().place(x=350, y=25)

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

#Functions for Risk of Ruin slider
def riskOfRuin():
    # print(current_value.get())
    tmp = -math.log(current_valueROR.get(), 2)
    ror = math.exp(-2/tmp)
    return str('{: .3f}'.format(ror))
    

def slider_changedRor(event):
    s2Label = ttk.Label(tab4, text=riskOfRuin(), borderwidth=3, relief="solid", width = 6, anchor=CENTER, font=(default_font, 17))
    s2Label.place(x=355, y=555)
    s2Label.configure(text=riskOfRuin())

def bankroll():
    # print(current_valueBR.get())
    val = current_valueBR.get()
    tmp = math.pow(val, 4)
    return str('{: .1f}'.format(tmp)) 


def slider_changedBR(event):
    s1Label = ttk.Label(tab4, text=bankroll(), borderwidth=3, relief="solid", width = 6, anchor=CENTER, font=(default_font, 17))
    s1Label.place(x=355, y=505)
    s1Label.configure(text=bankroll())
    s1Label.update_idletasks()

# tab2, text="0", borderwidth=3, relief="solid", width = 6, anchor=CENTER, font=(default_font, 17)
# Sliders
s1 = ttk.Scale(tab4, from_=0, to=47, orient="horizontal",command=slider_changedBR, variable=current_valueBR)
s1.set(0)
s1.place(x=240, y=510)

s2 = ttk.Scale(tab4, from_=0.999, to=0.5, orient="horizontal", command=slider_changedRor, variable=current_valueROR)
s2.set(0.999)
s2.place(x=240, y=560)

s3 = ttk.Scale(tab4, from_=0, to=5000000, orient="horizontal")
s3.set(0)
s3.place(x=240, y=610)

# Slider Labels
s1Label = ttk.Label(tab4, text="Starting Bankroll:").place(x=10, y=500)
s2Label = ttk.Label(tab4, text="Risk of Ruin:").place(x=10, y=550)
s3Label = ttk.Label(tab4, text="Rounds Played:").place(x=10, y=600)


# Progress Bar
progress = ttk.Progressbar(tab4, orient=HORIZONTAL, length=300, mode="indeterminate")
progress.place(x=475, y=305)

# Step Fucntion to iterate loading bar 


def runGraph():
    global progress
    progress.start(10)
    T2 = threading.Thread(target=demoDay)
    T2.start()

# Run Button
runButton = ttk.Button(tab4, text="Run", padding=15, command=runGraph)
runButton.place(x=575, y=330)

root.mainloop()
