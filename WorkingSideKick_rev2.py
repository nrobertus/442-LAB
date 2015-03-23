from cv2 import *
import cv2
import Image
import sys
import random
from time import time
import time as time2
import numpy as np
from naoqi import ALProxy
import motion
import math

### hunters Kick
namesLeft = list()
timesLeft = list()
keysLeft = list()

namesLeft.append("HeadPitch")
timesLeft.append([ 0.58000, 1.34000, 1.60000, 2.12000, 2.56000, 3.46000])
keysLeft.append([ [ 0.04363, [ 3, -0.19333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.26180, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 0.17453, [ 3, -0.08667, 0.06012], [ 3, 0.17333, -0.12023]], [ -0.27925, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ -0.26180, [ 3, -0.14667, -0.00403], [ 3, 0.30000, 0.00825]], [ -0.24241, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("HeadYaw")
timesLeft.append([ 0.58000, 1.34000, 1.60000, 2.12000, 2.56000, 3.46000])
keysLeft.append([ [ -0.00464, [ 3, -0.19333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.00149, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ -0.00311, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.04905, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.03371, [ 3, -0.14667, 0.00268], [ 3, 0.30000, -0.00548]], [ 0.02459, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("LAnklePitch")
timesLeft.append([ 0.52000, 0.66000, 0.88000, 1.12000, 1.28000, 1.42000, 1.54000, 1.68000, 1.84000, 2.06000, 2.50000, 3.40000])
keysLeft.append([ [ 0.08727, [ 3, -0.17333, 0.00000], [ 3, 0.04667, 0.00000]], [ -0.08727, [ 3, -0.04667, 0.08824], [ 3, 0.07333, -0.13866]], [ -0.59341, [ 3, -0.07333, 0.00000], [ 3, 0.08000, 0.00000]], [ -0.40143, [ 3, -0.08000, -0.14312], [ 3, 0.05333, 0.09541]], [ 0.12217, [ 3, -0.05333, 0.00000], [ 3, 0.04667, 0.00000]], [ -0.05236, [ 3, -0.04667, 0.04386], [ 3, 0.04000, -0.03759]], [ -0.12217, [ 3, -0.04000, 0.00000], [ 3, 0.04667, 0.00000]], [ 0.24435, [ 3, -0.04667, 0.00000], [ 3, 0.05333, 0.00000]], [ -0.12217, [ 3, -0.05333, 0.12468], [ 3, 0.07333, -0.17144]], [ -0.64403, [ 3, -0.07333, 0.00000], [ 3, 0.14667, 0.00000]], [ -0.21991, [ 3, -0.14667, -0.07049], [ 3, 0.30000, 0.14419]], [ 0.00000, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("LAnkleRoll")
timesLeft.append([ 0.52000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
keysLeft.append([ [ -0.40143, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.10887, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ -0.13802, [ 3, -0.08667, 0.00000], [ 3, 0.04667, 0.00000]], [ 0.00000, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ -0.18097, [ 3, -0.12667, 0.05338], [ 3, 0.14667, -0.06181]], [ -0.34558, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ -0.05066, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("LElbowRoll")
timesLeft.append([ 0.50000, 1.26000, 1.52000, 2.04000, 2.48000, 3.38000])
keysLeft.append([ [ -0.64117, [ 3, -0.16667, 0.00000], [ 3, 0.25333, 0.00000]], [ -1.15353, [ 3, -0.25333, 0.18364], [ 3, 0.08667, -0.06282]], [ -1.38056, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ -1.36062, [ 3, -0.17333, -0.01994], [ 3, 0.14667, 0.01687]], [ -0.96024, [ 3, -0.14667, -0.09905], [ 3, 0.30000, 0.20261]], [ -0.45564, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("LElbowYaw")
timesLeft.append([ 0.50000, 1.26000, 1.52000, 2.04000, 2.48000, 3.38000])
keysLeft.append([ [ -0.99714, [ 3, -0.16667, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.86368, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ -0.90970, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ -0.63205, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ -0.84834, [ 3, -0.14667, 0.09469], [ 3, 0.30000, -0.19368]], [ -1.49714, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("LHand")
timesLeft.append([ 0.50000, 1.26000, 1.52000, 2.04000, 2.48000, 3.38000])
keysLeft.append([ [ 0.00129, [ 3, -0.16667, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.00136, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 0.00132, [ 3, -0.08667, 0.00001], [ 3, 0.17333, -0.00002]], [ 0.00128, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.00133, [ 3, -0.14667, -0.00005], [ 3, 0.30000, 0.00010]], [ 0.00391, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("LHipPitch")
timesLeft.append([ 0.52000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
keysLeft.append([ [ 0.16265, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.39726, [ 3, -0.25333, 0.31826], [ 3, 0.08667, -0.10888]], [ -1.11876, [ 3, -0.08667, 0.00190], [ 3, 0.04667, -0.00102]], [ -1.11978, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ -0.78540, [ 3, -0.12667, -0.12796], [ 3, 0.14667, 0.14816]], [ -0.29142, [ 3, -0.14667, -0.10930], [ 3, 0.30000, 0.22356]], [ 0.21318, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("LHipRoll")
timesLeft.append([ 0.52000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
keysLeft.append([ [ 0.47124, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.54001, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 0.32218, [ 3, -0.08667, 0.09040], [ 3, 0.04667, -0.04868]], [ 0.12276, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ 0.36360, [ 3, -0.12667, -0.04547], [ 3, 0.14667, 0.05265]], [ 0.41713, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ 0.05825, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("LKneePitch")
timesLeft.append([ 0.52000, 1.28000, 1.42000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
keysLeft.append([ [ -0.08901, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ 1.97575, [ 3, -0.25333, 0.00000], [ 3, 0.04667, 0.00000]], [ 1.97222, [ 3, -0.04667, 0.00353], [ 3, 0.04000, -0.00302]], [ 1.23918, [ 3, -0.04000, 0.26583], [ 3, 0.04667, -0.31013]], [ 0.24435, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ 1.53589, [ 3, -0.12667, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.62430, [ 3, -0.14667, 0.17650], [ 3, 0.30000, -0.36102]], [ -0.07666, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("LShoulderPitch")
timesLeft.append([ 0.50000, 1.26000, 1.52000, 2.04000, 2.48000, 3.38000])
keysLeft.append([ [ 1.52782, [ 3, -0.16667, 0.00000], [ 3, 0.25333, 0.00000]], [ 1.46033, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 1.47413, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 1.24096, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ 1.51862, [ 3, -0.14667, -0.01504], [ 3, 0.30000, 0.03076]], [ 1.54938, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("LShoulderRoll")
timesLeft.append([ 0.50000, 1.26000, 1.52000, 2.04000, 2.48000, 3.38000])
keysLeft.append([ [ 0.12268, [ 3, -0.16667, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.04138, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 0.14569, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.13955, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.14722, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ 0.03993, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("LWristYaw")
timesLeft.append([ 0.50000, 1.26000, 1.52000, 2.04000, 2.48000, 3.38000])
keysLeft.append([ [ 0.08727, [ 3, -0.16667, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.07359, [ 3, -0.25333, 0.00911], [ 3, 0.08667, -0.00312]], [ 0.05058, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.06285, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ -0.05680, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ -0.00149, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("RAnklePitch")
timesLeft.append([ 0.52000, 0.88000, 1.28000, 2.06000, 2.50000, 3.40000])
keysLeft.append([ [ 0.03226, [ 3, -0.17333, 0.00000], [ 3, 0.12000, 0.00000]], [ 0.01745, [ 3, -0.12000, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.01745, [ 3, -0.13333, 0.00000], [ 3, 0.26000, 0.00000]], [ 0.03491, [ 3, -0.26000, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.03491, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ -0.00117, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("RAnkleRoll")
timesLeft.append([ 0.52000, 0.88000, 1.28000, 2.06000, 2.50000, 3.40000])
keysLeft.append([ [ -0.33161, [ 3, -0.17333, 0.00000], [ 3, 0.12000, 0.00000]], [ -0.36652, [ 3, -0.12000, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.36652, [ 3, -0.13333, 0.00000], [ 3, 0.26000, 0.00000]], [ -0.36652, [ 3, -0.26000, 0.00000], [ 3, 0.14667, 0.00000]], [ -0.34732, [ 3, -0.14667, -0.01920], [ 3, 0.30000, 0.03927]], [ 0.08433, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("RElbowRoll")
timesLeft.append([ 0.54000, 1.30000, 1.56000, 2.08000, 2.52000, 3.42000])
keysLeft.append([ [ 0.74096, [ 3, -0.18000, 0.00000], [ 3, 0.25333, 0.00000]], [ 1.03396, [ 3, -0.25333, -0.15621], [ 3, 0.08667, 0.05344]], [ 1.36990, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 1.02015, [ 3, -0.17333, 0.11965], [ 3, 0.14667, -0.10124]], [ 0.70722, [ 3, -0.14667, 0.07036], [ 3, 0.30000, -0.14392]], [ 0.37732, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("RElbowYaw")
timesLeft.append([ 0.54000, 1.30000, 1.56000, 2.08000, 2.52000, 3.42000])
keysLeft.append([ [ 1.15353, [ 3, -0.18000, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.95411, [ 3, -0.25333, 0.06096], [ 3, 0.08667, -0.02085]], [ 0.90809, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 1.23023, [ 3, -0.17333, -0.11716], [ 3, 0.14667, 0.09913]], [ 1.55697, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ 1.14441, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("RHand")
timesLeft.append([ 0.54000, 1.30000, 1.56000, 2.08000, 2.52000, 3.42000])
keysLeft.append([ [ 0.00317, [ 3, -0.18000, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.00328, [ 3, -0.25333, -0.00003], [ 3, 0.08667, 0.00001]], [ 0.00329, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.00317, [ 3, -0.17333, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.00325, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ 0.00187, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("RHipPitch")
timesLeft.append([ 0.52000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
keysLeft.append([ [ 0.23159, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.10580, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 0.12217, [ 3, -0.08667, 0.00000], [ 3, 0.04667, 0.00000]], [ 0.08433, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ 0.09046, [ 3, -0.12667, -0.00614], [ 3, 0.14667, 0.00710]], [ 0.19171, [ 3, -0.14667, -0.00904], [ 3, 0.30000, 0.01849]], [ 0.21020, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("RHipRoll")
timesLeft.append([ 0.52000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
keysLeft.append([ [ 0.34366, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.36820, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 0.36820, [ 3, -0.08667, 0.00000], [ 3, 0.04667, 0.00000]], [ 0.36513, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ 0.36667, [ 3, -0.12667, 0.00000], [ 3, 0.14667, 0.00000]], [ 0.36513, [ 3, -0.14667, 0.00153], [ 3, 0.30000, -0.00314]], [ -0.10129, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("RHipYawPitch")
timesLeft.append([ 0.52000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
keysLeft.append([ [ -0.18097, [ 3, -0.17333, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.25307, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ -0.06285, [ 3, -0.08667, -0.02279], [ 3, 0.04667, 0.01227]], [ -0.05058, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ -0.18711, [ 3, -0.12667, 0.02986], [ 3, 0.14667, -0.03457]], [ -0.24386, [ 3, -0.14667, 0.01444], [ 3, 0.30000, -0.02954]], [ -0.31903, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("RKneePitch")
timesLeft.append([ 0.52000, 0.88000, 1.28000, 1.54000, 1.68000, 2.06000, 2.50000, 3.40000])
keysLeft.append([ [ -0.08727, [ 3, -0.17333, 0.00000], [ 3, 0.12000, 0.00000]], [ -0.08727, [ 3, -0.12000, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.09235, [ 3, -0.13333, 0.00000], [ 3, 0.08667, 0.00000]], [ -0.07973, [ 3, -0.08667, 0.00000], [ 3, 0.04667, 0.00000]], [ -0.07973, [ 3, -0.04667, 0.00000], [ 3, 0.12667, 0.00000]], [ -0.07819, [ 3, -0.12667, -0.00047], [ 3, 0.14667, 0.00055]], [ -0.07666, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ -0.09208, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("RShoulderPitch")
timesLeft.append([ 0.54000, 1.30000, 1.56000, 2.08000, 2.52000, 3.42000])
keysLeft.append([ [ 1.48649, [ 3, -0.18000, 0.00000], [ 3, 0.25333, 0.00000]], [ 1.35917, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ 1.41746, [ 3, -0.08667, -0.02659], [ 3, 0.17333, 0.05318]], [ 1.59847, [ 3, -0.17333, -0.03988], [ 3, 0.14667, 0.03375]], [ 1.63835, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ 1.50021, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("RShoulderRoll")
timesLeft.append([ 0.54000, 1.30000, 1.56000, 2.08000, 2.52000, 3.42000])
keysLeft.append([ [ -0.02305, [ 3, -0.18000, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.01998, [ 3, -0.25333, 0.00000], [ 3, 0.08667, 0.00000]], [ -0.13197, [ 3, -0.08667, 0.00000], [ 3, 0.17333, 0.00000]], [ -0.11816, [ 3, -0.17333, -0.01381], [ 3, 0.14667, 0.01168]], [ -0.02305, [ 3, -0.14667, 0.00000], [ 3, 0.30000, 0.00000]], [ -0.03524, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

namesLeft.append("RWristYaw")
timesLeft.append([ 0.54000, 1.30000, 1.56000, 2.08000, 2.52000, 3.42000])
keysLeft.append([ [ -0.24435, [ 3, -0.18000, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.23935, [ 3, -0.25333, -0.00500], [ 3, 0.08667, 0.00171]], [ -0.22094, [ 3, -0.08667, -0.00409], [ 3, 0.17333, 0.00818]], [ -0.20253, [ 3, -0.17333, -0.00554], [ 3, 0.14667, 0.00469]], [ -0.19026, [ 3, -0.14667, -0.01227], [ 3, 0.30000, 0.02510]], [ 0.12736, [ 3, -0.30000, 0.00000], [ 3, 0.00000, 0.00000]]])

#Connect to the robot
IP = "169.254.154.187"
PORT = 9559

##################################################
############## CREATE PROXYS #####################
##################################################

#### Creat camera proxy
camProxy = ALProxy("ALVideoDevice", IP, PORT)
#### Create text to speech proxy
tts = ALProxy("ALTextToSpeech", IP, 9559)
#### Creat LED Proxy
led = ALProxy("ALLeds", IP, 9559)
#### Get video feed from robot
videoClient = camProxy.subscribe("python_client", 2, 11, 5)
#### Set parameters for video feed
camProxy.setParam(18, 1)
#### Create motion proxy for robot
try:
    motionProxy = ALProxy("ALMotion", IP, PORT)
except Exception,e:
    print "Could not create proxy to ALMotion"
    print "Error was: ",e
    sys.exit(1)
#### Create posture proxy for robot
try:
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e


##################################################
### VIDEO FEED COLOR VARIABLES ###################
##################################################

#### Variables for color manipulation
hue1 = 50
hue2 = 120
sat1 = 150
sat2 = 200
val1 = 220
val2 = 325

# define winRange of color BGR
lower = np.array([hue1,sat1,val1])
upper = np.array([hue2,sat2,val2])

##################################################
########### MOVEMENT VARIABLES ###################
##################################################

#destination coordinates
x = 0
y = 0
xTracker = 0
yTracker = 0
#### Variables for movement ######################

#### Window winRange
#### vals are xMin, xMax, yMin, yMax
winRange = [0, 16, 0, 12]

### Movement when head is up
### vals are xLow Up, xHigh Up, yLow Up, yHigh Up
up = [6, 10, 4, 7]

### Movement when head is down
### vals are xLow Down, xHigh Down, yLow Down, yHigh Down
down = [6, 9, 4, 6]

### Movement for side kick
### vals are xLow Side, xHigh Side, yLow Side, yHigh Side
side = [6, 10, 3, 8]

# pitch radians winRange -0.6720 (up) to 0.5139 (down)
headPitch = 0
# yaw radians winRange -2.0875 (right) to 2.0875 (left)
headYaw = 0

##################################################
############## LED INITILIZATION #################
##################################################
### Colors are Red, Blue, Green, 
leftColor = "Blue"
rightColor = "Blue"

left = [
"Face/Led/"+leftColor+"/Left/0Deg/Actuator/Value",
"Face/Led/"+leftColor+"/Left/45Deg/Actuator/Value",
"Face/Led/"+leftColor+"/Left/90Deg/Actuator/Value",
"Face/Led/"+leftColor+"/Left/135Deg/Actuator/Value",
"Face/Led/"+leftColor+"/Left/180Deg/Actuator/Value",
"Face/Led/"+leftColor+"/Left/225Deg/Actuator/Value",
"Face/Led/"+leftColor+"/Left/270Deg/Actuator/Value",
"Face/Led/"+leftColor+"/Left/315Deg/Actuator/Value"]

right = [
"Face/Led/"+rightColor+"/Right/0Deg/Actuator/Value",
"Face/Led/"+rightColor+"/Right/45Deg/Actuator/Value",
"Face/Led/"+rightColor+"/Right/90Deg/Actuator/Value",
"Face/Led/"+rightColor+"/Right/135Deg/Actuator/Value",
"Face/Led/"+rightColor+"/Right/180Deg/Actuator/Value",
"Face/Led/"+rightColor+"/Right/225Deg/Actuator/Value",
"Face/Led/"+rightColor+"/Right/270Deg/Actuator/Value",
"Face/Led/"+rightColor+"/Right/315Deg/Actuator/Value"]

led.createGroup('lGroup', left)
led.createGroup('rGroup', right)
led.off('FaceLeds')

##################################################
############## FINAL INITIALIZATION ##############
##################################################

#### Video Init
#initialiaze cnt
init_img = camProxy.getImageRemote(videoClient)
init_im = Image.fromstring("RGB", (init_img[0], init_img[1]), init_img[6])
init_frame = np.array(init_im)
cnt = init_frame[0]

#### speech and posture init
tts.setVolume(.2)
tts.say("Initiating")
postureProxy.goToPosture("Crouch", 0.8)
postureProxy.goToPosture("StandInit", 0.8)
motionProxy.setAngles(["HeadYaw", "HeadPitch"],[-0.1, 0.5], 0.2)

#### Boolean Init
stillWorking = True
commandGiven = True
sidekick = True
t = True
##################################################
############## PROGRAM ###########################
##################################################
i = 0
try:
    while(1):

        #get the current time in seconds
        seconds = int(time()%4)
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

        xPrev = xTracker
        yPrev = yTracker

        if(area > 1):
            xTracker = int(cv.GetSpatialMoment(moments, 1, 0) / area)/40
            yTracker = int(cv.GetSpatialMoment(moments, 0, 1) / area)/40
            if((xTracker >= 7) & (xTracker <= 9) & (yPrev != yTracker)):
                led.on('lGroup')
                led.on('rGroup')
            elif(xPrev > xTracker):
                led.off('rGroup')
                led.on('lGroup')
            elif(xPrev < xTracker):
                led.off('lGroup')
                led.on('rGroup')
            else:
                led.off('lGroup')
                led.off('rGroup')
        else:
                led.off('lGroup')
                led.off('rGroup')

        #convert from BGR to RGB
        one = 28
        two = one + 10
        three = 60
        regular = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if (i < one):
        	i += 1
        	motionProxy.setWalkTargetVelocity(0, 1, 0, .5)
        elif((i >= one) & (i < two)):
        	i += 1
        	motionProxy.setWalkTargetVelocity(0, 0, 0, 0)
        elif((i >= two) & (i < three)):
        	i += 1
        	motionProxy.setWalkTargetVelocity(1, 0, 0, .5)
        elif(i == three):
            motionProxy.setWalkTargetVelocity(0, 0, 0, 0)
        	##################################################
            ############## Setup for side kick ###############
            ##################################################
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

            # Motion of the RLeg and LLeg
            dx      = 0.0                 # translation axis X (meters)
            dy      = 0.2                   # translation axis Y (meters)
            dz      = 0.01                 # translation axis Z (meters)

            dwx     = 10.0*math.pi/180.0     # rotation axis X (radian)
            dwy     = 0.0                   # rotation axis Y (radian) Original: 5.0*math.pi/180.0
            dwz     = 0.0


            times   = [1.3, 1.4, 1.5]
            isAbsolute = False

            targetList = [
              [0.0, -dy, dz, -dwx, 0.0, 0.0],
              [dx, -dy, dz, -dwx, dwy, dwz],
              [0.0, -0.07, 0.0, 0.0, 0.0, 0.0]]

            
            ##################################################
            ############## Left Leg Balance ##################
            ##################################################
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

            ##################################################
            ############## Right Leg Kick ####################
            ##################################################
            ##### This does the right leg kick
            motionProxy.positionInterpolation(effectorName, space, targetList,
                                         axisMask, times, isAbsolute)


            ##################################################
            ############## Clean Up Stuff ####################
            ##################################################
            time2.sleep(1.0)

            # Deactivate Head tracking
            i += 1
            isEnabled    = False
            motionProxy.wbEnable(isEnabled)
            sidekick = False

            print "side kick"
        elif ((i > three) & (i < 125)):
        	i += 1
        	motionProxy.setWalkTargetVelocity(-.8, -1, .1, 1)
        elif(i == 125):
        	i += 1
        	motionProxy.setWalkTargetVelocity(0, 0, 0, 0)
        	break
        seconds = 10
        ##################################################
        ##### Main Movement Conditionals #################
        ##################################################
        if((seconds == 0)&(commandGiven)&(stillWorking)):

            ## If ball is found
            if((area > 40000)&(headYaw == 0)):
                x = int(cv.GetSpatialMoment(moments, 1, 0) / area)/40
                y = int(cv.GetSpatialMoment(moments, 0, 1) / area)/40
                print "x: ", x
                print "y: ", y

                ###### LOOKING UP CONDITIONALS
                if(sidekick):
                    commandGiven = False
                    
                    #### If the ball is at the top of the screen
                    if((y >= winRange[2]) & (y < side[2])):

                        if((x >= winRange[0]) & (x < side[0])): # STRAFE LEFT FAST
                            motionProxy.setWalkTargetVelocity(0, 1, 0, 0.8)
                            print "strafe left fast"

                        elif((x >= side[0]) & (x <= side[1])): # STRAFE LEFT SLOW
                            motionProxy.setWalkTargetVelocity(0, 1, 0, 0.3)
                            print "strafe left slow"

                        elif((x > side[1]) & (x <= winRange[1])): # FORWARD FAST
                            motionProxy.setWalkTargetVelocity(1, 0, 0, 0.8)
                            print "forward fast"

                    #### If the ball is at the middle of the screen
                    elif((y >= side[2]) & (y <= side[3])):

                        if((x >= winRange[0]) & (x < side[0])): # STRAFE LEFT FAST
                            motionProxy.setWalkTargetVelocity(0, 1, 0, 0.5)
                            print "strafe left fast"

                        elif((x >= side[0] )& (x <= side[1])): # STRAFE LEFT SLOW
                            motionProxy.setWalkTargetVelocity(0, 1, 0, 0.3)
                            print "strafe left slow"

                        elif((x > side[1]) & (x <= winRange[1])): # FORWARD SLOW
                            motionProxy.setWalkTargetVelocity(0.5, 0, 0, 0.1)
                            print "forward slow"

                    #### If the ball is at the bottom of the screen
                    elif((y > side[3]) & (y <= winRange[3])):

                        if((x >= winRange[0]) & (x < side[0])): # BACK UP SLOW
                            motionProxy.setWalkTargetVelocity(-1, 0, 0, 0.5)
                            print "back up slow"

                        elif((x >= side[0]) & (x <= side[1])): # BACK UP SLOW
                            motionProxy.setWalkTargetVelocity(-1, 0, 0, 0.5)
                            print "back up slow"

                        elif((x > side[1]) & (x <= winRange[1])): # SIDE KICK

                            ##################################################
                            ############## Setup for side kick ###############
                            ##################################################
                            motionProxy.setWalkTargetVelocity(0, 1, 0, 0.3)
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

                            # Motion of the RLeg and LLeg
                            dx      = 0.0                 # translation axis X (meters)
                            dy      = 0.1                   # translation axis Y (meters)
                            dz      = 0.01                 # translation axis Z (meters)

                            dwx     = 5.0*math.pi/180.0     # rotation axis X (radian)
                            dwy     = 0.0                   # rotation axis Y (radian) Original: 5.0*math.pi/180.0
                            dwz     = 0.0


                            times   = [.8, .9, 1.0]
                            isAbsolute = False

                            targetList = [
                              [0.0, -dy, 0.0, 0.0, 0.0, 0.0],
                              [dx, -dy, dz, -dwx, dwy, dwz],
                              [0.0, -0.07, 0.0, 0.0, 0.0, 0.0]]

                            
                            ##################################################
                            ############## Left Leg Balance ##################
                            ##################################################
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

                            ##################################################
                            ############## Right Leg Kick ####################
                            ##################################################
                            ##### This does the right leg kick
                            motionProxy.positionInterpolation(effectorName, space, targetList,
                                                         axisMask, times, isAbsolute)


                            ##################################################
                            ############## Clean Up Stuff ####################
                            ##################################################
                            time2.sleep(1.0)

                            # Deactivate Head tracking
                            isEnabled    = False
                            motionProxy.wbEnable(isEnabled)
                            sidekick = False
                            print "side kick"

                elif(headPitch == 0):
                    commandGiven = False
                    
                    #### If the ball is at the top of the screen
                    if((y >= winRange[2]) & (y < up[2])):

                        if((x >= up[0]) & (x <= up[1])): # FORWARD FAST
                            motionProxy.setWalkTargetVelocity(1, 0, 0, 1.0)
                            print "Forward Fast"

                        elif((x >= winRange[0]) & (x < up[0])): # LEFT SLOW
                            motionProxy.setWalkTargetVelocity(0, 0, 0.3, 0.1)
                            print "leftSlow"

                        elif((x > up[1]) & (x <= winRange[1])): # RIGHT SLOW
                            motionProxy.setWalkTargetVelocity(0, 0, -0.3, 0.1)
                            print "rightSlow"

                    #### If the ball is at the middle of the screen
                    elif((y >= up[2]) & (y <= up[3])):

                        if((x >= up[0]) & (x <= up[1])): # FORWARD SLOW
                            motionProxy.setWalkTargetVelocity(1, 0, 0, 0.5)
                            print "Forward slow"

                        elif((x >= winRange[0] )& (x < up[0])): # LEFT MEDIUM
                            motionProxy.setWalkTargetVelocity(0, 0, 0.3, 0.2)
                            print "leftMedium"

                        elif((x > up[1]) & (x <= winRange[1])): # RIGHT MEDIUM
                            motionProxy.setWalkTargetVelocity(0, 0, -0.3, 0.2)
                            print "rightMedium"

                    #### If the ball is at the bottom of the screen
                    elif((y > up[3]) & (y <= winRange[3])):

                        if((x >= winRange[0]) & (x < up[0])): # LEFT FAST
                            motionProxy.setWalkTargetVelocity(0, 0, 0.3, 0.2)
                            print "leftFast"

                        elif((x > up[1]) & (x <= winRange[1])): # RIGHT FAST
                            motionProxy.setWalkTargetVelocity(0, 0, -0.3, 0.2)
                            print "rightFast"

                        elif((x >= up[0]) & (x <= up[1])): # LOOK DOWN
                            headPitch = 0.5
                            motionProxy.setAngles(["HeadYaw", "HeadPitch"],[0.0, headPitch], 0.2)
                            print "look down"

                ###### LOOKING DOWN CONDITIONALS
                elif(headPitch == .5):
                    commandGiven = False

                    #### If the ball is at the top of the screen
                    if((y >= winRange[2]) & (y < down[2])):

                        if((x >= down[0]) & (x <= down[1])): # FORWARD FAST
                            motionProxy.setWalkTargetVelocity(1, 0, 0, 0.5)
                            print "Forward Fast"

                        elif((x >= winRange[0]) & (x < down[0])): # LEFT SLOW
                            motionProxy.setWalkTargetVelocity(0, 0, 0.2, 0.2)
                            print "leftSlow"

                        elif((x > down[1]) & (x <= winRange[1])): # RIGHT SLOW
                            motionProxy.setWalkTargetVelocity(0, 0, -0.2, 0.2)
                            print "rightSlow"

                    #### If the ball is at the middle of the screen
                    elif((y >= down[2]) & (y <= down[3])):
                        if((x >= down[0]) & (x <= down[1])): # FORWARD SLOW
                            motionProxy.setWalkTargetVelocity(0.8, 0, 0, 0.2)
                            print "Forward slow"

                        elif((x >= winRange[0]) & (x < down[0])): # LEFT MEDIUM
                            motionProxy.setWalkTargetVelocity(0, 0, 0.2, 0.2)
                            print "leftMedium"

                        elif((x > down[1]) & (x <= winRange[1])): # RIGHT MEDIUM
                            motionProxy.setWalkTargetVelocity(0, 0, -0.2, 0.2)
                            print "rightMedium"

                    #### If the ball is at the bottom of the screen
                    elif((y > down[3]) & (y <= winRange[3])):

                        if((x >= winRange[0]) & (x < down[0])): # LEFT FAST
                            motionProxy.setWalkTargetVelocity(0, 0, 0.3, 0.2)
                            print "leftFast"

                        elif((x > down[1]) & (x <= winRange[1])): # RIGHT FAST
                            motionProxy.setWalkTargetVelocity(0, 0, -0.3, 0.2)
                            print "rightFast"

                        elif((x >= down[0]) & (x <= down[1])): # KICK / LOOK DOWN
                            headPitch = 0
                            stillWorking = False
                            postureProxy.goToPosture("StandInit", 0.8)
                            time2.sleep(1)
                            motionProxy.angleInterpolationBezier(namesLeft, timesLeft, keysLeft)
                            tts.say("Finished")
                            print "kick"
                            break

            # Turn Left toward ball if it is found
            elif((area > 40000)&(headYaw == 1)):
                commandGiven = False
                headYaw = 0
                motionProxy.setAngles(["HeadYaw", "HeadPitch"],[0, 0], 1)
                motionProxy.setWalkTargetVelocity(0, 0, 1, 0.5)
                print "Ball Detected! Turning Left"
            # Turn right toward ball if it is found
            elif((area > 40000)&(headYaw == -1)):
                commandGiven = False
                headYaw = 0
                motionProxy.setAngles(["HeadYaw", "HeadPitch"],[0, 0], 1)
                motionProxy.setWalkTargetVelocity(0, 0, -1, 0.5)
                print "Ball Detected! Turning Right"

            #### Look around for the ball
            else:
                commandGiven = False
                if (headYaw == 0):
                    headYaw = 1
                    motionProxy.setAngles(["HeadYaw", "HeadPitch"],[headYaw, headPitch], 0.3)
                    print "look left for ball"
                elif (headYaw == 1):
                    headYaw = -1
                    motionProxy.setAngles(["HeadYaw", "HeadPitch"],[headYaw, headPitch], 0.3)
                    print "look right for ball"
                else:
                    headYaw = 0
                    motionProxy.setAngles(["HeadYaw", "HeadPitch"],[headYaw, headPitch], 0.3)
                    print "no ball found"
            
        #### Stop movement        
        if((seconds == 2)&(stillWorking)):
            commandGiven = True
            motionProxy.setWalkTargetVelocity(0, 0, 0, 0)


        # Display images
        cv2.circle(regular, (xTracker*40, yTracker*40), 10, 255, 5, 1, 0)
        cv.ShowImage('thresh', hsvThresh)
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
    led.on('rGroup')
    led.on('lGroup')
    postureProxy.goToPosture("Crouch", 0.5)
    motionProxy.stiffnessInterpolation("Body", 0, 1.0)
    camProxy.unsubscribe(videoClient)
    cv2.destroyAllWindows()
except:
    print"Failure"
    print sys.exc_info()[2]
    print sys.exc_info()[1]
    print sys.exc_info()[0]
    camProxy.unsubscribe(videoClient)
    cv2.destroyAllWindows()
    postureProxy.goToPosture("Crouch", 0.8)
    motionProxy.stiffnessInterpolation("Body", 0, 1.0)