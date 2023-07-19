import subprocess
import time
from datetime import datetime
from pynput.keyboard import Controller,Key
import webbrowser
from data import sched, wsched
import tkinter as tk

keyboard = Controller()
isStarted = False #classs
today = time.strftime("%A", time.localtime()) ##gets current time

root=tk.Tk()

screen = tk.Canvas(root, width=300, height=300)
screen.pack()

def zoombot ():
    if (today == "Wednesday"):
        for i in wsched:
         while True:
            if isStarted == False:
                if datetime.now().hour == int(i[1].split(':')[0]) and datetime.now().minute == int(i[1].split(':')[1]):
                    webbrowser.open(i[0])

                  ##  time.sleep(60)
                   ## with keyboard.pressed(Key.alt): Testing a feature to automatically turn on camera after 60 seconds has passed. Works for certain classes?
                   ##     keyboard.press('v')
                    isStarted = True
            elif isStarted == True:
                if datetime.now().hour == int(i[2].split(':')[0]) and datetime.now().minute == int(i[2].split(':')[1]):
                    with keyboard.pressed(Key.alt):
                        keyboard.press('q')
                    time.sleep(5)
                    keyboard.press(Key.enter)
                    isStarted = False
                    break
    else:
        for i in sched:
         while True:
            if isStarted == False:
                if datetime.now().hour == int(i[1].split(':')[0]) and datetime.now().minute == int(i[1].split(':')[1]):
                    webbrowser.open(i[0])
                 #   time.sleep(60)
                   # with keyboard.pressed(Key.alt):
                  #      keyboard.press('v')
                    isStarted = True
            elif isStarted == True:
                if datetime.now().hour == int(i[2].split(':')[0]) and datetime.now().minute == int(i[2].split(':')[1]):
                    with keyboard.pressed(Key.alt):
                         keyboard.press('q')
                    time.sleep(1)
                    keyboard.press(Key.enter)
                    isStarted = False
                    break




b1 = tk.Button(text='Run',command=zoombot,bg='brown',fg='white') #button to run zoom bot
b1.pack()
screen.create_window(150,150,window=b1)

root.mainloop()