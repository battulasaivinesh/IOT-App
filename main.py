from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.base        import runTouchApp
from kivy.config      import Config
from kivy.core.window import Window
from kivy.lang        import Builder
from kivy.utils       import platform
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import SlideTransition

if platform not in ('android', 'ios'):
  Config.set('graphics', 'resizable', '0')
  Window.size = (375, 667)


class MenuScreen(Screen):

	def one(self):
		self.parent.transition = SlideTransition(direction='left')
		self.parent.current='reactor1'

	def two(self):
		self.parent.transition = SlideTransition(direction='left')
		self.parent.current='reactor2'

	def three(self):
		self.parent.transition = SlideTransition(direction='left')
		self.parent.current='reactor3'


class BoxButton(ButtonBehavior,BoxLayout):
	pass

class ReactorScreen1(Screen):

	def back(self):
		self.parent.transition = SlideTransition(direction='right')
		self.parent.current = 'main'

class ReactorScreen2(Screen):

	def back(self):
		self.parent.transition = SlideTransition(direction='right')
		self.parent.current = 'main'

class ReactorScreen3(Screen):

	def back(self):
		self.parent.transition = SlideTransition(direction='right')
		self.parent.current = 'main'

		

	

class ScreenManagement(ScreenManager):
	pass     

presentation = Builder.load_file("MyApp.kv")

class MyApp(App):
    def build(self):
        return presentation


if __name__ == '__main__':
    MyApp().run()