from cv2 import *
import cv2
import Image
import sys
import random
from time import time
import numpy as np
from naoqi import ALProxy
import time as time2
import motion
import math

#Connect to the robot
IP = "169.254.189.195"
PORT = 9559
camProxy = ALProxy("ALVideoDevice", IP, PORT)
videoClient = camProxy.subscribe("python_client", 2, 11, 5)
camProxy.setParam(18, 1)
try:
    motionProxy = ALProxy("ALMotion", IP, PORT)
except Exception,e:
    print "Could not create proxy to ALMotion"
    print "Error was: ",e
    sys.exit(1)

try:
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e
#destination coordinates
x = 0;
y = 0;
hue1 = 50
hue2 = 120
sat1 = 150
sat2 = 200
val1 = 220
val2 = 325

# define range of color BGR
lower = np.array([hue1,sat1,val1])
upper = np.array([hue2,sat2,val2])

#initialiaze cnt
init_img = camProxy.getImageRemote(videoClient)
init_im = Image.fromstring("RGB", (init_img[0], init_img[1]), init_img[6])
init_frame = np.array(init_im)
cnt = init_frame[0]

headPitch = 1

postureProxy.goToPosture("StandInit", 0.8)
# pitch radians range -0.6720 to 0.5139


commandGiven = True
try:
    while(1):

        #get the current time in seconds
        t = int(time())
        seconds = int(str(t)[-1])
        seconds = int(seconds%3)
        #from other file
        img = camProxy.getImageRemote(videoClient)
        im = Image.fromstring("RGB", (img[0], img[1]), img[6])
        
        # Change capture to numpy for ez edit
        frame = np.array(im)
        
        #HSV Stuff
        hsvImg = cv.CreateImage(cv.GetSize(cv.fromarray(frame)), 8, 3)
        cv.CvtColor(cv.fromarray(frame), hsvImg, cv.CV_BGR2HSV)
        hsvThresh = cv.CreateImage(cv.GetSize(hsvImg), 8, 1)
        cv.InRangeS(hsvImg, lower, upper, hsvThresh)

        moments = cv.Moments(cv.GetMat(hsvThresh), 0)
        area = cv.GetCentralMoment(moments, 0, 0)

        # convert from BGR to RGB
        regular = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            x = int(cv.GetSpatialMoment(moments, 1, 0) / area)
            y = int(cv.GetSpatialMoment(moments, 0, 1) / area)
        except:
            x = int(cv.GetSpatialMoment(moments, 1, 0) / 1)
            y = int(cv.GetSpatialMoment(moments, 0, 1) / 1)
        
        if(((seconds == 0) | (seconds == 2))&(commandGiven)&(area > 10000)):
            x = x / 40
            y = y / 40
            print x
            print y
            commandGiven = False    
            #### (forward/back, side2side, rotate, speed)
            if((x >= 4) & (x <= 7) & (y >= 0) & (y <= 2)): # FORWARD FAST
                motionProxy.setWalkTargetVelocity(1, 0, 0, (0.8*headPitch))
                print "Forward Fast"

            elif((x >= 0) & (x <= 3) & (y >=0) & (y <= 2)): # LEFT SLOW
                motionProxy.setWalkTargetVelocity(0, 0, 0.1, 1)
                print "leftSlow"

            elif((x >= 8) & (x <= 15) & (y >=0) & (y <= 2)): # RIGHT SLOW
                motionProxy.setWalkTargetVelocity(0, 0, -0.1, 1)
                print "rightSlow"

            elif((x >= 4) & (x <= 7) & (y >=3) & (y <= 6)): # FORWARD SLOW
                motionProxy.setWalkTargetVelocity(1, 0, 0, (0.6*headPitch))
                print "Forward slow"

            elif((x >= 0 )& (x <=3) & (y >=3) & (y <= 6)): # LEFT MEDIUM
                motionProxy.setWalkTargetVelocity(0, 0, 0.2, (.8*headPitch))
                print "leftMedium"

            elif((x >= 8) & (x <= 15) & (y >=3) & (y <= 6)): # RIGHT MEDIUM
                motionProxy.setWalkTargetVelocity(0, 0, -0.2, (.8*headPitch))
                print "rightMedium"

            elif((x >= 0) & (x <= 3) & (y >=7) & (y <= 12)): # LEFT FAST
                motionProxy.setWalkTargetVelocity(0, 0, 0.3, (.8*headPitch))
                print "leftFast"

            elif((x >= 8) & (x <= 15) & (y >=7) & (y <= 12)): # RIGHT FAST
                motionProxy.setWalkTargetVelocity(0, 0, -0.3, (.8*headPitch))
                print "rightFast"

            elif((x >= 3) & (x <= 7) & (y >=7) & (y <= 12)): # KICK / LOOK DOWN
                if(headPitch == 1):
                    headPitch = 0.5
                    motionProxy.setAngles(["HeadYaw", "HeadPitch"],[0.0, headPitch], 0.2)
                else:

                    #### Kick Method ####
                    # Get to a stable posture first
                    postureProxy.goToPosture("StandInit", 0.8)
                    #wait a second to gain composure
                    time2.sleep(1)
                    #then kick
                    # Activate Whole Body Balancer
                    isEnabled  = True
                    motionProxy.wbEnable(isEnabled)
                    # Legs are constrained fixed
                    stateName  = "Fixed"
                    supportLeg = "Legs"
                    motionProxy.wbFootState(stateName, supportLeg)
                    # Constraint Balance Motion
                    isEnable   = True
                    supportLeg = "Legs"
                    motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)
                    # Com go to LLeg
                    supportLeg = "LLeg"
                    duration   = 2.0
                    motionProxy.wbGoToBalance(supportLeg, duration)
                    # RLeg is free
                    stateName  = "Free"
                    supportLeg = "RLeg"
                    motionProxy.wbFootState(stateName, supportLeg)
                    # RLeg is optimized
                    effectorName = "RLeg"
                    axisMask     = 63
                    space        = motion.FRAME_ROBOT
                    # Motion of the RLeg
                    dx      = 0.05                 # translation axis X (meters)
                    dz      = 0.05                 # translation axis Z (meters)
                    dwy     = 5.0*math.pi/180.0    # rotation axis Y (radian)
                    times   = [2.0, 2.7, 4.5]
                    isAbsolute = False
                    targetList = [
                      [-dx, 0.0, dz, 0.0, +dwy, 0.0],
                      [+dx, 0.0, dz, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
                    motionProxy.positionInterpolation(effectorName, space, targetList, axisMask, times, isAbsolute)
                    # Example showing how to Enable Effector Control as an Optimization
                    isActive     = False
                    motionProxy.wbEnableEffectorOptimization(effectorName, isActive)
                    # Com go to LLeg
                    supportLeg = "RLeg"
                    duration   = 2.0
                    motionProxy.wbGoToBalance(supportLeg, duration)
                    # RLeg is free
                    stateName  = "Free"
                    supportLeg = "LLeg"
                    motionProxy.wbFootState(stateName, supportLeg)
                    effectorName = "LLeg"
                    motionProxy.positionInterpolation(effectorName, space, targetList,axisMask, times, isAbsolute)
                    time2.sleep(1.0)
                    # Deactivate Head tracking
                    isEnabled    = False
                    motionProxy.wbEnable(isEnabled)
                    # send robot to Pose Init
                    postureProxy.goToPosture("StandInit", 0.5)

                    #### END Kick Method ####
                    break
                print "kick"

        if((seconds == 1) | (seconds == 3)):
            commandGiven = True
            motionProxy.setWalkTargetVelocity(0, 0, 0, 0)

        # Display images
        cv2.circle(regular, (x, y), 10, 255, 5, 1, 0)
        #cv.ShowImage('thresh', hsvThresh)
        cv2.imshow('regular', regular)
        
        
        # exit code
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

        #Recalibrate the color sensors
        if k == 119:
            hue1 = hue1+10
            hue2 = hue2 + 10
            print "Lower Hue: %d" % hue1
            print "Upper Hue: %d" % hue2
            print ""
        if k == 115:
            hue1 = hue1-10
            hue2 = hue2-10
            print "Lower Hue: %d" % hue1
            print "Upper Hue: %d" % hue2
            print ""
        if k == 101:
            sat1 = sat1+10
            sat2 = sat2 + 10
            print "Lower Saturation: %d" % sat1
            print "Upper Saturation: %d" % sat2
            print ""
        if k == 100:
            sat1 = sat1-10
            sat2 = sat2-10
            print "Lower Saturation: %d" % sat1
            print "Upper Saturation: %d" % sat2
            print ""
        if k == 114:
            val1 = val1+10
            val2 = val2 + 10
            print "Lower Value: %d" % val1
            print "Upper Value: %d" % val2
            print ""
        if k == 102:
            val1 = val1-10
            val2 = val2-10
            print "Lower Value: %d" % val1
            print "Upper Value: %d" % val2
            print ""
        lower = np.array([hue1,sat1,val1])
        upper = np.array([hue2,sat2,val2])
    # Cleanup
    camProxy.unsubscribe(videoClient)
    cv2.destroyAllWindows()
except:
    print"Failure"
    print sys.exc_info()[2]
    print sys.exc_info()[1]
    print sys.exc_info()[0]
    camProxy.unsubscribe(videoClient)
    cv2.destroyAllWindows()