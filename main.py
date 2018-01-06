from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.base        import runTouchApp
from kivy.config      import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang        import Builder
from kivy.utils       import platform
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import SlideTransition
import requests
import json
from threading import Thread


# Sets the screen size on computer for development
if platform not in ('android', 'ios'):
  Config.set('graphics', 'resizable', '0')
  Window.size = (375, 667)

# Retrives data from given url running on diffrent thread
def get_data():
    global data
    global temp
    global netstatusaf
    global netstatus_color
    t = 0
    while True:
        data = []
        try:
            Data = requests.get('http://54.88.51.15/get/')
            netstatus_color = [0, 0, 1, 0.6]
            netstatus = 'Online'
        except:
            netstatus = 'No Internet Connection'
            netstatus_color = [1,0,0,0.6]

# Internet Status Bar
class NetLab(BoxLayout):
	def __init__(self,**kwargs):
		super(NetLab, self).__init__(**kwargs)




# Main Screen contaning a grid of reactors
class MenuScreen(Screen):

	######  Transaction functions for on click event for each reactor ########

	# Reactor 1
	def one(self):
		self.parent.transition = SlideTransition(direction='left')
		self.parent.current='reactor1'

	# Reactor 2
	def two(self):
		self.parent.transition = SlideTransition(direction='left')
		self.parent.current='reactor2'

	# Reactor 3
	def three(self):
		self.parent.transition = SlideTransition(direction='left')
		self.parent.current='reactor3'



# Adding button behaviour to each reactor
class BoxButton(ButtonBehavior,BoxLayout):
	pass



############    Main Reactor Screen    ##############

### All the reactor screens are children of this widget

class ReactorScreen(Screen):
	def back(self):
		self.parent.transition = SlideTransition(direction='right')
		self.parent.current = 'main'





#############      Children Screen for each reactor  ##############


# Reactor 1
class ReactorScreen1(ReactorScreen):
	def __init__(self,**kwargs):
		super(ReactorScreen1, self).__init__(**kwargs)
		self.name = "reactor1"
		Clock.schedule_once(self._finish_init)
		Clock.schedule_interval(self.get_value, 1)

	# To initialize different sections
	def _finish_init(self, dt):
		self.ids.label.text = "ONE"

	def get_value(self,dt):
		self.ids.net.netstattxt = netstatus
		self.ids.net.netstatuscolor = netstatus_color

# Reactor 2
class ReactorScreen2(ReactorScreen):
	def __init__(self,**kwargs):
		super(ReactorScreen2, self).__init__(**kwargs)
		self.name = "reactor2"
	 	Clock.schedule_once(self._finish_init)
		Clock.schedule_interval(self.get_value, 1)

	# To initialize different sections
	def _finish_init(self, dt):
		self.ids.label.text = "TWO"

	def get_value(self,dt):
		self.ids.net.netstattxt = netstatus
		self.ids.net.netstatuscolor = netstatus_color


# Reactor 3
class ReactorScreen3(ReactorScreen):
	def __init__(self,**kwargs):
		super(ReactorScreen3, self).__init__(**kwargs)
		self.name = "reactor3"
		Clock.schedule_once(self._finish_init)
		Clock.schedule_interval(self.get_value, 1)

	# To initialize different sections
	def _finish_init(self, dt):
		self.ids.label.text = "THREE"

	def get_value(self,dt):
		self.ids.net.netstattxt = netstatus		
		self.ids.net.netstatuscolor = netstatus_color

		





### Main Screen Manager  ###

class ScreenManagement(ScreenManager):
	pass     

presentation = Builder.load_file("MyApp.kv")

class MyApp(App):
    def build(self):
        return presentation


if __name__ == '__main__':
    netstatus = 'Waiting for Network...'
    netstatus_color = [1,0.49,0.31,0.6]
    get_level_thread = Thread(target=get_data)
    get_level_thread.daemon = True
    get_level_thread.start()
    MyApp().run()