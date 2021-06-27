import cv2
import time
import numpy as np
import handtrackingmodule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
########################################
wcam,hcam=640,480
##############################


cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime=0
detector=htm.handdetector()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()


minvol=volrange[0]
maxvol=volrange[1]
vol=0
volbar=400
volper=0

while True:
    succ,img=cap.read()
    img=detector.findhands(img)
    lmlist=detector.findposition(img,draw=False)
    if lmlist:
        # print(lmlist[4],lmlist[8])


        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx=(x1+x2)//2
        cy=(y1+y2)//2

        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)

        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)
        # print(length)


# hand range from 50 to 300 approx
# volume ranges from -65 to 0

        vol=np.interp(length,[30,130],[minvol,maxvol])
        volbar=np.interp(length,[30,130],[400,150])
        volper=np.interp(length,[30,130],[0,100])

        print(int(length),vol)

        volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)




    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volbar)),(85,400),(0,255,0),cv2.FILLED)

    cv2.putText(img,f'VOL:{int(volper)}%',(35,450),cv2.FONT_HERSHEY_COMPLEX
                ,1,(0,255,0),2)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime



    cv2.imshow("Img",img)
    cv2.waitKey(25)
