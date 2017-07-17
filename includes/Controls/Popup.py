from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.core.window import Window
import re
import kivy.metrics
#from kivy.properties import ObjectProperty


#Builder.load_file('includes/Controls/Timer.kv')
Builder.load_file('includes/Controls/Popup.kv')

class MyPopup(RelativeLayout):
    shortCut={}
    def __init__(self,tips,btns,**kwargs):
        super(MyPopup,self).__init__(**kwargs)
        self.tips.text=tips
        self.keyboard=Window.request_keyboard(self.CloseShortCut,self,input_type='text')
        #self.keyboard.on_key_down=self.ShortCut
        self.keyboard.bind(on_key_down=self.ShortCut)
        self.shortCut={}
        for btn in btns:
            #big or normal
            if re.search('big',btn['type']):
                btnTmp=BigButton(text=btn['text'])
            else:
                btnTmp=PureButton(text=btn['text'])
            #left or right
            if re.search('left',btn['type']):
                self.operationsLeft.add_widget(btnTmp)
            else:
                self.operations.add_widget(btnTmp)
            if btn['func']=='' or btn['func']==None:
                func=self.Close
            else:
                func=btn['func']
            btnTmp.bind(on_press=func)
            if ('shortCut' in btn.keys()) and btn['shortCut']!=0:
                btn['shortCut']
                self.shortCut[btn['shortCut']]=func
            btnTmp.texture_update([0,0])
            btnTmp.width=kivy.metrics.dp(60) if btnTmp.texture_size[0]+kivy.metrics.dp(24)<kivy.metrics.dp(60) else btnTmp.texture_size[0]+kivy.metrics.dp(24)

    def CloseShortCut(self,*args):
        self.keyboard.unbind(on_key_down=self.ShortCut)
        self.keyboard=None

    def ShortCut(self,keyboard,keycode=None,text=None,modifiers=None):
        if keycode[1]=='q' and modifiers=='meta':
            Window.close()
        if keycode[1] in self.shortCut.keys():
            self.shortCut[keycode[1]]()

    def Close(self,instance=None):
        #Window.release_keyboard(self.keyboard)
        self.keyboard.release()
        self.parent.RequestKeyboard()
        self.parent.requestLeaving=0
        self.parent.remove_widget(self)

class PureButton(Button):
    pass

class BigButton(Button):
    pass
