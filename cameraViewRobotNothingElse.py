import cv2.cv as cv 
import numpy as np
import PIL, Image, time
from naoqi import ALProxy
#IP = "looney.local"
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
    img = camProxy.getImageRemote(videoClient)
    #img = cv.Canny(img, 100, 200, 3)
    im = Image.fromstring("RGB", (img[0], img[1]), img[6])
    out = cv.CreateImageHeader(im.size, cv.IPL_DEPTH_8U, 3)
    cv.SetData(out, im.tostring(), im.size[0]*3)
    #output = cv.Canny(out, 100, 200, 3);
    cv.ShowImage("robot", out)
    x = cv.WaitKey(10)
    if x != -1:
        camProxy.unsubscribe(videoClient)    
        cv.DestroyWindow("robot")
        cv.DestroyWindow("ball")
camProxy.unsubscribe(videoClient)    
cv.DestroyWindow("robot")
cv.DestroyWindow("ball")
