from kivy.lang.builder import Builder
from kivy.clock import Clock
from includes.Controls.AdaptView import AdaptView
from includes.Controls.Reports import Reports
from datetime import *
import csv
import platform
import subprocess

Builder.load_file('includes/Report.kv')

class ReportView(AdaptView):
    tags=None
    def __init__(self,screenName,sysArgs,**kwargs):
        super(ReportView,self).__init__(screenName,sysArgs,**kwargs)
        self.menu.Init(Export=self.ExportLog)
        self.navigator.Init(2)
        self.datePicker.DrawLog=self.DrawLog
        self.tags={}
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

    def ExportLog(self,instance=None):
        filePath=self.FILEPATH+'tmp.csv'
        with open(filePath, 'w',encoding='utf-8') as csvFile:
            fieldNames=['Tag','Total Time(Hour)','Content','Time(Hour)']
            writer=csv.DictWriter(csvFile, fieldnames=fieldNames)
            writer.writeheader()
            for (tag,info) in self.tags.items():
                firstLine=True
                for (job,duration) in info['job'].items():
                    if firstLine==True:
                        firstLine=False
                        writer.writerow({'Tag':tag,'Total Time(Hour)':info['duration'],'Content':job,'Time(Hour)':duration})
                    else:
                        writer.writerow({'Content':job,'Time(Hour)':duration})
            sys=platform.system()
            if sys=='Window':
                os.startfile(filePath)
            elif sys=='Linux':
                subprocess.call(["xdg-open", filePath])
            elif sys=='Darwin':
                subprocess.call(["open", filePath])

    def DrawLog(self,startTimeinString,endTimeinString):
        self.tags={}
        '''
        tag{
            'tag1':{
                'duration':''
                'job':{
                    'job1':'duration'
                    'job2':'duration'
                },
            'tag2':{
                .
                .
                .
                }
            }

        }
        '''
        startTime=datetime.strptime(startTimeinString,'%Y-%m-%d')
        endTime=datetime.strptime(endTimeinString,'%Y-%m-%d') if datetime.strptime(endTimeinString,'%Y-%m-%d')<datetime.now() else datetime.now()
        dayDelta=endTime-startTime
        for i in range(0,dayDelta.days+1):
            date1=startTime+timedelta(days=i)
            data=self.DB.SearchDate(date1)
            #process data in one day
            for datum in data:
                #if the tag exists?
                if datum['tag']:
                    #if the tag already in record?
                    if datum['tag'] in self.tags.keys():
                        #if the job already in record
                        if datum['job'] in self.tags[datum['tag']]['job'].keys():
                            self.tags[datum['tag']]['job'][datum['job']]+=float(datum['duration'])
                        else:
                            self.tags[datum['tag']]['job'][datum['job']]=float(datum['duration'])
                        self.tags[datum['tag']]['duration']+=float(datum['duration'])
                    else:
                        #if tag is not in tags, add it
                        self.tags[datum['tag']]={'duration':float(datum['duration']),'job':{datum['job']:float(datum['duration'])}}
        self.reports.Clear()
        self.reports.DrawReports(self.tags)
