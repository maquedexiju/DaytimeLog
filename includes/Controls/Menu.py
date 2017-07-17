from kivy.lang.builder import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.button import Button
import kivy.metrics
from kivy.logger import Logger

Builder.load_file('includes/Controls/Menu.kv')
Builder.load_file('includes/Controls/ImageButton.kv')

class Menu(RelativeLayout):
    menuIndex=[]
    more=ObjectProperty(None)
    poped=False
    def Init(self,**kwargs):
        i=0
        Logger.info('MENU: init, parent\' width %d '%self.parent.width)
        for key in kwargs:
            i+=1
            t=eval(key)(kwargs[key])
            t.pos=-kivy.metrics.dp(114)+self.parent.width*3,-kivy.metrics.dp(36)*i
            self.add_widget(t)
            self.menuIndex.append(t)
        self.mask.pos=self.to_local(0+self.parent.width*3,0)
        self.more.bind(on_release=self.PopUp)
        '''
        def laterInit(time=None):
            self.mask.pos=self.to_local(0+self.parent.width*3,0)
            self.more.bind(on_press=self.PopUp)
        Clock.schedule_once(laterInit,1)
        '''

    def PopUp(self,btn):
        if self.poped==False:
            Logger.info('MENU: popup')
            for menuLine in self.menuIndex:
                menuLine.x-=self.parent.width*3
            self.poped=True
            self.mask.x-=self.parent.width*3
            #self.bind(on_touch_down=self.Close)
        else :
            Logger.info('MENU: close')
            for menuLine in self.menuIndex:
                menuLine.x+=self.parent.width*3
            self.poped=False
            self.mask.x+=self.parent.width*3
    #def Close(self,instance,event):
    def Close(self):
        for menuLine in self.menuIndex:
            menuLine.x+=self.parent.width*3
        self.mask.x+=self.parent.width*3
        self.poped=False
        #self.funbind('on_touch_down',self.Close)

    def EnterEdit(self):
        self.more.x+=self.parent.width*3
        self.done.x-=self.parent.width*3

    def LeaveEdit(self):
        self.more.x-=self.parent.width*3
        self.done.x+=self.parent.width*3
        self.parent.LeaveEdit()

class MenuLine(RelativeLayout):
    icon=ObjectProperty(None)
    title=ObjectProperty(None)
    operation=ObjectProperty(None)
    def __init__(self,icon,title,operation,**kwargs):
        self.id=title
        def laterInit(time=None):
            self.icon.background_normal=icon
            self.title.text=title
            self.operation.bind(on_press=operation)
            self.operation.bind(on_release=self.Close)
        Clock.schedule_once(laterInit,0.5)
        super(MenuLine,self).__init__(**kwargs)
    def Close(self,instance):
        self.parent.Close()

class Save(MenuLine):
    iconPath='includes/icons/Save.png'
    title="Save"
    def __init__(self,operation,**kwargs):
        super(Save,self).__init__(self.iconPath,self.title,operation,**kwargs)

class Export(MenuLine):
    iconPath='includes/icons/Export.png'
    title="Export"
    def __init__(self,operation,**kwargs):
        super(Export,self).__init__(self.iconPath,self.title,operation,**kwargs)

class Edit(MenuLine):
    iconPath='includes/icons/Edit.png'
    title="Edit"
    def __init__(self,operation,**kwargs):
        super(Edit,self).__init__(self.iconPath,self.title,operation,**kwargs)
