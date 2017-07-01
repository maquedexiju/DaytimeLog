from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import re
from datetime import *
from string import *

class TabTextInput(TextInput):
    __last=None
    pre=None
    nex=None
    id1=0
    def __init__(self,**kwargs):
        super(TabTextInput,self).__init__(**kwargs)
        self.font_name="includes/fzltqh.ttf"
        self.multiline=False
        self.font_size="12sp"
        self.text_size=self.size
        self.valign="middle"
        #self.keybindings='emacs'
        self.keyboard=Window.request_keyboard(self.callback,self,input_type="text")
        self.keyboard_on_key_down=self.OnKeyDown
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

    def OnKeyDown(self,keyboard,keycode=None,text=None,modifier=None,**kwargs):
        if keycode[1]=='tab':
            if modifier==['shift']:
                try:
                    #self.focus=False
                    self.pre.focus=True
                except AttributeError:
                    pass
            else:
                try:
                    #self.focus=False
                    self.nex.focus=True
                except AttributeError:
                    pass
        elif keycode[1]=='escape':
            pass
        else:
            super(TabTextInput,self).keyboard_on_key_down(keyboard,keycode,text,modifier,**kwargs)

        return True

    def callback(self):
        Window.release_keyboard(self.keyboard)

    def Delete(self):
        try:
            self.pre.nex=self.nex
        except AttributeError:
            pass
        try:
            self.nex.pre=self.pre
        except AttributeError:
            TabTextInput.__last=self.pre

    def GetLast():
        return TabTextInput.__last

class TimeInput(TabTextInput):
    contentTmp=None
    def __init__(self,**kwargs):
        super(TimeInput,self).__init__(**kwargs)
        self.input_type="number"
    def on_focus(self,instance,value):
        if value==True:
            self.contentTmp=self.text
        else:
            if self.contentTmp!=self.text:
                try:
                    #timeDelta=datetime.strptime(self.text,'%H:%M')-datetime.strptime(self.contentTmp,'%H:%M')
                    #self.parent.ChangeTime(timeDelta)
                    self.parent.ChangeTime()
                    self.parent.ChangeDuration(timeDelta)
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
    def insert_text(self,substring,from_undo=False):
        if re.match('[0-9]',substring) or substring==".":
            return super(DurationInput,self).insert_text(substring,from_undo)
    def on_focus(self,instance,value):
        if value==True:
            self.contentTmp=self.text
        else:
            if self.contentTmp!=self.text:
                try:
                    #delta=float(self.text)-float(self.contentTmp)
                    #timeDelta=timedelta(seconds=delta*3600)
                    #self.parent.ChangeTime(timeDelta)
                    self.parent.ChangeTime()
                except ValueError:
                    pass

class JobInput(TabTextInput):
    def __init__(self,**kwargs):
        super(JobInput,self).__init__(**kwargs)
        self.keyboard_on_key_down=self.OnKeyDown

    def OnKeyDown(self,keyboard,keycode=None,text=None,modifier=None,**kwargs):
        if keycode[0]==9 and modifier==[] and self==TabTextInput.GetLast():
            self.parent.AddNewLog()
            self.nex.focus=True
        else:
            super(JobInput,self).OnKeyDown(keyboard,keycode,text,modifier,**kwargs)
        return True

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
