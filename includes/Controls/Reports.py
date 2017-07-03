from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
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

Builder.load_file('includes/Controls/Reports.kv')
#Builder.load_file('includes/Controls/ImageButton.kv')
class Reports(ScrollView):
    indexTags=[]
    def DrawReports(self,data):
        for (tag,info) in data.items():
            report=ReportOneLine(tag,info,self.width)
            self.reports.add_widget(report)
            self.indexTags.append(report)
        self.UpdateHeight()

    def UpdateHeight(self):
        height=0
        for child in self.reports.children[:]:
            height+=child.height
        self.reports.height=height

    def Clear(self):
        self.reports.clear_widgets()
        self.indexTags=[]


class ReportOneLine(StackLayout):
    indexJobs=None
    def __init__(self,id=None,info=None,width=None,**kwargs):
        super(ReportOneLine,self).__init__(**kwargs)
        self.width=width
        self.id=id
        self.tag.text=id
        self.time.text='%.2f'%info['duration']+'H'
        self.indexJobs=[]
        self.btn.bind(on_press=self.Expand)
        for job,duration in info['job'].items():
            oneJob=Jobs(job,duration,self.width)
            #self.add_widget(oneJob)
            self.indexJobs.append(oneJob)
        self.UpdateHeight()

    def Expand(self,instance):
        for job in self.indexJobs[:]:
            self.add_widget(job)
        self.UpdateHeight()
        self.parent.parent.UpdateHeight()
        instance.funbind('on_press',self.Expand)
        instance.bind(on_press=self.Close)

    def Close(self,instance):
        for job in self.indexJobs[:]:
            self.remove_widget(job)
        self.UpdateHeight()
        self.parent.parent.UpdateHeight()
        instance.funbind('on_press',self.Close)
        instance.bind(on_press=self.Expand)

    def UpdateHeight(self):
        height=0
        for child in self.children[:]:
            height+=child.height
        self.height=height

class Jobs(RelativeLayout):
    #jobContent=ObjectProperty(None)
    def __init__(self,job=None,duration=None,width=None,**kwargs):
        super(Jobs,self).__init__(**kwargs)
        self.width=width
        self.jobContent.text=job
        self.jobContent.texture_update([0,0])
        self.height=self.jobContent.height+kivy.metrics.dp(20)
        self.time.text='%.2f'%duration+'H'
'''
class MyLabel(Label):
    def texture_update(self,size):
        a=super(MyLabel,self).texture_update(size)
        return self.height
'''
