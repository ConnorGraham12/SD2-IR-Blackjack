
# Importing needed libraries
import numpy as np
import cv2
import time


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

        # Showing results obtained from camera in Real Time

        # Showing current frame with detected objects
        # Giving name to the window with current frame
        # And specifying that window is resizable
        cv2.namedWindow("YOLO v3 Real Time Detections", cv2.WINDOW_NORMAL)
        # Pay attention! 'cv2.imshow' takes images in BGR format
        cv2.imshow("YOLO v3 Real Time Detections", frame)

        # Breaking the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Releasing camera
    camera.release()
    # Destroying all opened OpenCV windows
    cv2.destroyAllWindows()
