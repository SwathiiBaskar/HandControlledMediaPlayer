import cv2
import mediapipe as mp
import pyautogui
import time
import keyboard
mp_hands=mp.solutions.hands #solutions is a subpackage containing all mediapipe modules(hands, face,pose etc)
#mp.solutions.hands accesses the hand-tracking module, which include the Hands class
#so inside the module there is a class
mp_draw=mp.solutions.drawing_utils #a module to draw connections and landmarks
hands=mp_hands.Hands(model_complexity=1,max_num_hands=1) #object for the Hands class
#runs a palm detector
#runs a hand landmark model
#manages post processing(normalisation, filtering)
#other parameters to use
'''bool static_image_mode --> set True if using photos
int max_num_hands --> maximum number of hands to detect
float min_detection_confidence (0-1)--> Threshold for detecting new hand(Minimum confidence to say the object is hand)
float min_tracking_confidence -->Threshold for tracking existing hands (Minimum confidence to keep tracking)
'''
tip_ids=[4,8,12,16,20] #among the 21 points for hand, these 5 represent tip of each finger
def count_fingers(hand_landmarks):
    #hand_landmarks is a landmark object for one detected hand
    fingers=[]
    if hand_landmarks.landmark[tip_ids[0]].x<hand_landmarks.landmark[tip_ids[0]-1].x:
        #.landmark is a list-like structure holding all 21 landmarks accessed by 0 to 20
        #when we fold thumb alone we fold it sidewise in horizontal direction
        #other fingers are folded vertically
        #Thats y x is considered here
        #the relational operator's sign inverts if we consider the opposite hand
        #attributes if hand_landmark.landmarks:
        #       .x-->horizontal position[0.0,1.0]
        #       .y--> vertical position
        #       .z--> depth(float, relative to landmark 0) or in simple words, distance of point from camera
        #           if z<0 closer to camera
        #           farther to camera
        fingers.append(1)
    else:
        fingers.append(0)
    for i in range(1,5):
        if hand_landmarks.landmark[tip_ids[i]].y<hand_landmarks.landmark[tip_ids[i]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return sum(fingers)

cap=cv2.VideoCapture(0)
prev_gesture=-1
isPlaying=False
last_volume_time=time.time()
volume_interval=0.3
while True:
    success,frame=cap.read()
    if not success:
        break
    frame=cv2.flip(frame,1) #flipping to avoid mirroring
    img_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #mediapipe requires rgb format frames
    result=hands.process(img_rgb) #feeds a single rgb image for detection and tracking
    #returns a named tuple multi_hand_landmarks containing a normalised landmark list
    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame,handlms,mp_hands.HAND_CONNECTIONS)
            #here mp_hands.HAND_CONNECTIONS contain a frozenset[Tuple[int, int]], a constant list of
            #landmark index pairs that defines how to connect hand keypoints
            #or in simple words used to draw the bones
            total_fingers=count_fingers(handlms)
            cv2.putText(frame, f'Fingers: {total_fingers}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            #the above line is to display gesture on screen
            current_time=time.time()
            if total_fingers!=prev_gesture:
            #If the current action is different from previous one (to avoid repitition
                prev_gesture=total_fingers #updating previous gesture to make it remember what was just done
                current_time=time.time()
                if total_fingers==5 and isPlaying:
                    keyboard.send('play/pause media')
                    isPlaying=False
                elif total_fingers==0 and not isPlaying:
                    keyboard.send('play/pause media')
                    isPlaying=True
                elif total_fingers==3:
                    keyboard.press_and_release('right')
                elif total_fingers==4:
                    keyboard.press_and_release('left')
            if total_fingers==2:
                if current_time-last_volume_time>volume_interval:
                    keyboard.send('volume up')
                    last_volume_time=current_time
            elif total_fingers==1:
                if current_time-last_volume_time>volume_interval:
                    keyboard.send('volume down')
                    last_volume_time=current_time
    cv2.imshow("Hand controlled Media player",frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
