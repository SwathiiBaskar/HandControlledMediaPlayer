# Hand-Controlled Media Player 

A Python project that lets you **control your media player using hand gestures** with the help of **OpenCV, MediaPipe, and Keyboard automation**.

---

## Features
- **0 Fingers** → Play (if paused)  
- **5 Fingers** → Pause (if playing)  
- **1 Finger** → Volume Down  
- **2 Fingers** → Volume Up  
- **3 Fingers** → Next Track (Right Arrow)  
- **4 Fingers** → Previous Track (Left Arrow)  

Gestures are recognized using **MediaPipe Hand Landmarks** and mapped to media key shortcuts.

---

## 🛠️ Tech Stack
- [Python 3.8+](https://www.python.org/)  
- [OpenCV](https://opencv.org/) → Frame capture & visualization  
- [MediaPipe](https://developers.google.com/mediapipe/) → Hand detection & landmarks  
- [Keyboard](https://pypi.org/project/keyboard/) → Media key automation  
- [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) → Auxiliary automation  

---

## Hand Landmark Reference

0: Wrist<br>
1–4: Thumb<br>
5–8: Index Finger<br>
9–12: Middle Finger<br>
13–16: Ring Finger<br>
17–20: Pinky<br>

---


