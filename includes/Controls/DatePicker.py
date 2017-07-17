from kivy.clock import Clock
from kivy.lang.builder import Builder
import kivy.metrics
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.logger import Logger
import re
from includes.Controls.TextInput import YearInput,MonthInput,StartTimeInput,EndTimeInput
from datetime import *
from string import *
import calendar

Builder.load_file('includes/Controls/DatePicker.kv')
Builder.load_file('includes/Controls/ImageButton.kv')

class Dates(RelativeLayout):
    yearInput=ObjectProperty(None)
    monthInput=ObjectProperty(None)
    startTimeInput=ObjectProperty(None)
    endTimeInput=ObjectProperty(None)
    canlerderDays=ObjectProperty(None)
    confrim=ObjectProperty(None)
    '''
    yesterday=ObjectProperty(None)
    lastWeek=ObjectProperty(None)
    thisWeek=ObjectProperty(None)
    '''
    indexCalendar=[]
    startYear=None
    startMonth=None
    startDay=None
    endYear=None
    endMonth=None
    endDay=None
    inFrequentlyUsed=False
    def __init__(self,**kwargs):
        super(Dates,self).__init__(**kwargs)
        def laterInit(time=None):
            #the date input
            self.yearInput.focus_next=self.monthInput
            self.yearInput.focus_previous=None
            self.monthInput.focus_previous=self.yearInput
            self.monthInput.focus_next=None
            self.monthInput.ConfirmDate=self.ChooseMonth
            #the time input
            self.startTimeInput.focus_next=self.endTimeInput
            self.startTimeInput.focus_previous=None
            self.endTimeInput.focus_previous=self.startTimeInput
            self.endTimeInput.focus_next=None
            self.startTimeInput.SetStartTime=self.SetStartTime
            self.endTimeInput.SetEndTime=self.SetEndTime
            #init confirm
            self.confirm.bind(on_press=self.on_confirm)
            #init frequently used
            self.yesterday.bind(on_press=self.ChooseFrequentlyUsed)
            self.lastWeek.bind(on_press=self.ChooseFrequentlyUsed)
            self.thisWeek.bind(on_press=self.ChooseFrequentlyUsed)
        Clock.schedule_once(laterInit,0.5)

    def setView(self,startTime=None,endTime=None):
        #init
        if not startTime:
            #set year and month
            year=date.today().year
            month=date.today().month
            #set start and end
            startTime=date.today()-timedelta(days=date.today().weekday())
            endTime=date.today()+timedelta(days=6-date.today().weekday())
            self.thisWeek.state="down"
            self.inFrequentlyUsed==True
        else :
            year=endTime.year
            month=endTime.month
        startTimeinString=datetime.strftime(startTime,'%Y-%m-%d')
        endTimeinString=datetime.strftime(endTime,'%Y-%m-%d')
        #set self.start end ...
        self.startYear=startTime.year
        self.startMonth=startTime.month
        self.startDay=startTime.day
        self.endYear=endTime.year
        self.endMonth=endTime.month
        self.endDay=endTime.day
        #set year and month input
        self.yearInput.text=str(year)
        self.monthInput.text=str(month).zfill(2)
        #draw dates
        self.DrawDates(year,month)
        #set time input
        self.startTimeInput.text=startTimeinString
        self.endTimeInput.text=endTimeinString
        #set highlight
        self.DrawHighLightDays()


    def DrawDates(self,year,month):
        #used to draw the calendar
        #clear the days before
        self.canlerderDays.clear_widgets()
        self.indexCalendar=[]
        #judge if the day is beyond today
        days=calendar.monthcalendar(year,month)
        if year>date.today().year or (month>date.today().month and year==date.today().year):
            beyondToday=0
        elif month==date.today().month and year==date.today().year:
            beyondToday=date.today().day
        else:
            beyondToday=31
        #start draw
        i=0
        for week in days:
            j=0
            for day in week:
                if day!=0:
                    dayView=OneDay()
                    dayView.day.text=str(day)
                    dayView.id='day'+str(day)
                    self.canlerderDays.add_widget(dayView)
                    dayView.pos=int(self.canlerderDays.width/7)*j,kivy.metrics.dp(36)*(4-i)
                    dayView.size=int(self.canlerderDays.width/7),kivy.metrics.dp(36)
                    dayView.SetTime=self.SetTime
                    self.indexCalendar.append(dayView)
                    if day>beyondToday:
                        dayView.disabled=True
                j+=1
            i+=1

    def ChooseMonth(self,instance):
        year=int(instance.focus_previous.text)
        month=int(instance.text)
        instance.text=str(month).zfill(2)
        self.DrawDates(year,month)
        self.DrawHighLightDays()
        instance.focus=False

    def SetTime(self,day):
        if (not re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}',self.startTimeInput.text)) or self.startTimeInput.choosed==True:
            self.startTimeInput.text=self.yearInput.text+'-'+self.monthInput.text+'-'+str(day).zfill(2)
            self.startYear=int(self.yearInput.text)
            self.startMonth=int(self.monthInput.text)
            self.startDay=int(day)
            self.startTimeInput.choosed=False
            if re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}',self.endTimeInput.text) :
                if self.startTimeInput.text>self.endTimeInput.text:
                    self.endTimeInput.text=''
                    self.endYear=None
                    self.endMonth=None
                    self.endDay=None
            self.endTimeInput.focus=True
            self.DrawHighLightDays()
        else:
            self.endYear=int(self.yearInput.text)
            self.endMonth=int(self.monthInput.text)
            self.endDay=int(day)
            endTime=self.yearInput.text+'-'+self.monthInput.text+'-'+str(day).zfill(2)
            startTime=self.startTimeInput.text
            '''
            if endTime<startTime:
                startTime,endTime=endTime,startTime
                self.startYear,self.endYear=self.endYear,self.startYear
                self.startMonth,self.endMonth=self.endMonth,self.startMonth
                self.startDay,self.endDay=self.endDay,self.startDay
                self.startTimeInput.text=startTime
            '''
            self.endTimeInput.text=endTime
            self.DrawHighLightDays()

    def SetStartTime(self,instance):
        if instance.text>datetime.strftime(date.today(),'%Y-%m-%d') or not re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}',instance.text):
            instance.text=datetime.strftime(date.today(),'%Y-%m-%d')
        time=re.findall('[0-9]+',instance.text)
        self.startYear=int(time[0])
        self.yearInput.text=time[0]
        self.startMonth=int(time[1])
        self.monthInput.text=time[1]
        self.startDay=int(time[2])
        self.DrawHighLightDays()
        instance.focus_next.focus=True
        instance.choosed=False

    def SetEndTime(self,instance):
        if instance.text>datetime.strftime(date.today(),'%Y-%m-%d') or not re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}',instance.text):
            instance.text=datetime.strftime(date.today(),'%Y-%m-%d')
        time=re.findall('[0-9]+',instance.text)
        self.endYear=int(time[0])
        self.yearInput.text=time[0]
        self.endMonth=int(time[1])
        self.monthInput.text=time[1]
        self.endDay=int(time[2])
        self.DrawHighLightDays()
        self.Confirm(self.startTimeInput.text,self.endTimeInput.text)

    def ChooseFrequentlyUsed(self,instance):
        instance.state='down'
        self.inFrequentlyUsed=True
        if instance.text=='Last Week':
            startTime=date.today()-timedelta(days=7+date.today().weekday())
            self.startYear=startTime.year
            self.startMonth=startTime.month
            self.startDay=startTime.day
            startTimeinString=datetime.strftime(startTime,'%Y-%m-%d')
            endTime=date.today()-timedelta(days=1+date.today().weekday())
            self.endYear=endTime.year
            self.endMonth=endTime.month
            self.endDay=endTime.day
            endTimeinString=datetime.strftime(endTime,'%Y-%m-%d')
        elif instance.text=='This Week':
            startTime=date.today()-timedelta(days=date.today().weekday())
            self.startYear=startTime.year
            self.startMonth=startTime.month
            self.startDay=startTime.day
            startTimeinString=datetime.strftime(startTime,'%Y-%m-%d')
            endTime=date.today()+timedelta(days=6-date.today().weekday())
            self.endYear=endTime.year
            self.endMonth=endTime.month
            self.endDay=endTime.day
            endTimeinString=datetime.strftime(endTime,'%Y-%m-%d')
        elif instance.text=='Yesterday':
            startTime=date.today()-timedelta(days=1)
            self.startYear=startTime.year
            self.startMonth=startTime.month
            self.startDay=startTime.day
            startTimeinString=datetime.strftime(startTime,'%Y-%m-%d')
            endTime=date.today()-timedelta(days=1)
            self.endYear=endTime.year
            self.endMonth=endTime.month
            self.endDay=endTime.day
            endTimeinString=datetime.strftime(endTime,'%Y-%m-%d')
        self.startTimeInput.text=startTimeinString
        self.endTimeInput.text=endTimeinString
        self.DrawHighLightDays()
        self.Confirm(startTimeinString,endTimeinString)

    def Confirm(self,startTime,endTime):
        pass

    def on_confirm(self,instance):
        self.Confirm(self.startTimeInput.text,self.endTimeInput.text)

    def DrawHighLightDays(self):
        #set for frequently used
        if self.inFrequentlyUsed==True:
            self.inFrequentlyUsed=False
        else:
            self.yesterday.state='normal'
            self.lastWeek.state='normal'
            self.thisWeek.state='normal'
        #judge the start and end
        start=None
        end=None
        if self.startYear==None:
            pass
        elif self.endYear==None:
            if self.startMonth==int(self.monthInput.text) and self.startYear==int(self.yearInput.text):
                start=self.startDay-1
                end=self.startDay
        else:
            if self.startYear<=int(self.yearInput.text) and self.startMonth<int(self.monthInput.text):
                start=0
            elif self.startYear==int(self.yearInput.text) and self.startMonth==int(self.monthInput.text):
                start=self.startDay-1
            if self.endYear>=int(self.yearInput.text) and self.endMonth>int(self.monthInput.text):
                end=None
            elif self.endYear==int(self.yearInput.text) and self.endMonth==int(self.monthInput.text):
                end=self.endDay
            else:
                start=None
        #start drawing
        if start!=None:
            for oneDay in self.indexCalendar[:]:
                oneDay.day.state='normal'
            for oneDay in self.indexCalendar[start:end]:
                oneDay.day.state='down'

class OneDay(RelativeLayout):
    day=ObjectProperty(None)
    def Checked(self,instance):
        self.SetTime(int(instance.text))

    def SetTime(self,day):
        pass

class DatePicker(RelativeLayout):
    startTime=None
    endTime=None
    def __init__(self,**kwargs):
        super(DatePicker,self).__init__(**kwargs)
        def laterInit(time=None):
            #self.mask.x=self.to_local(0+self.width*3,0)
            self.mask.pos=self.to_local(0+self.width*3,0)
            Logger.info('DATEPICKER: parent size, %d, %d, mask size, %d, %d'%(self.parent.width,self.parent.height,self.width,self.height))
            Logger.info('DATEPICKER: mask position, %d, %d'%(self.mask.x,self.mask.y))
            self.picker.center=self.to_local(self.parent.width/2+self.width*3,self.parent.height/2)
            self.picker.Confirm=self.SetDate
            self.prevRange.bind(on_press=self.JumpPrev)
            self.nextRange.bind(on_press=self.JumpNext)
        Clock.schedule_once(laterInit,0.5)

    def Init(self):
        self.picker.setView()
        startTime=self.picker.startTimeInput.text
        endTime=self.picker.endTimeInput.text
        self.startTime=startTime
        self.endTime=endTime
        self.result.text=startTime+' To '+endTime
        #self.DrawLog(startTime,endTime)


    def CloseDates(self,time=None):
        self.mask.x+=self.width*3
        self.picker.center_x+=self.width*3

    def OpenDates(self):
        self.mask.x-=self.width*3
        self.picker.center_x-=self.width*3

    def GetDate(self):
        return {'startTime':self.startTime,'endTime':self.endTime}

    def SetDate(self,startTime,endTime):
        self.startTime=startTime
        self.endTime=endTime
        self.result.text=startTime+' To '+endTime
        self.DrawLog(startTime,endTime)
        Clock.schedule_once(self.CloseDates,0.4)

    def DrawLog(self,startTime,endTime):
        #Reserved for the parent class
        pass

    def JumpPrev(self,instance):
        timeDelta=datetime.strptime(self.endTime,'%Y-%m-%d')-datetime.strptime(self.startTime,'%Y-%m-%d')
        endTime=datetime.strptime(self.startTime,'%Y-%m-%d')-timedelta(days=1)
        self.endTime=datetime.strftime(endTime,'%Y-%m-%d')
        startTime=datetime.strptime(self.startTime,'%Y-%m-%d')-timeDelta-timedelta(days=1)
        self.startTime=datetime.strftime(startTime,'%Y-%m-%d')
        self.picker.setView(startTime,endTime)
        self.result.text=self.startTime+' To '+self.endTime
        self.DrawLog(self.startTime,self.endTime)

    def JumpNext(self,instance):
        timeDelta=datetime.strptime(self.endTime,'%Y-%m-%d')-datetime.strptime(self.startTime,'%Y-%m-%d')
        startTime=datetime.strptime(self.endTime,'%Y-%m-%d')+timedelta(days=1)
        if startTime>datetime.today():
            return
        self.startTime=datetime.strftime(startTime,'%Y-%m-%d')
        endTime=datetime.strptime(self.endTime,'%Y-%m-%d')+timeDelta+timedelta(days=1)
        self.endTime=datetime.strftime(endTime,'%Y-%m-%d')
        self.picker.setView(startTime,endTime)
        self.result.text=self.startTime+' To '+self.endTime
        self.DrawLog(self.startTime,self.endTime)
