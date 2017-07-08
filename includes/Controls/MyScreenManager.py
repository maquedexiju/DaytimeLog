from kivy.uix.screenmanager import ScreenManager

class MyScreenManager(ScreenManager):
    def __init__(self,**kwargs):
        super(MyScreenManager,self).__init__(**kwargs)

    def OnLeaving(self,*args):
        return self.children[0].OnLeaving()