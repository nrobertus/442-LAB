import cv2.cv as cv, Image, time, numpy as np, PIL
import cv2
from naoqi import ALProxy

#video_capture = cv.VideoCapture(2)
IP = "169.254.124.254"
cam = 1
camProxy = ALProxy("ALVideoDevice", IP, 9559)
print "camProxy done"
videoClient = camProxy.subscribe("python_client", 1, 11, 5)
print "subscribe done"
print "init done"
cv.NamedWindow("robot", 1)
camProxy.setParam(18, 1)

while True:
    # Capture frame-by-frame
    frame = camProxy.getImageRemote(videoClient)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 200, 3)
    cv.imshow('Video', edges)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv.destroyAllWindows()