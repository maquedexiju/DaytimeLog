from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
import re
from datetime import *
from string import *

class TabTextInput(TextInput):
    '''
    __last=None
    pre=None
    nex=None
    id1=0
    '''
    def __init__(self,**kwargs):
        super(TabTextInput,self).__init__(**kwargs)
        self.font_name="includes/fzltqh.ttf"
        #self.multiline=False
        self.font_size="12sp"
        #self.keybindings='emacs'
        self.keyboard=Window.request_keyboard(self.callback,self,input_type="text")
        self.keyboard_on_key_down=self.OnKeyDown
        '''
        try:
            pre=kwargs['pre']
            self.pre=pre
            pre.nex.pre=self
            self.nex=pre.nex
            pre.nex=self
        except KeyError:
            self.pre=TabTextInput.__last
            try:
                TabTextInput.__last.nex=self
            except AttributeError:
                pass
            self.id1=TabTextInput.id1
            TabTextInput.id1+=1
            TabTextInput.__last=self
        '''

    def OnKeyDown(self,keyboard,keycode=None,text=None,modifier=None,**kwargs):
        if keycode[1]=='tab':
            if modifier==['shift']:
                try:
                    #self.focus=False
                    self.focus_previous.focus=True
                except AttributeError:
                    pass
            else:
                try:
                    #self.focus=False
                    self.focus_next.focus=True
                except AttributeError:
                    pass
        elif keycode[1]=='escape':
            pass
        else:
            super(TabTextInput,self).keyboard_on_key_down(keyboard,keycode,text,modifier,**kwargs)

        return True

    def callback(self):
        #Window.release_keyboard(self.keyboard)
        pass

    def Delete(self):
        try:
            self.focus_previous.focus_next=self.focus_next
        except AttributeError:
            pass
        try:
            self.focus_next.focus_previous=self.focus_previous
        except AttributeError:
            pass

    '''
    def GetLast():
        return TabTextInput.__last
    '''

class TimeInput(TabTextInput):
    contentTmp=None
    def __init__(self,**kwargs):
        super(TimeInput,self).__init__(**kwargs)
        self.input_type="number"
        def laterInit(time=None):
            if self.parent.id=='0':
                self.focus_previous==None
            else:
                self.focus_previous=self.parent.parent.parent.recordIndex[int(self.parent.id)-1].job
                self.parent.parent.parent.recordIndex[int(self.parent.id)-1].job.focus_next=self
            self.focus_next=self.parent.duration
        Clock.schedule_once(laterInit,0.2)

    def on_focus(self,instance,value):
        if value==True:
            self.contentTmp=self.text
        else:
            if self.contentTmp!=self.text:
                try:
                    timeDelta=datetime.strptime(self.text,'%H:%M')-datetime.strptime(self.contentTmp,'%H:%M')
                    #self.parent.ChangeTime(timeDelta)
                    self.parent.TimeChanged(timeDelta)
                    #self.parent.ChangeDuration(timeDelta)
                except ValueError:
                    pass

    def insert_text(self,substring,from_undo=False):
        if re.match('[0-9]',substring) or substring==":":
            return super(TimeInput,self).insert_text(substring,from_undo)
        elif substring=="：":
            return super(TimeInput,self).insert_text(":",from_undo)

class DurationInput(TabTextInput):
    contentTmp=None
    def __init__(self,**kwargs):
        super(DurationInput,self).__init__(**kwargs)
        self.input_type="number"
        def laterInit(time=None):
            self.focus_previous=self.parent.time
            self.focus_next=self.parent.job
        Clock.schedule_once(laterInit,0.2)

    def insert_text(self,substring,from_undo=False):
        if re.match('[0-9]',substring) or substring==".":
            return super(DurationInput,self).insert_text(substring,from_undo)

    def on_focus(self,instance,value):
        if value==True:
            self.hint_text=self.AutoDuration()
            if self.text=='':
                self.contentTmp='0'
            else:
                self.contentTmp=self.text
        else:
            if self.text=='' and self.hint_text!='Duration':
                self.text=self.hint_text
            if self.contentTmp!=self.text:
                try:
                    delta=float(self.text)-float(self.contentTmp)
                    timeDelta=timedelta(seconds=delta*3600)
                    #self.parent.ChangeTime(timeDelta)
                    self.parent.TimeChanged(timeDelta)
                except ValueError:
                    pass
            if self.text:
                self.text='%.2f'%float(self.text)

    def AutoDuration(self):
        return 'Duration'

class JobInput(TabTextInput):
    def __init__(self,**kwargs):
        super(JobInput,self).__init__(**kwargs)
        self.keyboard_on_key_down=self.OnKeyDown
        def laterInit(time=None):
            focus_previous=self.parent.duration
            if self.parent.parent.parent.recordIndex[-1]==self.parent:
                self.focus_next==None
            else:
                self.focus_next=self.parent.parent.parent.recordIndex[int(self.parent.id)+1].time
        Clock.schedule_once(laterInit,0.2)

    def OnKeyDown(self,keyboard,keycode=None,text=None,modifier=None,**kwargs):
        if keycode[0]==9 and modifier==[] and self.parent==self.parent.parent.parent.recordIndex[-1]:
            self.parent.AddNewLog()
            def focusNext(time=None):
                self.focus_next.focus=True
            Clock.schedule_once(focusNext,0.2)
        else:
            super(JobInput,self).OnKeyDown(keyboard,keycode,text,modifier,**kwargs)
        return True
'''
class DateInput(TabTextInput):
    contentTmp=None

    def __init__(self,**kwargs):
        super(DateInput,self).__init__(**kwargs)

    def on_focus(self,instance,value):
        if value==True:
            self.contentTmp=self.text
        else:
            if self.contentTmp!=self.text:
                date1=self.parent.GetDate()
                self.parent.parent.OnDateChanged(datetime.strptime(date1,'%Y%m%d'))
'''
class YearInput(TextInput):
    def insert_text(self,substring,from_undo=False):
        if substring=='\t':
            if len(self.text)!=4 or int(self.text)>date.today().year or int(self.text)<0:
                pass
            else:
                self.focus_next.focus=True
                #something to do here
        elif re.match('[0-9]',substring):
            return super(YearInput,self).insert_text(substring,from_undo)
    def on_text_validate(self):
        self.focus_next.focus=True

class MonthInput(TextInput):
    def insert_text(self,substring,from_undo=False):
        if substring=='\t':
            if int(self.text)>12 or int(self.text)<1:
                pass
            else:
                self.ConfirmDate(self)
        elif re.match('[0-9]',substring):
            return super(MonthInput,self).insert_text(substring,from_undo)

    def on_text_validate(self):
        self.ConfirmDate(self)

    def ConfirmDate(self,instance):
        pass

class StartTimeInput(TextInput):
    choosed=True
    def insert_text(self,substring,from_undo=False):
        if substring=='\t':
            self.SetStartTime(self)
        elif re.match('[0-9]',substring) or re.match('-',substring):
            return super(StartTimeInput,self).insert_text(substring,from_undo)
    def on_text_validate(self):
        self.SetStartTime(self)
    def SetStartTime(self,instance):
        pass
    def on_focus(self,instance,value):
        if value==True:
            self.choosed=True

class EndTimeInput(TextInput):
    def insert_text(self,substring,from_undo=False):
        if substring=='\t':
            self.SetEndTime(self)
        elif re.match('[0-9]',substring) or re.match('-',substring):
            return super(EndTimeInput,self).insert_text(substring,from_undo)
    def on_focus(self,instance,value):
        if value==True:
            if not re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}',self.focus_previous.text):
                self.focus_previous.focus=True
    def on_text_validate(self):
        self.SetEndTime(self)
    def SetEndTime(self,instance):
        pass
