from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from includes.Controls.AdaptView import AdaptView
from includes.Controls.Navigator import Navigator
from includes.Controls.DatePicker import DatePicker
from includes.Controls.Menu import Menu
from includes.Controls.Log import Log
import re
from datetime import *
import csv
import platform
import subprocess

Builder.load_file('includes/History.kv')

class HistoryView(AdaptView):
    menu=ObjectProperty(None)
    navigator=ObjectProperty(None)
    log=ObjectProperty(None)
    datePicker=ObjectProperty(None)
    def __init__(self,screenName,sysArgs,**kwargs):
        super(HistoryView,self).__init__(screenName,sysArgs,**kwargs)
        #self.menu.Init(Save=self.SaveLog,Export=self.ExportLog)
        self.menu.Init(Export=self.ExportLog)
        self.navigator.Init(1)
        self.datePicker.DrawLog=self.DrawLog
        self.log.viewMode=True
        def laterInit(time=None):
            self.datePicker.Init()
        Clock.schedule_once(laterInit,0.5)

    def on_enter(self):
        time=self.datePicker.GetDate()
        startTime=time['startTime']
        endTime=time['endTime']
        def tmpfunction(time=None):
            self.DrawLog(startTime,endTime)
        Clock.schedule_once(tmpfunction,0.4)
        super(HistoryView, self).on_enter()

    def on_leave(self,*args):
        self.SaveLog()
        super(HistoryView,self).on_leave()

    def DrawLog(self,startTimeinString,endTimeinString):
        startTime=datetime.strptime(startTimeinString,'%Y-%m-%d')
        endTime=datetime.strptime(endTimeinString,'%Y-%m-%d') if datetime.strptime(endTimeinString,'%Y-%m-%d')<datetime.now() else datetime.now()
        dayDelta=endTime-startTime
        self.log.Clear()
        for i in range(0,dayDelta.days+1):
            date1=startTime+timedelta(days=i)
            LogThisDay=self.DB.SearchDate(date1)
            self.log.DrawLog(LogThisDay,datetime.strftime(date1,'%Y-%m-%d'))

    def SaveLog(self,instance=None):
        data=self.log.GetLog()
        self.DB.Save(data)

    def ExportLog(self,instance=None):
        data=self.log.GetLog()
        filePath=self.FILEPATH+'tmp.csv'
        with open(filePath, 'w',encoding='utf-8') as csvFile:
            fieldNames=['ID','Start Time','Duration','Tag','Content']
            writer=csv.DictWriter(csvFile, fieldnames=fieldNames)
            writer.writeheader()
            day=None
            for record in data:
                if record['day']!=day:
                    writer.writerow({'ID':record['day']})
                    day=record['day']
                writer.writerow({'ID':record['id'],\
                #'Date':record['day'],\
                'Start Time':record['time'],\
                'Duration':record['duration'],\
                'Tag':record['tag'],\
                'Content':record['job']})
            sys=platform.system()
            if sys=='Window':
                os.startfile(filePath)
            elif sys=='Linux':
                subprocess.call(["xdg-open", filePath])
            elif sys=='Darwin':
                subprocess.call(["open", filePath])
