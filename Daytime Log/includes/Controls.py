from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
#from kivy.properties import NumericProperty, ReferenceListProperty, AliasProperty
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from includes.TextInput import *
import re
from datetime import *
from kivy.clock import Clock
from kivy.core.window import Window

DefaultTimer=5 #default time for timer in minite

class DaytimeLog(RelativeLayout):
    timer=ObjectProperty(None)
    date1=ObjectProperty(None)
    menu=ObjectProperty(None)
    log=ObjectProperty(None)
    recordIndex=[]
    def __init__(self,window,**kwargs):
        super(DaytimeLog,self).__init__(**kwargs)
        self.center=window.center
    def resize(self,window):
        #seems that using window.center will cause some problems
        #self.center=window.center
        self.center_x=window.width/2
        self.center_y=window.height/2
    def DrawLog(self,log):
        sorted(log,key=lambda x:x['id'],reverse=True)
        i=0
        #When log is less than record,delete the extra lines
        if len(log)<=len(self.recordIndex):
            for record in log:
                self.recordIndex[i].time.text=record['time']
                self.recordIndex[i].duration.text=record['duration']
                if record['tag']:
                    self.recordIndex[i].job.text=record['tag']+": "+record['job']
                else :
                    self.recordIndex[i].job.text=record['job']
                i+=1
            for t in range(i,len(self.recordIndex)):
                self.log.remove_widget(self.recordIndex[i])
                del(self.recordIndex[i])
            if len(log)==0:
                self.AddNewLog()
        #else, add lines
        else :
            for record in self.recordIndex:
                record.time.text=log[i]['time']
                record.duration.text=log[i]['duration']
                if log[i]['tag']:
                    record.job.text=log[i]['tag']+": "+log[i]['job']
                else:
                    record.job.text=log[i]['job']
                i+=1
            for t in range(i,len(log)):
                recordtmp=Record(t)
                recordtmp.time.text=log[t]['time']
                recordtmp.duration.text=log[t]['duration']
                if log[t]['tag']:
                    recordtmp.job.text=log[t]['tag']+": "+log[t]['job']
                else:
                    recordtmp.job.text=log[t]['job']
                recordtmp.id=str(t)
                self.log.add_widget(recordtmp)
                #recordtmp.pos=(0,self.log.height-56*t)
                self.recordIndex.append(recordtmp)
        self.UpdateRecordPos()

    def GetLog(self,date1):
        data=[]
        for child in self.recordIndex[:]:
            match=re.search('.*: ',child.job.text)
            if match:
                tag=re.sub(': ','',match.group(0))
                job=child.job.text[match.end(0):]
            else:
                match=re.search('.*： ',child.job.text)
                if match:
                    tag=re.sub('： ','',match.group(0))
                    job=child.job.text[match.end(0):]
                else:
                    tag=""
                    job=child.job.text
            if(job!=''):
                dicttmp={'id':child.id,\
                         'day':date1,\
                         'time':child.time.text,\
                         'duration':child.duration.text,\
                         'tag':tag,\
                         'job':job}
                data.append(dicttmp)
        return data

    def AddNewLog(self):
        length=len(self.recordIndex)
        recordtmp=Record(length)
        self.log.add_widget(recordtmp)
        #recordtmp.pos=(0,-56*length)
        recordtmp.id=str(length)
        self.recordIndex.append(recordtmp)
        if recordtmp.id!='0':
            try:
                pre=self.recordIndex[-2]
                time=datetime.strptime(pre.time.text,'%H:%M')+timedelta(seconds=float(pre.duration.text)*3600)
                recordtmp.time.text=datetime.strftime(time,'%H:%M')
            except ValueError:
                pass
        self.UpdateRecordPos()

    def Remove(self,index):
        self.log.remove_widget(self.recordIndex[index])
        for child in self.recordIndex[index+1:]:
            number=int(child.id)-1
            child.id=str(number)
            #######################
            #child.y=-56*number
        del(self.recordIndex[index])
        self.UpdateRecordPos()

    def Insert(self,index):
        self.AddNewLog()
        for i in range(len(self.recordIndex)-1,index,-1):
            self.recordIndex[i].Copy(self.recordIndex[i-1])
        self.recordIndex[index].Clear()

    def ChangeTime(self,id):
        time=datetime.strptime(self.recordIndex[id].time.text,'%H:%M')+timedelta(seconds=float(self.recordIndex[id].duration.text)*3600)
        for record in self.recordIndex[id+1:]:
            record.time.text=datetime.strftime(time,'%H:%M')
            time=datetime.strptime(record.time.text,'%H:%M')+timedelta(seconds=float(record.duration.text)*3600)

    def ChangeDuration(self,timeDelta,id):
        hours=timeDelta.seconds/3600
        duration=float(self.recordIndex[id-1].duration.text)
        self.recordIndex[id-1].duration.text=str(hours+duration)

    def UpdateRecordPos(self):
        length=len(self.recordIndex)
        self.log.height=length*56
        height=self.log.height
        t=1
        for record in self.recordIndex[:]:
            record.y=height-56*t
            t+=1

    def OnDateChanged(self,date1):
        pass

class Menu(RelativeLayout):
    export=ObjectProperty(None)
    save=ObjectProperty(None)
    add=ObjectProperty(None)
    def Init(self,**kargs):
        try:
            self.save.bind(on_press=kargs['save'])
        except KeyError:
            pass

        try:
            self.export.bind(on_press=kargs['export'])
        except KeyError:
            pass

        try:
            self.add.bind(on_press=kargs['add'])
        except KeyError:
            pass


class Timer(Widget):
    timeSet=ObjectProperty(None)
    oper=ObjectProperty(None)
    TimerHandler=None
    TimeSet=30
    Time=None
    def __init__(self,**kwargs):
        super(Timer,self).__init__(**kwargs)
        #self.operation.bind(on_press=self.StartTimer)
    def StartTimer(self,instance):
        #print("StartTimer")
        if instance.text=="Start":
            try:
                self.TimeSet=datetime.strptime(self.timeSet.text,'%H:%M:%S')
            except ValueError:
                try:
                    self.TimeSet=datetime.strptime(self.timeSet.text,'%M:%S')
                except ValueError:
                    try:
                        minutes=re.match('[0-9]+',self.timeSet.text)[0]
                        self.TimeSet=datetime.strptime(minutes,'%M')
                    except TypeError:
                        self.TimeSet=datetime.strptime(str(DefaultTimer),'%S')
            Clock.schedule_once(self.Blink,self.TimeSet.second+self.TimeSet.minute*60+self.TimeSet.hour*3600)
            self.Time=self.TimeSet
            self.UpdateTime()
            self.TimerHandler=Clock.schedule_interval(self.UpdateTime,1)
            instance.text="Pause"
        else:
            Clock.unschedule(self.TimerHandler)
            instance.text="Start"
    #self.get_root_window()
    def Blink(self,accurateTime=None):
        self.oper.text="Start"
        Clock.unschedule(self.TimerHandler)
        self.timeSet.text=''
        #Window.minimize()
        Window.minimize()
        Window.restore()
        #Clock.schedule_once(Window.restore)
    def UpdateTime(self,accurateTime=None):
        self.Time-=timedelta(seconds=1)
        if self.Time.hour:
            self.timeSet.text=datetime.strftime(self.Time,'%H:%M:%S')
        else:
            self.timeSet.text=datetime.strftime(self.Time,'%M:%S')

class Date(Widget):
    year=ObjectProperty(None)
    month=ObjectProperty(None)
    day=ObjectProperty(None)
    preBtn=ObjectProperty(None)
    nexBtn=ObjectProperty(None)
    def GetDate(self):
        return self.year.text+self.month.text.zfill(2)+self.day.text.zfill(2)
    def SetDate(self,date):
        self.year.text=str(date.year)
        self.month.text=str(date.month).zfill(2)
        self.day.text=str(date.day).zfill(2)
    def Init(self,pre,nex):
        self.preBtn.bind(on_press=pre)
        self.nexBtn.bind(on_press=nex)


class Record(Widget):
    time=ObjectProperty(None)
    duration=ObjectProperty(None)
    job=ObjectProperty(None)
    delete=ObjectProperty(None)
    add=ObjectProperty(None)

    def __init__(self,id,**kwargs):
        super(Record,self).__init__(**kwargs)
        self.id=str(id)
        #self.delete.bind(on_press=self.Delete)
        #self.add.bind(on_press=self.Insert)

    def Delete(self,btn):
        self.time.Delete()
        self.duration.Delete()
        self.job.Delete()
        self.parent.parent.parent.Remove(int(self.id))
    def Insert(self,btn):
        self.parent.parent.parent.Insert(int(self.id))

    def Clear(self):
        self.time.text=""
        self.duration.text=""
        self.job.text=""

    def Copy(self,record):
        self.time.text=record.time.text
        self.duration.text=record.duration.text
        self.job.text=record.job.text
    '''
    def ChangeTime(self,timeDelta):
        self.parent.parent.ChangeTime(timeDelta,int(self.id))
    '''

    def ChangeTime(self):
        self.parent.parent.parent.ChangeTime(int(self.id))

    def ChangeDuration(self,timeDelta):
        if self.id!=0:
            self.parent.parent.parent.ChangeDuration(timeDelta,int(self.id))

    def AddNewLog(self):
        self.parent.parent.parent.AddNewLog()
