import cv2
import mediapipe as mp
import time


mphands=mp.solutions.hands
hands=mphands.Hands()
mpdraw=mp.solutions.drawing_utils



cap=cv2.VideoCapture(0)


ptime=0

ctime=0

while True:
    check,img=cap.read()
    imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgrgb)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for hndlms in results.multi_hand_landmarks:
            for id, lm  in enumerate(hndlms.landmark):
                h,w,c=img.shape
       #here we are accessing the accurate position of our  handladmarks so that we
       #use it later on according to out need
                cx,cy=int(lm.x*w),int(lm.y*h)

               # by below code we can make circle on any of the index we want
                # if id==4:
                #     cv2.circle(img,(cx,cy),15,(244,0,255),cv2.FILLED)






            mpdraw.draw_landmarks(img,hndlms,mphands.HAND_CONNECTIONS)


    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,f"FPS:{int(fps)}",(10,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)

    cv2.imshow("img",img)
    cv2.waitKey(25)