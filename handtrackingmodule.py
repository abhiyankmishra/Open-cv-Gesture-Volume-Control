import cv2
import mediapipe as mp
import time

class handdetector():

    def __init__(self,mode = False,maxhands = 2,mindetectionconfidence = 0.7,mintrackingconfidence=0.5):
      self.mode=mode
      self.maxhands=maxhands
      self.mindetectionconfidence=mindetectionconfidence
      self.mintrackingconfidence=mintrackingconfidence

      self.mphands = mp.solutions.hands
      self.hands = self.mphands.Hands(self.mode,self.maxhands,self.mindetectionconfidence,self.mintrackingconfidence)
      self.mpdraw = mp.solutions.drawing_utils

    def findhands(self,img,draw=True):
      imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
      self.results=self.hands.process(imgrgb)
    # print(results.multi_hand_landmarks)

      if self.results.multi_hand_landmarks:
          for hndlms in self.results.multi_hand_landmarks:
              if draw:
                self.mpdraw.draw_landmarks(img,hndlms,self.mphands.HAND_CONNECTIONS)
      return img


    def findposition(self,img,handno=0,draw=True):
        lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand= self.results.multi_hand_landmarks[handno]
            for id, lm  in enumerate(myhand.landmark):
                   h,w,c=img.shape
                   cx,cy=int(lm.x * w),int(lm.y * h)
                   lmlist.append([id,cx,cy])
                   if draw:
                      cv2.circle(img,(cx,cy),4,(255,0,255),cv2.FILLED)
            return lmlist


def main():
    ptime = 0
    ctime = 0
    detector=handdetector()
    cap = cv2.VideoCapture(0)
    while True:
        check, img = cap.read()
        img=detector.findhands(img)
        lmlist=detector.findposition(img)
        if lmlist:
            print(lmlist[4])

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 2)

        cv2.imshow("img", img)
        cv2.waitKey(1)



if __name__=="__main__":
    main()
