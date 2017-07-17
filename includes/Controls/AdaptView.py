from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.core.window import Window
from includes.Controls.Popup import MyPopup
from includes.DB import *
from kivy.logger import Logger
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import markdown

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
        self.width=sysArgs['WIDTH']
        self.height=sysArgs['HEIGHT']
        Logger.info('%s: width %d'%(self.name,self.width))
        self.DESKTOP=sysArgs['DESKTOP']
        self.requestLeaving=0
        #self.RequestKeyboard()

    def resize(self):
        #seems that using window.center will cause some problems
        self.height=self.WINDOW.height
        self.width=self.WINDOW.width
        self.size=self.WINDOW.size
        self.center_x=self.WINDOW.width/2
        self.center_y=self.WINDOW.height/2

    def on_enter(self):
        self.resize()
        if self.DESKTOP:
            self.RequestKeyboard()

    def on_leave(self):
        if self.DESKTOP:
            self.keyboard.unbind(on_key_down=self.ShortCut)
            self.keyboard=None

    def RequestKeyboard(self):
        Logger.info('KEYBOARD: %s requests keyboard'%self.name)
        self.keyboard=Window.request_keyboard(self.CloseShortCut,self,input_type='text')
        self.widget=None
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
    
    #send record/logs via email
    def SendviaEmail(self, receiver, content, format):

        #set e-mail account
        mail_host = 'smtp.tom.com'
        mail_port = 25
        mail_account = 'daytimelog@tom.com'
        mail_password = 'com.xiaotian'

        sender = 'daytimelog@tom.com'
        receivers = 'xtmatriment@126.com'

        #for 126
        '''
        mail_host = 'smtp.126.com'
        mail_port = 25
        mail_account = 'daytimelog@126.com'
        mail_password = '123asd'

        sender = u'daytimelog<daytimelog@126.com>'
        receivers = u'<xtmatriment@126.com>'
        '''

        #set content
        if format == 'csv':
            sheet = ''
            print(format)
            with open(content,'r') as file:
                title = file.readline()[:-1].split(',')
                sheet = "|" + "|".join(title) + "|\n|"
                for col in title:
                    sheet += "---|"
                sheet +='\n'
                for line in file.readlines():
                    content = "|" + "|".join(line[:-1].split(',')) + "|\n"
                    sheet += content
                    print(content)
            
            html = markdown.markdown('Hope you never waste time! ')
            html += markdown.markdown(sheet, extensions=['markdown.extensions.tables'])
        
        #message = MIMEText(html, 'html', 'utf-8' )
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receivers
        message['Subject'] = Header(u'[DaytimeLog]Record Your Life', 'utf-8')
        message.attach(MIMEText(html, 'html', 'utf-8' ))
        

        try:
            #tom mail
            emailService = smtplib.SMTP(mail_host,mail_port)
            emailService.ehlo()
            emailService.login(mail_account, mail_password)
            emailService.sendmail(sender, receivers, message.as_string())
            emailService.quit()

            #126 mail
            '''
            emailService = smtplib.SMTP(mail_host, mail_port)
            emailService.ehlo()
            emailService.login(mail_account, mail_password)
            emailService.sendmail(sender, receivers, message.as_string())
            emailService.quit()
            '''

            Logger.info('EMAIL: succeed')
        except Exception as e:
            #Logger.error("EMAIL: failed",exc_info=True,stack_info=True)
            Logger.error("EMAIL: %s"%repr(e))
        
        #except:
        #    Logger.error('EMAIL: failed')