from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from includes.DB import *

Builder.load_file('includes/Controls/AdaptView.kv')

class AdaptView(Screen):
    DB=None
    BASEPATH=None
    SM=None
    WINDOW=None
    def __init__(self,screenName,sysArgs,**kwargs):
        super(AdaptView,self).__init__(name=screenName,**kwargs)
        self.DB=sysArgs['DB']
        self.BASEPATH=sysArgs['BASEPATH']
        self.FILEPATH=sysArgs['FILEPATH']
        self.SM=sysArgs['SM']
        self.WINDOW=sysArgs['WINDOW']

    def resize(self):
        #seems that using window.center will cause some problems
        self.height=self.WINDOW.height
        self.center_x=self.WINDOW.width/2
        self.center_y=self.WINDOW.height/2

    def on_enter(self):
        self.resize()
