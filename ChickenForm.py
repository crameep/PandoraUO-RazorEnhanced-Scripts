import clr, time, thread, sys, System

clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Data')
from System.Collections.Generic import List
from System import Byte
from System.Drawing import Point, Color, Size
from System.Windows.Forms import (Application, Button, Form, BorderStyle, Label, FlatStyle, TextBox, CheckBox, ProgressBar)
from System.Data import DataTable
import sys



def makeMournButton(text, width, height, location, click):
    button = Button()
    button.Text = text
    button.Width = width
    button.Height = height
    button.Location = location
    button.Click += click
    return button


class PekahBox(Form):
    ver = '0.01'
    name = 'PekahBox'
    w = 220
    h = 300

    def __init__(self):
        # self.Contents = contents       
        self.BackColor = Color.FromArgb(40,40,40)
        self.ForeColor = Color.FromArgb(255, 255, 255)
        self.Size = Size(self.w, self.h)
        self.Text = '{0} - v{1}'.format(self.name, self.ver)
        self.TopMost = True
        self.myButtons = []
        self.buttser = 1
        i = j = 0
        
        for j in range(5):
            for i in range(5):
                p = Point(i * 40 + 2,  j * 40 + 2)
                b  = makeMournButton(str(self.buttser), 40, 40, p, self.pushed)
                self.Controls.Add(b)
                self.myButtons.append(b)
                self.buttser += 1
            j += 1


    def pushed(self, sender, event):
        Misc.SendMessage("Player: " + Player.Name + " pressed button " + sender.Text)

                                      
        
form = PekahBox()
Application.Run(form)