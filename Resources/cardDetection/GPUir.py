from __future__ import division
import time
import torch 
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import cv2 
from Resources.cardDetection.util import *
from Resources.cardDetection.darknet import Darknet
# from preprocess import prep_image, inp_to_image
import pandas as pd
import random 
import argparse
import pickle as pkl
from typing import NamedTuple, Tuple
from dataclasses import dataclass
from sklearn.cluster import KMeans
from collections import defaultdict
from collections import Counter
from math import ceil
Point = Tuple[int, int]

CUDA = torch.cuda.is_available()
classes = load_classes('Resources/cardDetection/classes.names')
colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')

@dataclass
class Detection():
    label: int
    TopLeft: Point
    BotRight: Point
    pair: int = None

    #looks for overlap in prior BB
    def intersection(self, X):
        #Given points from BB
        (c1_x, c1_y), (c2_x, c2_y) = self.TopLeft, self.BotRight
        (c3_x, c3_y), (c4_x, c4_y) = X.TopLeft, X.BotRight

        BL_1_x, BL_1_y = c1_x, c2_y
        TR_1_x, TR_1_y = c2_x, c1_y 

        BL_2_x, BL_2_y = c3_x, c4_y
        TR_2_x, TR_2_y = c4_x, c3_y 

        width = min(TR_1_x, TR_2_x) - max(BL_1_x, BL_2_x)
        height = min(TR_1_y, TR_2_y) - max(BL_1_y, BL_2_y)

        if width > 0 and height > 0:
          area = width * height
        else:
          area = 0 # no intersection

        return area

    #Euclidean distance
    def distance(self, X):
        x1, y1 = self.BotRight
        x2, y2 = X.BotRight

        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    #If its not its own BB or the label from the BB is not the same as the desired BB label, cant be a pair
    def is_eligable(self, X):
        if self.label != X.label or self == X:
            return False

        x1, y1 = self.BotRight
        x2, y2 = X.TopLeft

        #We do a cone scope, making sure its to the right and down from the other BB
        return (x2 > x1 and y2 > y1)  or (x2 < x1 and y2 < y1)

    def features(self):

        return self.TopLeft

    def __str__(self):
        card_names = ['K','Q','J','10','9','8','7','6','5','4','3','2','A','back']
        return card_names[self.label]

#frame by frame pass through
def prep_image(img, inp_dim):
    """
    Prepare image for inputting to the neural network. 
    
    Returns a Variable 
    """

    orig_im = img
    dim = orig_im.shape[1], orig_im.shape[0]
    img = cv2.resize(orig_im, (inp_dim, inp_dim))
    img_ = img[:,:,::-1].transpose((2,0,1)).copy()
    img_ = torch.from_numpy(img_).float().div(255.0).unsqueeze(0)
    return img_, orig_im, dim

#Writes for each of the BB
def write(x, img):
    c1 = tuple(x[1:3].int())
    c1 = int(c1[0]), int(c1[1])
    c2 = tuple(x[3:5].int())
    c2 = int(c2[0]), int(c2[1])
    cls = int(x[-1])
    # print("CLS: "+str(cls))
    label = "{0}".format(classes[cls])
    color = random.choice(colors)
    cv2.rectangle(img, c1, c2,(255,0,0), 1)
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
    c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
    cv2.rectangle(img, c1, c2,(0,0,0), -1)
    cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225,255,255], 1);
    return img

#filters out each of the repeating BB from the same card
def filter(hand):
    freq = Counter(hand)
    ret = []
    #print("HAND IS ", hand)
    for card, count in freq.items():

        #need to filter out the 2nd BB

        #print('FREQ.ITEMS = ', freq.items(),'\n\n')
        #print('COUNT', count, '\n\n')
        ret += [card] * ceil(int(count)//2)

    return ret


#For easy access in other files
class IR:
    cfgfile = "Resources/cardDetection/train.cfg"
    weightsfile = "Resources/cardDetection/card_chip.weights"
    num_classes = 18

    confidence = 0.5
    nms_thesh = 0.3
    start = 0
    def __init__(self):
    
        
        
        model = Darknet(self.cfgfile)
        model.load_weights(self.weightsfile)
        
        model.net_info["height"] = 640#800#640
        self.inp_dim = int(model.net_info["height"])
        
        #assert inp_dim % 32 == 0 
        #assert inp_dim > 32

        if CUDA:
            model.cuda()
                
        model.eval()
        
        cap = cv2.VideoCapture(0)
        
        assert cap.isOpened(), 'Cannot capture source'
        self.cap = cap
        self.model = model

    #Whenever IR is called it executes this
    def __call__(self, num_players):
        if not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()

        if not ret:
            return None

        img, orig_im, dim = prep_image(frame, self.inp_dim)
        im_dim = torch.FloatTensor(dim).repeat(1,2)   
        
        #Checks for GPU   
        if CUDA:
            im_dim = im_dim.cuda()
            img = img.cuda()
        
        output = self.model(Variable(img), CUDA)
        output = write_results(output, self.confidence, self.num_classes, nms = True, nms_conf = self.nms_thesh)

        if type(output) == int:
            return [], orig_im

        output[:,1:5] = torch.clamp(output[:,1:5], 0.0, float(self.inp_dim))/self.inp_dim
            
        output[:,[1,3]] *= frame.shape[1]
        output[:,[2,4]] *= frame.shape[0]
        
        list(map(lambda x: write(x, orig_im), output))

        #Detection stores[label and the 4 points of the BB] : stores 8 values while a card is in frame
        detections = [Detection(int(x[7]), (int(x[1]),int(x[2])), (int(x[3]), int(x[4]))) for x in output if len(x) == 8]
        
        #used to detect eligable BB
        for x in detections:
            canidates = (d for d in detections if x.is_eligable(d))
            minimum = 100000000
            for y in canidates: #figure out how to bypass back, x.label == 13
                if x.distance(y) < minimum:
                    minimum = x.distance(y)
                    x.pair = y

        #Detections allows for singular BB on each card, but not sure of the flaws it could create
        #cards = detections
        cards = [d for d in detections if d.pair]

        if len(cards) < num_players:
            return [], orig_im
        data = [c.features() for c in cards]
        data_y = KMeans(n_clusters=num_players).fit_predict(data)
        players = [[] for _ in range(num_players)]
        for card, y in zip(cards, data_y):
            players[y].append(card)

        players.sort(key=lambda x: x[0].TopLeft[0])
        return_value = [filter([str(card) for card in hand]) for hand in players]

        return return_value, orig_im



if __name__ == '__main__':
    cfgfile = "../train.cfg"
    weightsfile = "../card_chip.weights"
    #cfgfile = "../train.cfg"
    #weightsfile = "../card_chip.weights"
    num_classes = 18

    confidence = 0.5
    nms_thesh = 0.3
    start = 0
    CUDA = torch.cuda.is_available()

    
    #classes for BB
    bbox_attrs = 5 + num_classes
    
    #Model
    model = Darknet(cfgfile)
    model.load_weights(weightsfile)
    
    model.net_info["height"] = 640
    inp_dim = int(model.net_info["height"])
    
    assert inp_dim % 32 == 0 
    assert inp_dim > 32

    #For GPU access
    if CUDA:
        model.cuda()

    model.eval()

    #camera feed
    cap = cv2.VideoCapture(0)
    
    #throws an error if no camera source
    assert cap.isOpened(), 'Cannot capture source'
    
    frames = 0
    start = time.time()

    #Loops while camera is opened
    while cap.isOpened():
        
        ret, frame = cap.read()
        if ret:
            
            img, orig_im, dim = prep_image(frame, inp_dim)
            
            im_dim = torch.FloatTensor(dim).repeat(1,2)                        
            
            
            if CUDA:
                im_dim = im_dim.cuda()
                img = img.cuda()
            
            #feeds model each frame
            output = model(Variable(img), CUDA)
            output = write_results(output, confidence, num_classes, nms = True, nms_conf = nms_thesh)

            if type(output) == int:
                frames += 1
                print("FPS of the video is {:5.2f}".format( frames / (time.time() - start)))
                cv2.imshow("frame", orig_im)
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    break
                continue
            

        
            output[:,1:5] = torch.clamp(output[:,1:5], 0.0, float(inp_dim))/inp_dim
            
#            im_dim = im_dim.repeat(output.size(0), 1)
            output[:,[1,3]] *= frame.shape[1]
            output[:,[2,4]] *= frame.shape[0]

            #classes get loaded along side color of BB
            classes = load_classes('../classes.names')
            #colors = pkl.load(open("pallete", "rb"))
            colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')
            
            list(map(lambda x: write(x, orig_im), output))

            #Detections grabs label and 4 points of BB
            detections = [Detection(int(x[7]), (int(x[1]),int(x[2])), (int(x[3]), int(x[4]))) for x in output if len(x) == 8]
            
            cv2.imshow("frame", orig_im)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            frames += 1
            #print("FPS of the video is {:5.2f}".format( frames / (time.time() - start)))

            #checks for "eligable" pairs, meaning it excludes itself and non valid labels
            for x in detections:
                canidates = [d for d in detections if x.is_eligable(d)]
                minimum = 100000
                for y in canidates:
                    if x.distance(y) < minimum:
                        minimum = x.distance(y)
                        x.pair = y

            cards = [d for d in detections if d.pair]

            if len(cards) < 2:
                continue
            data = np.array([c.features() for c in cards])
            data_y = KMeans(n_clusters=2, random_state=0).fit_predict(data)
            players = defaultdict(list)
            for card, y in zip(cards, data_y):
                players[y].append(card)

            return_value = [filter([str(card) for card in hand]) for hand in players.values()]
            print(return_value)





            
        else:
            break
    

    
