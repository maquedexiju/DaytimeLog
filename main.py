from kivy.config import Config
from kivy.app import App
from kivy.clock import *
from kivy.core.window import Window
from kivy.uix.screenmanager import *
from kivy.logger import Logger
import kivy.metrics
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
import os
import platform
import subprocess

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

        Logger.info('SYS_INFO: window size, %d, %d'%(Window.width, Window.height))
        def resize(*args):
                self.todayView.resize()
                self.historyView.resize()
                self.reportView.resize()
        Window.bind(on_resize=resize)

    def SysInit(self):
        BASEPATH=''
        userSystem=platform.system()
        Logger.info('SYS_INFO: system %s'%str(platform.uname()))
        if userSystem=='Window':
            pass
        elif userSystem=='Linux' :#and re.search('arm',platform.machine())!=None:
            #basepath
            if getattr( sys, 'frozen', False ) :
                BASEPATH=os.path.dirname(sys.executable)+'/'
            else :
                BASEPATH=''
            self.sysArgs['BASEPATH']=BASEPATH
            #filepath
            self.sysArgs['FILEPATH']=os.path.abspath('..')+'/'
            #size
            self.sysArgs['WIDTH']=Window.width
            self.sysArgs['HEIGHT']=Window.height
            #open shortcut
            self.sysArgs['DESKTOP']=False
            #keyboard mode
            Window.softinput_mode='below_target'
        else:#elif userSystem=='Darwin':
            #basepath
            if getattr( sys, 'frozen', False ) :
                BASEPATH=os.path.dirname(sys.executable)+'/'
            else :
                BASEPATH=''
            self.sysArgs['BASEPATH']=BASEPATH
            #file path
            filepath=os.path.expanduser('~')+'/.DaytimeLog'
            if not os.path.exists(filepath):
                os.mkdir(filepath)
            self.sysArgs['FILEPATH']=filepath+'/'
            #window size
            Window.size=375,667
            self.sysArgs['WIDTH']=kivy.metrics.dp(375)
            self.sysArgs['HEIGHT']=kivy.metrics.dp(667)
            #open shortcut
            self.sysArgs['DESKTOP']=True
        Logger.info('SYS_INFO: shortcut %s'%str(self.sysArgs['DESKTOP']))
        #database
        self.dataBase=DBDaytimeLog(self.sysArgs['FILEPATH'])
        self.sysArgs['DB']=self.dataBase
        #ScreenManager
        self.screenManager=MyScreenManager(transition=NoTransition())
        self.sysArgs['SM']=self.screenManager
        #window
        self.sysArgs['WINDOW']=Window
        #config file
        Config.read(BASEPATH+'includes/config.ini')
        #config logs
        Config.set('kivy','log_dir',self.sysArgs['FILEPATH'])
        #config logo
        #Config.set('kivy','window_icon', BASEPATH+'includes/icons/DaytimeLog.png')
        self.icon='includes/icons/DaytimeLog.png'
        #keyboard
        #Window.keyboard_on_key_down=


    def TaskInit(self):
        #in suppose that you use the app today and still open it tommorrow
        Window.bind(on_cursor_enter=self.RefreshContent)
        #when request close
        Window.bind(on_request_close=self.screenManager.OnLeaving)
        #listen to shortcut
        #self.screenManager.RequestKeyboard()
        #AutoSave

    def RefreshContent(self,*args):
        self.todayView.Refresh()

    def build(self):
        self.SysInit()
        self.ViewInit()
        self.TaskInit()
        #self.screenManager.current='reportView'
        return self.screenManager
if __name__=='__main__':
    try:
        DaytimeLogApp().run()
    except:
        Logger.critical('crashed',exc_info=True,stack_info=True)
