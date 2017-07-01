from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.lang.builder import Builder
from kivy.clock import Clock
import kivy.metrics
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.effects.scroll import ScrollEffect
from includes.Controls.TextInput import *
import re
from datetime import *
from string import *

Builder.load_file('includes/Controls/Log.kv')
#Builder.load_file('includes/Controls/ImageButton.kv')
class Log(RelativeLayout):
    viewMode=False
    indexLogs=[]
    def __init__(self,**kwargs):
        super(Log,self).__init__(**kwargs)
        self.indexLogs=[]
        def laterInit(time=None):
            self.title.edit.bind(on_press=self.EnterEdit)
        Clock.schedule_once(laterInit,0.2)

    def DrawLog(self,records,date):
        log=LogOneDay(date,self.viewMode,self.width)
        self.logAll.add_widget(log)
        log.DrawLog(records)
        #self.logAll.height+=log.height
        self.indexLogs.append(log)
        self.UpdateHeight()

    def Clear(self):
        self.logAll.clear_widgets()
        self.indexLogs=[]

    def GetLog(self):
        data=[]
        for logOneDay in self.indexLogs[:]:
            data+=logOneDay.GetLog()
        return data

    def EnterEdit(self,instance=None):
        self.title.edit.funbind('on_press',self.EnterEdit)
        self.title.edit.bind(on_press=self.LeaveEdit)
        self.title.edit.text='Done'
        self.title.date.text=instance.parent.date.text
        for logOneDay in self.indexLogs[:]:
            if logOneDay.id!=self.title.date.text:
                self.logAll.remove_widget(logOneDay)
            else :
                logOneDay.EnterEdit()
        self.scrollView.scroll_y=1
        self.UpdateHeight()

    def LeaveEdit(self,instance=None):
        self.logAll.children[0].LeaveEdit()
        self.logAll.clear_widgets()
        for logOneDay in self.indexLogs[:]:
            self.logAll.add_widget(logOneDay)
        self.UpdateHeight()
        self.title.edit.funbind('on_press',self.LeaveEdit)
        self.title.edit.text='Edit'
        self.title.edit.bind(on_press=self.EnterEdit)

    def UpdateHeight(self):
        self.logAll.height=0
        self.scrollView.indexPostion=[]
        for logOneDay in self.logAll.children[::-1]:
            self.scrollView.indexPostion.append({'position':self.logAll.height,'id':logOneDay.id})
            self.logAll.height+=logOneDay.height
        self.logAll.y=self.scrollView.height-self.logAll.height+self.scrollView.y

class LogOneDay(StackLayout):
    log=ObjectProperty(None)
    addRecord=None
    recordIndex=[]
    editMode=False
    viewMode=False
    '''
    def Init(self,log):
        def laterInit(self,time=None):
            #self.DrawLog(log)
            pass
        Clock.schedule_once(laterInit,0.5)
    '''
    def __init__(self,date,viewMode,width,**kwargs):
        super(LogOneDay,self).__init__(**kwargs)
        self.recordIndex=[]
        self.id=date
        self.title.date.text=date
        self.viewMode=viewMode
        self.width=width
        if viewMode==False:
            self.addRecord=AddRecord()
            self.addRecord.width=self.width
            self.addRecord.btn.bind(on_press=self.AddNewLog)
            self.add_widget(self.addRecord)
        def laterInit(time=None):
            self.title.edit.bind(on_press=self.PressEdit)
        Clock.schedule_once(laterInit,0.5)

    def DrawLog(self,log):
        sorted(log,key=lambda x:x['id'],reverse=True)
        i=0
        #draw logs
        for t in range(0,len(log)):
            recordtmp=Record(t)
            recordtmp.time.text=log[t]['time']
            recordtmp.duration.text=log[t]['duration']
            if log[t]['tag']:
                recordtmp.job.text=log[t]['tag']+": "+log[t]['job']
            else:
                recordtmp.job.text=log[t]['job']
            recordtmp.width=self.width
            self.log.add_widget(recordtmp)
            #recordtmp.pos=(0,self.log.height-56*t)
            self.recordIndex.append(recordtmp)
        if len(log)==0:
            if self.viewMode==True:
                emptyLog=LogEmpty()
                emptyLog.width=self.width
                self.log.add_widget(emptyLog)
            else:
                self.AddNewLog()
        self.UpdateHeight()

    def AddNewLog(self,instance=None):
        length=len(self.recordIndex)
        if length==0 and self.viewMode==True:
            self.log.clear_widgets()
        recordtmp=Record(length)
        self.log.add_widget(recordtmp)
        #recordtmp.pos=(0,-56*length)
        recordtmp.width=self.width
        self.recordIndex.append(recordtmp)
        if recordtmp.id!='0':
            try:
                pre=self.recordIndex[-2]
                time=datetime.strptime(pre.time.text,'%H:%M')+timedelta(seconds=float(pre.duration.text)*3600)
                recordtmp.time.text=datetime.strftime(time,'%H:%M')
            except ValueError:
                pass
        if self.editMode==True:
            recordtmp.insert.x-=self.width*3
            recordtmp.delete.x-=self.width*3
        self.UpdateHeight()

    def Remove(self,index):
        self.log.remove_widget(self.recordIndex[index])
        for child in self.recordIndex[index+1:]:
            number=int(child.id)-1
            child.id=str(number)
            #######################
            #child.y=-56*number
        self.recordIndex[index].Delete()
        del(self.recordIndex[index])
        if len(self.recordIndex)==0:
            if self.viewMode==True:
                emptyLog=LogEmpty()
                emptyLog.width=self.width
                self.log.add_widget(emptyLog)
            else:
                self.AddNewLog()
        self.UpdateHeight()

    def Insert(self,index):
        self.AddNewLog()
        for i in range(len(self.recordIndex)-1,index,-1):
            self.recordIndex[i].Copy(self.recordIndex[i-1])
        self.recordIndex[index].Clear()

    def UpdateHeight(self):
        length=len(self.log.children)
        self.log.height=length*kivy.metrics.dp(72)
        if self.viewMode==True and self.editMode==False:
            self.height=self.log.height+kivy.metrics.dp(30)
        else:
            self.height=self.log.height+kivy.metrics.dp(102)
        #self.parent.parent.parent.UpdateHeight()

    def ChangeTime(self,id,timeDelta):
        if id>0:
            durationPrevintimeDelta=datetime.strptime(self.recordIndex[id].time.text,'%H:%M')-datetime.strptime(self.recordIndex[id-1].time.text,'%H:%M')
            durationPrevinFLoat=durationPrevintimeDelta.seconds/3600
            if durationPrevinFLoat<0:
                self.recordIndex[id].text=self.recordIndex[id-1].text
            else:
                self.recordIndex[id-1].duration.text=str(durationPrevinFLoat)
        for record in self.recordIndex[id+1:]:
            time=datetime.strptime(record.time.text,'%H:%M')+timeDelta
            record.time.text=datetime.strftime(time,'%H:%M')

    def GetLog(self):
        data=[]
        date1=self.id
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

    def EnterEdit(self,instance=None):
        for record in self.recordIndex[:]:
            record.insert.x-=self.width*3
            record.delete.x-=self.width*3
        self.editMode=True
        if self.viewMode==True:
            self.addRecord=AddRecord()
            self.addRecord.width=self.width
            self.addRecord.btn.bind(on_press=self.AddNewLog)
            self.add_widget(self.addRecord)
            self.UpdateHeight()
        '''
        self.title.edit.text='Done'
        self.title.edit.funbind('on_press',self.EnterEdit)
        self.title.edit.bind(on_press=self.LeaveEdit)
        '''

    def PressEdit(self,instance=None):
        self.parent.parent.parent.EnterEdit(instance)

    def LeaveEdit(self,instance=None):
        for record in self.recordIndex[:]:
            record.insert.x+=self.width*3
            record.delete.x+=self.width*3
        self.editMode=False
        if self.viewMode==True:
            self.remove_widget(self.addRecord)
            self.addRecord=None
            self.UpdateHeight()
        '''
        self.title.edit.text='Edit'
        self.title.edit.funbind('on_press',self.LeaveEdit)
        self.title.edit.bind(on_press=self.EnterEdit)
        self.parent.parent.parent.LeaveEdit(self.id)
        '''

class Record(RelativeLayout):
    time=ObjectProperty(None)
    duration=ObjectProperty(None)
    job=ObjectProperty(None)
    id=None
    def __init__(self,id=None,**kwargs):
        super(Record,self).__init__(**kwargs)
        self.id=str(id)
        self.duration.AutoDuration=self.AutoDuration

    def Delete(self):
        self.time.Delete()
        self.duration.Delete()
        self.job.Delete()

    def Insert(self,btn):
        self.parent.parent.Insert(int(self.id))

    def Clear(self):
        self.time.text=""
        self.duration.text=""
        self.job.text=""

    def Copy(self,record):
        self.time.text=record.time.text
        self.duration.text=record.duration.text
        self.job.text=record.job.text

    def TimeChanged(self,timeDelta):
        self.parent.parent.ChangeTime(int(self.id),timeDelta)

    def AddNewLog(self):
        self.parent.parent.AddNewLog()

    def AutoDuration(self):
        if re.match('[0-9]+:[0-9]+',self.time.text):
            now=datetime.now()
            start=datetime.strptime(str(date.today())+' '+self.time.text,'%Y-%m-%d %H:%M')
            timeDelta=now-start
            seconds=timeDelta.seconds
            hour=int(seconds/3600)
            minute=float('%.2f'%(int((seconds-hour*3600)/60)/60))
            return str(hour+minute)
        else:
            return 'Duration'

class AddRecord(RelativeLayout):
    pass

class LogEmpty(RelativeLayout):
    pass

class MyScrollView(ScrollView):
    indexPostion=[]
    formerSize=None
    def __init__(self,**kwargs):
        super(MyScrollView,self).__init__(**kwargs)
        self.indexPostion=[]
        self.effect_cls=ScrollEffect
        self.formerSize=0

    def update_from_scroll(self,pos):
        #scroll
        x=0+self.x
        y=(self.height-self.children[0].height)*(self.scroll_y)+self.y #if self.height<self.children[0].height else
        self.children[0].pos=[x,y]
        #set title
        position=self.children[0].height-self.height+y
        for i in range(0,len(self.indexPostion)):
            if position>=self.indexPostion[i]['position'] and (i==len(self.indexPostion)-1 or position<self.indexPostion[i+1]['position']):
                self.parent.title.date.text=self.indexPostion[i]['id']
                break
            i+=1
