from kivy.app import App
from kivy.clock import *
#from kivy.uix.widget import Widget
#from kivy.properties import ObjectProperty
#from kivy.uix.textinput import TextInput
#from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from includes.Controls import *
from includes.DB import *
from json import *
from array import array
from datetime import date
import re

class DaytimeLogApp(App):
    daytimeLog=None
    dataBase=None
    def Init(self):
        #window resize
        def resize(*args):
            self.daytimeLog.resize(Window)
        Window.bind(on_resize=resize)
        #init DB
        self.dataBase=DBDaytimeLog()
        #Set date
        now=date.today()
        #Draw the log
        self.Draw(now)
        #Set auto save
        #autoSave=Clock.schedule_interval(self.SaveLog,1800)
        #Set Menu
        self.daytimeLog.menu.Init(save=self.SaveLog,export=self.Export,add=self.AddNewLog)
        self.daytimeLog.date1.Init(pre=self.PrevDay,nex=self.NextDay)
        self.daytimeLog.OnDateChanged=self.Draw

    def SaveLog(self,*args):
        date1=self.daytimeLog.date1.GetDate()
        data=self.daytimeLog.GetLog(date1)
        self.dataBase.Save(data)

    def Export(self,*args):
        pass

    def AddNewLog(self,*args):
        self.daytimeLog.AddNewLog()

    def Draw(self,date):
        self.daytimeLog.date1.SetDate(date)
        #Find the daytime log
        LogThisDay=self.dataBase.SearchDate(date)
        self.daytimeLog.DrawLog(LogThisDay)

    def PrevDay(self,*args):
        date1=datetime.strptime(self.daytimeLog.date1.GetDate(),'%Y%m%d')-timedelta(days=1)
        self.Draw(date1)

    def NextDay(self,*args):
        date1=datetime.strptime(self.daytimeLog.date1.GetDate(),'%Y%m%d')+timedelta(days=1)
        self.Draw(date1)

    def build(self):
        self.daytimeLog=DaytimeLog(Window)
        self.Init()
        return self.daytimeLog
if __name__=='__main__':
    DaytimeLogApp().run()
