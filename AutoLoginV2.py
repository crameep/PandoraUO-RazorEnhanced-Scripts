 
from System.Threading import ThreadStart, Thread
import sys
sys.path.append(r'C:\Program Files (x86)\IronPython.StdLib.2.7.9')
import keyboard
Misc.SetSharedValue('check',0)
oldValue = -1 

password = "PASSWORD"

def login(password):
    Misc.Pause(500)
    for letter in password:
        if letter.isupper():
            keyboard.press('shift')
        keyboard.press_and_release(letter)
        keyboard.release('shift')
        Misc.Pause(200)
    Misc.Pause(1000)
    keyboard.press_and_release('enter')
    Misc.Pause(1000)
    keyboard.press_and_release('enter')
    Misc.Pause(1000)
    keyboard.press_and_release('enter')

def loginThread():
    global oldValue
    while True:       
        Misc.SendMessage('Running')
        if oldValue == Misc.ReadSharedValue('check'):
            Misc.FocusUOWindow()            
            login(password)
            break
        oldValue = Misc.ReadSharedValue('check')
        Misc.Pause(10000)
                    
t = Thread(ThreadStart(loginThread))
t.Start()
while True:
    doublecheck = Player.Hits
    x = Misc.ReadSharedValue('check')
    Misc.SetSharedValue('check',x + 1)
    Misc.Pause(9000)
    
    
    
    





   