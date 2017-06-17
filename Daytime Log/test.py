
from kivy.app import App
from kivy.uix.widget import Widget

class test(Widget):
    pass

class testApp(App):
    def build(self):
        return test()
if __name__=='__main__':
    testApp().run()

'''
class c:
    __val1=0
    def __init__(self,x,y):
        self.val2=x
        c.__val1=y
    def getVal1(self):
        return self.__val1
'''
'''
import kivy
kivy.require('1.0.8')

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.properties import ObjectProperty


class MyKeyboardListener(Widget):
    test=ObjectProperty(None)
    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self.test, 'text')
        self.test=self._keyboard.on_key_down
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        #self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        #self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)

        if keycode==(9, 'tab') and modifiers==['shift']:
            print("fuck")
        else:
            #Window.Keyboard.on_key_down()
            self.test(keycode, text, modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        #if keycode[1] == 'escape':
        #    keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

class testApp(App):
    def build(self):
        return MyKeyboardListener()

if __name__ == '__main__':
    testApp().run()
'''
