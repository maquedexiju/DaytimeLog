from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.core.window import Window
from includes.Controls.Popup import MyPopup
from includes.DB import *

Builder.load_file('includes/Controls/AdaptView.kv')

class AdaptView(Screen):
    DB=None
    BASEPATH=None
    SM=None
    WINDOW=None
    requestLeaving=0
    def __init__(self,screenName,sysArgs,**kwargs):
        super(AdaptView,self).__init__(name=screenName,**kwargs)
        self.DB=sysArgs['DB']
        self.BASEPATH=sysArgs['BASEPATH']
        self.FILEPATH=sysArgs['FILEPATH']
        self.SM=sysArgs['SM']
        self.WINDOW=sysArgs['WINDOW']
        self.requestLeaving=0
        #self.RequestKeyboard()

    def resize(self):
        #seems that using window.center will cause some problems
        self.height=self.WINDOW.height
        self.center_x=self.WINDOW.width/2
        self.center_y=self.WINDOW.height/2

    def on_enter(self):
        self.resize()
        self.RequestKeyboard()

    def on_leave(self):
        self.keyboard.unbind(on_key_down=self.ShortCut)
        self.keyboard=None

    def RequestKeyboard(self):
        self.keyboard=Window.request_keyboard(self.CloseShortCut,self,input_type='text')
        self.keyboard.bind(on_key_down=self.ShortCut)

    def ShortCut(self,keyboard,keycode,text,modifiers):
        if modifiers==['meta'] and keycode[1]=='s':
            self.Save()
        elif modifiers==['meta'] and keycode[1]=='e':
            self.Export()

    def CloseShortCut(self,*args):
        '''
        self.keyboard.unbind(on_key_down=self.ShortCut)
        self.keyboard=None
        '''

    def SaveAndLeave(self,instance=None):
        self.SaveLog()
        Window.close()

    def Save(self,instance=None):
        self.SaveLog()

    def SaveLog(self):
        pass

    def Export(self,instance=None):
        self.ExportLog()

    def ExportLog(self):
        pass
        
    def OnLeaving(self,*args):
        '''
        if self.requestLeaving==0:
            popup=MyPopup([{'type':'left-pure','text':'Don\'t Save','func':self.Leave,'shortCut':'d'},\
                           {'type':'right-big','text':'Save','func':self.SaveAndLeave,'shortCut':'s'},
                           {'type':'right-pure','text':'Cancel','func':'','shortCut':'c'}])
            self.children[0].add_widget(popup)
            self.requestLeaving=1
            return True
        else:
            return False
        '''
        if self.requestLeaving==0:
            popup=MyPopup('Do you want to leave now?',[{'type':'right-big','text':'Quit','func':self.SaveAndLeave,'shortCut':'q'},
                           {'type':'right-pure','text':'Cancel','func':'','shortCut':'c'}])
            self.add_widget(popup)
            self.requestLeaving=1
            return True
        else:
            return False
