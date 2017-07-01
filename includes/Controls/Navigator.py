from kivy.lang.builder import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock

Builder.load_file('includes/Controls/Navigator.kv')
Builder.load_file('includes/Controls/ImageButton.kv')

class Navigator(RelativeLayout):
    title=ObjectProperty(None)
    today=ObjectProperty(None)
    history=ObjectProperty(None)
    report=ObjectProperty(None)
    underline=ObjectProperty(None)
    def __init__(self,**kwargs):
        super(Navigator,self).__init__(**kwargs)
        self.index=['Today','History','Report']

    def Init(self,number):
        self.title.text=self.index[int(number)]
        eval('self.tab'+str(number)).state='down'
        for i in range(0,3):
            eval('self.title'+str(i)).color=[0,0,0,1]
        eval('self.title'+str(number)).color=[0.97,0.36,0.29,1]

    def ShowView(self,view):
        self.parent.SM.current=view
