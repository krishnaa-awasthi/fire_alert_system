import cv2
import numpy as np
import pygame
import threading
import tkinter as tk
from PIL import Image, ImageTk

# === AUDIO SETUP ===
pygame.mixer.init()
ALERT_AUDIO = "aag.mp3"   # put your alert file here

def play_alert():
    pygame.mixer.music.load(ALERT_AUDIO)
    pygame.mixer.music.play()

# === CAMERA SETUP ===
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
if not cap.isOpened():
    print("Camera not opened")
    exit()

# === TKINTER SETUP ===
root = tk.Tk()
root.title("Fire Detector System")

video_label = tk.Label(root)
video_label.pack()

fire_prev = False
cooldown = 0
MIN_AREA = 1500
COOLDOWN_FRAMES = 20

def update_frame():
    global fire_prev, cooldown
    
    ret, frame = cap.read()
    if not ret:
        root.after(10, update_frame)
        return

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 80, 80])
    upper = np.array([60, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    fire = False
    for cnt in contours:
        if cv2.contourArea(cnt) > MIN_AREA:
            fire = True
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)

    if cooldown > 0:
        cooldown -= 1

    if fire and not fire_prev and cooldown == 0:
        threading.Thread(target=play_alert, daemon=True).start()
        cooldown = COOLDOWN_FRAMES

    fire_prev = fire

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(frame))
    video_label.config(image=img)
    video_label.image = img

    root.after(10, update_frame)

update_frame()
root.mainloop()
cap.release()
