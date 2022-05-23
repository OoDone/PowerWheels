from time import sleep
import numpy.core.multiarray
import cv2
import numpy as np
import math
import os
import threading

a = 1
b = 0.9
c = 0.8
d = 0.7
e = 0.6
f = 0.5
g = 0.4

testmode = 1 #to enable added features such as view and save on file

key = ''
start = False
global lastDirection
lastDirection = 5

class Vision: #(threading.Thread):
    def __init__(self, Logger, threadID):
        #threading.Thread.__init__(self)
        #self.threadID = threadID
        #self.name = name
        global logger
        global cap
        logger = Logger
        logger.info("Robot | Code: Vision.py Init")
        
        cap = cv2.VideoCapture(0)
        try:
            if not os.path.exists('data'):
                os.makedirs('data')
        except OSError:
            print ('Error: Creating directory of data')
            
        if testmode == 1:
            global F
            F = open("./data/imagedetails.txt",'a')
            F.write("\n\nNew Test \n")
        
    def run(self):
      logger.info("Starting " + self.name)
      self.startVision()
      logger.info("Exiting " + self.name)

    def forward(self): #... add onto the left
        global lastDirection
        lastDirection = 0
        m1_speed = 0.8 #mr
        m2_speed = a #ml
        #r.value = (m1_speed, m2_speed)
        logger.info("Vision: Clear To Go Forward")

    def backward(self):
        global lastDirection
        lastDirection = 1
        #r.reverse()
        logger.info("Vision: Clear To Go Backwards")

    def right(self):
        global lastDirection
        lastDirection = 2
        #r.right(speed=1)
        logger.info("Vision: Obstacle, Attempting To Go Right")
        #sleep(0.6) #0.5
        #forward()

 
    def left(self):
        global lastDirection
        lastDirection = 3
        #r.left(speed=1)
        logger.info("Vision: Obstacle, Attempting To Go Left")
        #sleep(0.6) #0.5
        #forward()

    def stop(self):
        m1_speed = 0.0
        m2_speed = 0.0
        global lastDirection
        lastDirection = 4
        #r.value = (m1_speed, m2_speed)
        logger.info("Vision: Obstacle?? Stopping")
        
    def getLastDirection(self):
        global lastDirection
        return lastDirection
   
    def calc_dist(self, p1,p2):

        x1 = p1[0]

        y1 = p1[1]

        x2 = p2[0]

        y2 = p2[1]
    
        dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)

        return dist


    def getChunks(self, l, n):

        """Yield successive n-sized chunks from l."""

        a = []

        for i in range(0, len(l), n):   

            a.append(l[i:i + n])

        return a



    def startVision(self):
        StepSize = 5
        currentFrame = 0
        logger.info("Starting Vision...")
        print("Start Vision")
        while(1):
            sleep(0.05)
            _,frame = cap.read()
            #if testmode == 1:
            name = './data/frame' + str(currentFrame) + '.jpg'
            nameC = './data/frame' + str(currentFrame) + 'C.jpg'
            nameB = './data/frame' + str(currentFrame) + 'B.jpg'
            print ('Creating...' + name)
        
            img = frame.copy()

            blur = cv2.bilateralFilter(img,9,40,40)
            #cv2.imwrite(nameB, blur)

            edges = cv2.Canny(blur,50,100)
            cv2.imwrite(nameC, edges)

            img_h = img.shape[0] - 1

            img_w = img.shape[1] - 1

            EdgeArray = []

            for j in range(0,img_w,StepSize):

                pixel = (j,0)

                for i in range(img_h-5,0,-1):

                    if edges.item(i,j) == 255:

                        pixel = (j,i)

                        break

                EdgeArray.append(pixel)


            for x in range(len(EdgeArray)-1):

                cv2.line(img, EdgeArray[x], EdgeArray[x+1], (0,255,0), 1)



            for x in range(len(EdgeArray)):

                cv2.line(img, (x*StepSize, img_h), EdgeArray[x],(0,255,0),1)


            chunks = self.getChunks(EdgeArray,int(len(EdgeArray)/3)) # 5

            max_dist = 0

            c = []

            for i in range(len(chunks)-1):        

                x_vals = []

                y_vals = []

                for (x,y) in chunks[i]:

                    x_vals.append(x)

                    y_vals.append(y)


                avg_x = int(np.average(x_vals))

                avg_y = int(np.average(y_vals))

                c.append([avg_y,avg_x])

                cv2.line(frame,(320,480),(avg_x,avg_y),(255,0,0),2)  

            print(c)

            forwardEdge = c[1]
            print(forwardEdge)

            cv2.line(frame,(320,480),(forwardEdge[1],forwardEdge[0]),(0,255,0),3)   
            cv2.imwrite(name, frame)
         
            y = (min(c))
            print(y)
        
            if forwardEdge[0] > 230: #200 # >230 works better 

                if y[1] < 360: #310
                    self.left()
                    #pwm.start(0)
                    #pwm1.start(40)
                    direction = "left "
                    print(direction)

                else: 
                    self.right()
                    direction = "right "
                    print(direction)

            else:
                self.forward()
    #           sleep(0.005)
                direction = "forward "
                print(direction)
           
            if testmode == 1:
                global F
                F.write ("frame"+str(currentFrame)+".jpg" +" | " + str(c[0]) + " | " + str(c[1]) + " | " +str(c[2])  + " | " + direction + "\n") 
                currentFrame +=1

            if testmode == 2:

                cv2.imshow("frame",frame)

                cv2.imshow("Canny",edges)

                cv2.imshow("result",img)


            k = cv2.waitKey(5) & 0xFF  ##change to 5

            if k == 27:

                break
            


        #cv2.destroyAllWindows
        #cap.release()
            
    def stopVision(self):
        global start
        start = False
        logger.info("Stopping Vision...")
            
        
