# # TODO
# Get open CV window inside gui
# experiment with packing to make gui resizable
# get edge calc working
# light/dark mode
# tk sliders to ttk


from logging import currentframe
import tkinter as tk
from tkinter import Button, StringVar, ttk
from tkinter import font
from tkinter.constants import ANCHOR, DISABLED, HORIZONTAL, S
from tkinter.font import Font, nametofont
import webbrowser
import time
import cv2
import numpy as np

# Imported for Images
from PIL import ImageTk, Image

# For mathlib charts
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import external functions
# from CardDetect.test3 import startWebcam
# from cardDetection.carddetection import RunIR
from houseEdgeCalc.EdgeCalc import edgeCalc

root = tk.Tk()

# Window Name
root.title("SD Blackjack")

# Icon for window
root.iconphoto(False, tk.PhotoImage(file="Resources/favicon2.png"))
helpImage = Image.open("Resources/questionMark.png")
helpPhoto = ImageTk.PhotoImage(helpImage.resize((40, 40), Image.ANTIALIAS))

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


# Logo
image1 = Image.open("Resources/blackjackLogo.png")
photo1 = ImageTk.PhotoImage(image1.resize((350, 252), Image.ANTIALIAS))
imgLabel1 = ttk.Label(tab1, image=photo1).place(x=300, y=20)

# Lables
ttk.Label(tab1, text="The ultimate card counting trainer.").place(x=325, y=285)
ttk.Label(
    tab1,
    text="Creators: Connor Graham, John Murphy, Tyler Vandermate, Paul Vicino, Graham West  ",
).place(x=150, y=370)

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
        trueCountLabel.update()


def trueCountUp():
    global trueCount
    trueCount += 1
    updateText = "True Count: " + str(trueCount)
    trueCountLabel.configure(text=updateText)
    trueCountLabel.update()


#####TODO CHANGE TO STRATEGY CHARTS SPECIFIC INFO PAGE
def openWebsiteStrat():
    webbrowser.open(
        "https://sd1-blackjack.herokuapp.com/login?next=%2F", new=0, autoraise=True
    )


##
##CHART SIDE
##

image2 = Image.open("Resources/stratchart1.jpg")
photo2 = ImageTk.PhotoImage(image2.resize((280, 370), Image.ANTIALIAS))
imgLabel2 = ttk.Label(tab2, image=photo2).place(x=610, y=10)

# Up Increment
upButtonImg = Image.open("Resources/upArrow.png")
upButtonImg2 = ImageTk.PhotoImage(upButtonImg.resize((70, 40), Image.ANTIALIAS))
upButton = ttk.Button(tab2, image=upButtonImg2, command=trueCountUp).place(x=500, y=80)

# Down Increment
downButtonImg = Image.open("Resources/downArrow.png")
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
def runEdgeCalc():
    (
        edgeCalc(
            insuranceTC.get(),
            lateSurrenderTC.get(),
            doubleAfterSplitTC.get(),
            dealerStandTC.get(),
            resplitAcesTC.get(),
            basicStratDeviationsTC.get(),
            decks.get(),
        )
    )
    T1.insert(0, "test")
    T1.update()


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
ttk.Radiobutton(tab2, text="1", variable=decks, value=0).place(x=140, y=40)
ttk.Radiobutton(tab2, text="2", variable=decks, value=1).place(x=180, y=40)
ttk.Radiobutton(tab2, text="4", variable=decks, value=2).place(x=220, y=40)
ttk.Radiobutton(tab2, text="6", variable=decks, value=4).place(x=270, y=40)

# Check Buttons
tc1 = ttk.Checkbutton(
    tab2,
    text="Insurance",
    variable=insuranceTC,
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc,
).place(x=20, y=60)
tc2 = ttk.Checkbutton(
    tab2,
    text="Late Surrender Allowed",
    variable=lateSurrenderTC,
    onvalue=1,
    offvalue=0,
    command=runEdgeCalc,
).place(x=20, y=90)
tc3 = ttk.Checkbutton(
    tab2, text="Double After Split", variable=doubleAfterSplitTC, onvalue=1, offvalue=0
).place(x=20, y=120)
tc4 = ttk.Checkbutton(
    tab2,
    text="Dealer Stands on soft 17 ",
    variable=dealerStandTC,
    onvalue=1,
    offvalue=0,
).place(x=20, y=150)
tc5 = ttk.Checkbutton(
    tab2, text="Resplit aces", variable=resplitAcesTC, onvalue=1, offvalue=0
).place(x=20, y=180)
tc6 = ttk.Checkbutton(
    tab2,
    text="Basic Startegy Deviations",
    variable=basicStratDeviationsTC,
    onvalue=1,
    offvalue=0,
).place(x=20, y=210)
helpButton = ttk.Button(tab2, image=helpPhoto, command=openWebsiteStrat).place(
    x=910, y=10
)
T1 = tk.Label(tab2, text="    ", borderwidth=2, relief="solid")
T1.place(x=20, y=240)

###########################
# 						  #
#   Livefeed components   #
# 						  #
###########################


camera = cv2.VideoCapture(0)
imageFrame = tk.Frame(tab3, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
running_Count = []
def updateRunningCount():
    running_Count.append(2)
    l2.configure(text = running_Count)
    l2.update

def RunIR():

    camera = cv2.VideoCapture(0)

    # Preparing variables for spatial dimensions of the frames
    h, w = None, None

    with open("cardDetection/classes.names") as f:
        # Getting labels reading every line
        # and putting them into the list
        labels = [line.strip() for line in f]

    network = cv2.dnn.readNetFromDarknet(
        "cardDetection/train.cfg", "cardDetection/card_chip.weights"
    )

    network.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    network.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    # Getting list with names of all layers from YOLO v3 network
    layers_names_all = network.getLayerNames()

    # Getting only output layers' names that we need from YOLO v3 algorithm
    # with function that returns indexes of layers with unconnected outputs
    layers_names_output = [
        layers_names_all[i[0] - 1] for i in network.getUnconnectedOutLayers()
    ]

    # Setting minimum probability to eliminate weak predictions
    probability_minimum = 0.5

    # Setting threshold for filtering weak bounding boxes
    # with non-maximum suppression
    threshold = 0.3

    # Generating colours for representing every detected object
    # with function randint(low, high=None, size=None, dtype='l')
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
    while True:
        # Capturing frame-by-frame from camera
        _, frame = camera.read()

        # Getting spatial dimensions of the frame
        # we do it only once from the very beginning
        # all other frames have the same dimension
        if w is None or h is None:
            # Slicing from tuple only first two elements
            h, w = frame.shape[:2]

        # Getting blob from current frame
        # The 'cv2.dnn.blobFromImage' function returns 4-dimensional blob from current
        # frame after mean subtraction, normalizing, and RB channels swapping
        # Resulted shape has number of frames, number of channels, width and height
        # E.G.:
        # blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size, mean, swapRB=True)
        blob = cv2.dnn.blobFromImage(
            frame, 1 / 255.0, (416, 416), swapRB=True, crop=False
        )

        # Implementing forward pass with our blob and only through output layers
        # Calculating at the same time, needed time for forward pass
        network.setInput(blob)  # setting blob as input to the network
        start = time.time()
        output_from_network = network.forward(layers_names_output)
        end = time.time()

        # Showing spent time for single current frame
        # print('Current frame took {:.5f} seconds'.format(end - start))

        # Preparing lists for detected bounding boxes,
        # obtained confidences and class's number
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
                # Getting current bounding box coordinates,
                # its width and height
                x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
                box_width, box_height = bounding_boxes[i][2], bounding_boxes[i][3]

                # Preparing colour for current bounding box
                # and converting from numpy array to list
                colour_box_current = colours[class_numbers[i]].tolist()

                # # # Check point
                # print(type(colour_box_current))  # <class 'list'>
                # print(colour_box_current)  # [172 , 10, 127]

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
                #####TODO

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
            running_Count.append(labels[int(class_numbers[i])])
            updateRunningCount()
        # Showing results obtained from camera in Real Time

        # Showing current frame with detected objects
        # Giving name to the window with current frame
        # And specifying that window is resizable
        # cv2.namedWindow("YOLO v3 Real Time Detections", cv2.WINDOW_NORMAL)
        # Pay attention! 'cv2.imshow' takes images in BGR format
        # cv2.imshow("YOLO v3 Real Time Detections", frame)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        im = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=im)
        lmain.configure(image=imgtk)
        lmain.update()
        # Breaking the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Releasing camera
    camera.release()
    # Destroying all opened OpenCV windows
    cv2.destroyAllWindows()


l1 = tk.Label(tab3, text="Running Count:")
l2 = tk.Label(tab3, text="")
l3 = tk.Label(tab3, text="Decks Remaining:")
l4 = tk.Label(tab3, text="Current Bet:")
l5 = tk.Label(tab3, text="Reset page")


def changePage():
    l1.place(x=675, y=50)
    l1.update()
    l1.place(x=715, y=50)
    updateRunningCount()
    # RunIR()


startstream = ttk.Button(tab3, text="Start Livefeed", command=changePage).place(x=400, y=100)

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
data2 = {
    "Time": [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
    "Bankroll": [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3],
}
df2 = DataFrame(data2, columns=["Time", "Bankroll"])

# MathPlotLib Graph
figure2 = plt.Figure(figsize=(9, 4), dpi=60)
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, tab4)
line2.get_tk_widget().place(x=350, y=25)
df2 = df2[["Time", "Bankroll"]].groupby("Time").sum()
df2.plot(kind="line", legend=True, ax=ax2, color="r", marker="o", fontsize=10)
ax2.set_title("Time Vs. Bankroll")

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
# helpImage = Image.open('Resources/questionMark.png')
# helpPhoto = ImageTk.PhotoImage(helpImage.resize((40, 40), Image.ANTIALIAS))
helpButton = ttk.Button(tab4, image=helpPhoto, command=openWebsiteSim).place(
    x=910, y=10
)

# CheckButtons
c1 = ttk.Checkbutton(
    tab4, text="Insurance", variable=insurance, onvalue=1, offvalue=0
).place(x=20, y=40)
c2 = ttk.Checkbutton(
    tab4, text="Late Surrender Allowed", variable=lateSurrender, onvalue=1, offvalue=0
).place(x=20, y=70)
c3 = ttk.Checkbutton(
    tab4, text="Double After Split", variable=doubleAfterSplit, onvalue=1, offvalue=0
).place(x=20, y=100)
c4 = ttk.Checkbutton(
    tab4, text="Dealer Stands on soft 17 ", variable=dealerStand, onvalue=1, offvalue=0
).place(x=20, y=130)
c5 = ttk.Checkbutton(
    tab4, text="Resplit aces", variable=resplitAces, onvalue=1, offvalue=0
).place(x=20, y=160)
c6 = ttk.Checkbutton(
    tab4,
    text="Basic Startegy Deviations",
    variable=basicStratDeviations,
    onvalue=1,
    offvalue=0,
).place(x=20, y=190)

# Sliders
s1 = tk.Scale(tab4, from_=0, to=1000, orient="horizontal")
s1.set(0)
s1.place(x=170, y=230)

s2 = tk.Scale(tab4, from_=0, to=1000, orient="horizontal")
s2.set(0)
s2.place(x=170, y=280)

s3 = tk.Scale(tab4, from_=0, to=1000, orient="horizontal")
s3.set(0)
s3.place(x=170, y=330)

# Slider Labels
s1Label = ttk.Label(tab4, text="Starting Bankroll:").place(x=10, y=250)
s2Label = ttk.Label(tab4, text="Hands per hour:").place(x=10, y=300)
s3Label = ttk.Label(tab4, text="Hours Played:").place(x=10, y=350)
# Slider Values Labels
s1ValLabel = ttk.Label(tab4, text="Starting Bankroll:")
s2ValLabel = ttk.Label(tab4, text="Hands per hour:")
s3ValLabel = ttk.Label(tab4, text="Hours Played:")
# Progress Bar


progress = ttk.Progressbar(tab4, orient=HORIZONTAL, length=300, mode="determinate")
progress.place(x=475, y=275)


def step():
    for i in range(11):
        root.update_idletasks()
        progress["value"] += 10
        time.sleep(0.2)
    progress["value"] = 0


# Run Button
runButton = ttk.Button(tab4, text="Run", padding=15, command=step).place(x=575, y=300)


root.mainloop()
