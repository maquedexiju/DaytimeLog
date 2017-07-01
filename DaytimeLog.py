from kivy.config import Config
from kivy.app import App
from kivy.clock import *
from kivy.core.window import Window
from kivy.uix.screenmanager import *
from includes.Today import *
from includes.History import *
from includes.Report import *
from includes.DB import *
from includes.Controls.MyScreenManager import MyScreenManager
from json import *
from array import array
from datetime import date
import re
import sys

from kivy.uix.textinput import TextInput

class DaytimeLogApp(App):
    todayView=None
    historyView=None
    reportView=None
    dataBase=None
    screenManager=None
    keyboard=None
    sysArgs={}
    def ViewInit(self):
        self.todayView=TodayView('todayView',self.sysArgs)
        self.historyView=HistoryView('historyView',self.sysArgs)
        self.reportView=ReportView('reportView',self.sysArgs)
        #Set auto save
        #autoSave=Clock.schedule_interval(self.SaveLog,1800)
        #Set Menu
        self.screenManager.add_widget(self.todayView)
        self.screenManager.add_widget(self.historyView)
        self.screenManager.add_widget(self.reportView)

        Window.size=375,667
        def resize(*args):
                self.todayView.resize()
                self.historyView.resize()
                self.reportView.resize()
        Window.bind(on_resize=resize)

    def SysInit(self):
        #basepath
        if getattr( sys, 'frozen', False ) :
            BASEPATH=os.path.dirname(sys.executable)+'/'
        else :
            BASEPATH=''
        self.sysArgs['BASEPATH']=BASEPATH
        #database
        self.dataBase=DBDaytimeLog(BASEPATH)
        self.sysArgs['DB']=self.dataBase
        #ScreenManager
        self.screenManager=MyScreenManager(transition=NoTransition())
        self.sysArgs['SM']=self.screenManager
        #window
        self.sysArgs['WINDOW']=Window
        #config file
        Config.read(BASEPATH+'includes/config.ini')

    def TaskInit(self):
        #in suppose that you use the app today and still open it tommorrow
        Window.bind(on_cursor_enter=self.RefreshContent)
        #when request close
        Window.bind(on_request_close=self.screenManager.OnLeaving)
        #listen to shortcut
        self.screenManager.RequestKeyboard()

    def RefreshContent(self,*args):
        self.todayView.Refresh()

    def build(self):
        self.SysInit()
        self.ViewInit()
        self.TaskInit()
        #self.screenManager.current='reportView'
        return self.screenManager
if __name__=='__main__':
    DaytimeLogApp().run()
