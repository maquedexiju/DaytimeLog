from kivy.lang.builder import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window
from datetime import *
import re

DefaultTimer=30

Builder.load_file('includes/Controls/Timer.kv')
Builder.load_file('includes/Controls/ImageButton.kv')

class Timer(RelativeLayout):
    tips=ObjectProperty(None)
    timeSet=ObjectProperty(None)
    timeSetMask=ObjectProperty(None)
    clock=ObjectProperty(None)
    start=ObjectProperty(None)
    TimerHandler=None
    countDown=None
    lastTimer=ObjectProperty(None)
    def __init__(self,**kwargs):
        super(Timer,self).__init__(**kwargs)
        Clock.schedule_once(self.Init,0.5)

    def Init(self,time):
        self.timeSet.bind(text=self.TimeEdit)
        self.timeSet.bind(focus=self.StopEdit)
        self.timeSet.bind(on_text_validate=self.StartTimer)
        self.timeSetMask.bind(on_release=self.EnterEdit)
        self.start.bind(on_press=self.StartTimer)
        self.pause.bind(on_press=self.PauseTimer)
        self.stop.bind(on_press=self.StopTimerManually)
        #self.operation.bind(on_press=self.StartTimer)

    def EnterEdit(self,instance):
        self.timeSet.focus=True
    def TimeEdit(self,instance,value):
        #text=value
        text=value[0:instance.cursor_col+1]+"|"+value[instance.cursor_col+1:]
        self.timeSetMask.text=text
    def StopEdit(self,instance,value):
        if value==False:
            if instance.text=='':
                instance.text=str(DefaultTimer)
            self.timeSetMask.text=instance.text
        else:
            instance.text=''
            self.timeSetMask.text='|'
    def StartTimer(self,instance=None):
        if self.timeSet.text=='':
            self.timeSet.text=str(DefaultTimer)
        self.timeSetMask.x+=self.width*3
        self.start.x+=self.width*3
        self.stop.x-=self.width*3
        self.pause.x-=self.width*3
        self.clock.opacity=1
        self.lastTimer.text='Last timer started at '+datetime.strftime(datetime.now(),'%H:%M')
        #Set countDown
        try:
            self.countDown=datetime.strptime(self.timeSet.text,'%H:%M:%S')
        except ValueError:
            try:
                self.countDown=datetime.strptime(self.timeSet.text,'%M:%S')
            except ValueError:
                try:
                    minutes=int(re.match('[0-9]+',self.timeSet.text)[0])
                    if minutes>1440:
                        self.countDown=datetime.strptime('24:00','%H:%M')
                    elif minutes>60:
                        self.countDown=datetime.strptime(str(int(minutes/60))+":"+str(minutes-int(minutes/60)*60),'%H:%M')
                    elif minutes>0:
                        self.countDown=datetime.strptime(str(minutes),'%M')
                    else:
                        self.countDown=datetime.strptime(str(DefaultTimer),'%M')
                except TypeError:
                    self.countDown=datetime.strptime(str(DefaultTimer),'%M')
        Clock.schedule_once(self.StopTimer,self.countDown.second+self.countDown.minute*60+self.countDown.hour*3600)
        if self.countDown.hour:
            self.clock.text=datetime.strftime(self.countDown,'%H:%M:%S')
        else:
            self.clock.text=datetime.strftime(self.countDown,'%M:%S')
        self.TimerHandler=Clock.schedule_interval(self.UpdateTime,1)

    def StopTimer(self,accurateTime=None):
        self.StopTimerManually()
        #Window.minimize()
        #Window.restore()
        Window.raise_window()
    def UpdateTime(self,accurateTime=None):
        self.countDown-=timedelta(seconds=1)
        if self.countDown.hour:
            self.clock.text=datetime.strftime(self.countDown,'%H:%M:%S')
        else :
            self.clock.text=datetime.strftime(self.countDown,'%M:%S')
    def PauseTimer(self,instance):
        if self.TimerHandler.is_triggered :
            Clock.unschedule(self.TimerHandler)
            instance.background_normal='includes/icons/Start.png'
        else:
            self.TimerHandler=Clock.schedule_interval(self.UpdateTime,1)
            instance.background_normal='includes/icons/Pause.png'

    def StopTimerManually(self,instance=None):
        Clock.unschedule(self.TimerHandler)
        self.timeSetMask.x-=self.width*3
        self.clock.opacity=0
        self.start.x-=self.width*3
        self.stop.x+=self.width*3
        self.pause.x+=self.width*3
        self.pause.background_normal='includes/icons/Pause.png'

    '''
    def StartTimerManually(self,instance=None):
        try:
            if self.TimerHandler.is_triggered:
                pass
            else:
                self.StartTimer()
        except AttributeError:
            self.StartTimer()
    '''
