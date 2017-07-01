from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from includes.Controls.Popup import MyPopup

class MyScreenManager(ScreenManager):
    requestLeaving=0
    def __init__(self,**kwargs):
        super(MyScreenManager,self).__init__(**kwargs)
        #self.RequestKeyboard()

    def RequestKeyboard(self):
        self.keyboard=Window.request_keyboard(self.CloseShortCut,self,input_type='text')
        self.keyboard.bind(on_key_down=self.ShortCut)

    def ShortCut(self,keyboard,keycode,text,modifiers):
        print('sm kb')
        if modifiers==['meta'] and keycode[1]=='s':
            self.Save()
        elif modifiers==['meta'] and keycode[1]=='e':
            self.Export()

    def CloseShortCut(self,*args):
        self.keyboard.unbind(on_key_down=self.ShortCut)
        self.keyboard=None

    def Save(self,instance=None):
        if self.current=='todayView':
            self.children[0].SaveLog()
        elif self.current=='historyView':
            self.children[0].SaveLog()

    def Export(self,instance=None):
        self.children[0].ExportLog()

    def SaveAndLeave(self,instance=None):
        self.Save()
        Window.close()

    def Leave(self,instance=None):
        Window.close()

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
            popup=MyPopup([{'type':'right-big','text':'Quit','func':self.SaveAndLeave,'shortCut':'q'},
                           {'type':'right-pure','text':'Cancel','func':'','shortCut':'c'}])
            self.children[0].add_widget(popup)
            self.requestLeaving=1
            return True
        else:
            return False
