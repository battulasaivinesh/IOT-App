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
from kivy.garden.graph import MeshLinePlot, SmoothLinePlot
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, ListProperty
import socket
import time
import paho.mqtt.client as paho
from kivy.utils import get_color_from_hex

broker='io.adafruit.com'

global levels_temp
global levels_humidity
global number_of_reactors
global temp_t
global humidity_t

number_of_reactors = 4

temp_t = []
humidity_t = []
levels_temp = []
levels_humidity = []

for j in range(0,number_of_reactors):
    for i in range(0,25):
        temp_t.append(0)
        humidity_t.append(0)
    levels_temp.append(temp_t)
    levels_humidity.append(humidity_t)
    temp_t = []
    humidity_t = []


def on_message(client, userdata, message):
    global dataRecv
    time.sleep(0.5)
    dataRecv = str(message.payload.decode("utf-8"))

def get_data():
    global s
    global data
    global temp
    global netstatus
    global netstatus_color
    global port
    global dataRecv
    global levels_temp
    global levels_humidity
   
    t = 0
    time.sleep(0.2)
    client= paho.Client("client-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
    ######Bind function to callback
    client.on_message=on_message
    #####
    client.username_pw_set("Rahul_1408","650adecd1c964f988aaffbe35fe11766")
    # print("connecting to broker ",broker)
    client.connect(broker)#connect
    client.loop_start() #start loop to process received messages
    # print("subscribing ")
    client.subscribe("Rahul_1408/feeds/sensdat")#subscribe
        
        #c, addr = s.accept()
     
    while True:
        data = []
        try:
            arr = json.loads(dataRecv)
            # print arr
            for a in arr:
                data.append(float(a))
            temp = data
            # print temp
            for i in range(0,number_of_reactors):
                levels_temp[i].append(temp[i])
                if len(levels_temp[i]) > 26:
                    levels_temp[i].pop(0)
            
            # print levels_temp;
            
            # print levels
            netstatus_color = get_color_from_hex('#009B72')
            netstatus = 'Online'
            
            # print levels_temp
        except:

            netstatus = 'No Internet Connection'
            netstatus_color =  get_color_from_hex('#AF2A3C')
            temp = [0,0,0,0]

            

        time.sleep(1)


# Sets the screen size on computer for development
if platform not in ('android', 'ios'):
    Config.set('graphics', 'resizable', '0')
    Window.size = (375, 667)

# if platform not in ('android', 'ios'):
#   Config.set('graphics', 'resizable', '0')
#   Window.size = (768, 1024)


# Internet Status Bar
class NetLab(BoxLayout):
    def __init__(self,**kwargs):
        super(NetLab, self).__init__(**kwargs)

class CanvasCustom(BoxLayout):
    temp_value = NumericProperty(None)
    temp_angle = NumericProperty(None)
    temp_strval = StringProperty(None)
    humidity_value = NumericProperty(None)
    humidity_angle = NumericProperty(None)
    humidity_strval = StringProperty(None)
    sen_color_humidity = ListProperty([])
    main_header_color = ListProperty([])
    sen_color_temp = ListProperty([])
    title = StringProperty(None)

    def __init__(self,**kwargs):
        super(CanvasCustom, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1,0.5)



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

    def four(self):
        self.parent.transition = SlideTransition(direction='left')
        self.parent.current='reactor4'



# Adding button behaviour to each reactor
class BoxButton(ButtonBehavior,BoxLayout):
    pass



############    Main Reactor Screen    ##############

### All the reactor screens are children of this widget

class ReactorScreen(Screen):
    def back(self):
        self.parent.transition = SlideTransition(direction='right')
        self.parent.current = 'main'



#############      Children Screen for each reactor  ############swswwWd##


# Reactor 1
class ReactorScreen1(ReactorScreen):
    def __init__(self,**kwargs):
        super(ReactorScreen1, self).__init__(**kwargs)
        self.name = "reactor1"
        Clock.schedule_once(self._finish_init)
        Clock.schedule_interval(self.get_value, 1)
        self.plot_temp = SmoothLinePlot(color = get_color_from_hex('#3DA3D1'))
        self.plot_humidity = SmoothLinePlot(color = get_color_from_hex('#3DA3D1'))


    def _finish_init(self, dt): 
        pass
        # print "added" 
        # if Window.size[0] > 500:
        #     self.ids.humid_meter.size_hint = (0.5,None)
        #     self.ids.temp_meter.size_hint = (0.5,None)
        #     self.ids.temp_graph_cover.size_hint = (0.5,None)
        #     self.ids.humidity_graph_cover.size_hint = (0.5,None)
        #     # print "yes"
        # else:
        #     self.ids.humid_meter.size_hint = (1,None)
        #     self.ids.temp_meter.size_hint = (1,None)
        #     self.ids.temp_graph_cover.size_hint = (1,None)
        #     self.ids.humidity_graph_cover.size_hint= (1,None)
        #     self.ids.reactor_main_layout.spacing = 30


    
    def get_value(self,dt):
        self.main_header_color = netstatus_color
        self.ids.graph_temp.add_plot(self.plot_temp);
        self.ids.graph_humidity.add_plot(self.plot_humidity);
        self.ids.net.netstattxt = netstatus
        self.ids.net.netstatuscolor = netstatus_color
        self.plot_temp.points = [(i-25, j) for i, j in enumerate(levels_temp[0])]
        self.plot_humidity.points = [(i-25, j) for i, j in enumerate(levels_humidity[0])]
        # print self.plot.points
        self.temp_value = temp[0]
        self.humidity_value = 0
        self.temp_angle = 3.6*self.temp_value
        self.temp_strval = str(round(self.temp_value,2))+ u'\u00b0' + 'C'
        self.humidity_strval = str(round(self.humidity_value,2))+ "%"
        self.humidity_angle = 3.6*self.humidity_value

        if self.temp_value > 50:
            self.sen_color_temp = get_color_from_hex('#C73C4C')

        elif self.temp_value < 20:
            self.sen_color_temp = get_color_from_hex('#3DA3D1')

        else:
            self.sen_color_temp = get_color_from_hex('#3DA3D1')

        if self.humidity_value > 50:
            self.sen_color_humidity = get_color_from_hex('#C73C4C')

        elif self.humidity_value < 20:
            self.sen_color_humidity = get_color_from_hex('#3DA3D1')

        else:
            self.sen_color_humidity = get_color_from_hex('#3DA3D1')





# Reactor 2
class ReactorScreen2(ReactorScreen):
    def __init__(self,**kwargs):
        super(ReactorScreen2, self).__init__(**kwargs)
        self.name = "reactor2"
        Clock.schedule_once(self._finish_init)
        Clock.schedule_interval(self.get_value, 1)
        self.plot_temp = SmoothLinePlot(color = get_color_from_hex('#3DA3D1'))
        self.plot_humidity = SmoothLinePlot(color = get_color_from_hex('#3DA3D1'))


    def _finish_init(self, dt): 
        
        self.ids.main_label.text = "SENSOR 2"
        # print "added" 
        # if Window.size[0] > 500:
        #     self.ids.humid_meter.size_hint = (0.5,None)
        #     self.ids.temp_meter.size_hint = (0.5,None)
        #     self.ids.temp_graph_cover.size_hint = (0.5,None)
        #     self.ids.humidity_graph_cover.size_hint = (0.5,None)
        #     # print "yes"
        # else:
        #     self.ids.humid_meter.size_hint = (1,None)
        #     self.ids.temp_meter.size_hint = (1,None)
        #     self.ids.temp_graph_cover.size_hint = (1,None)
        #     self.ids.humidity_graph_cover.size_hint= (1,None)
        #     self.ids.reactor_main_layout.spacing = 30


    
    def get_value(self,dt):
        self.main_header_color = netstatus_color
        self.ids.graph_temp.add_plot(self.plot_temp);
        self.ids.graph_humidity.add_plot(self.plot_humidity);
        self.ids.net.netstattxt = netstatus
        self.ids.net.netstatuscolor = netstatus_color
        self.plot_temp.points = [(i-25, j) for i, j in enumerate(levels_temp[1])]
        self.plot_humidity.points = [(i-25, j) for i, j in enumerate(levels_humidity[1])]
        # print self.plot.points
        self.temp_value = temp[1]
        self.humidity_value = 0
        self.temp_angle = 3.6*self.temp_value
        self.temp_strval = str(round(self.temp_value,2))+ u'\u00b0' + 'C'
        self.humidity_strval = str(round(self.humidity_value,2))+ "%"
        self.humidity_angle = 3.6*self.humidity_value

        if self.temp_value > 50:
            self.sen_color_temp = get_color_from_hex('#C73C4C')

        elif self.temp_value < 20:
            self.sen_color_temp = get_color_from_hex('#3DA3D1')

        else:
            self.sen_color_temp = get_color_from_hex('#3DA3D1')

        if self.humidity_value > 50:
            self.sen_color_humidity = get_color_from_hex('#C73C4C')

        elif self.humidity_value < 20:
            self.sen_color_humidity = get_color_from_hex('#3DA3D1')

        else:
            self.sen_color_humidity = get_color_from_hex('#3DA3D1')


# Reactor 3
class ReactorScreen3(ReactorScreen):
    def __init__(self,**kwargs):
        super(ReactorScreen3, self).__init__(**kwargs)
        self.name = "reactor3"
        Clock.schedule_once(self._finish_init)
        Clock.schedule_interval(self.get_value, 1)
        self.plot_temp = SmoothLinePlot(color = get_color_from_hex('#3DA3D1'))
        self.plot_humidity = SmoothLinePlot(color = get_color_from_hex('#3DA3D1'))


    def _finish_init(self, dt): 
        self.ids.main_label.text = "SENSOR 3"
        # print "added" 
        # if Window.size[0] > 500:
        #     self.ids.humid_meter.size_hint = (0.5,None)
        #     self.ids.temp_meter.size_hint = (0.5,None)
        #     self.ids.temp_graph_cover.size_hint = (0.5,None)
        #     self.ids.humidity_graph_cover.size_hint = (0.5,None)
        #     # print "yes"
        # else:
        #     pass
            # self.ids.humid_meter.size_hint = (1,None)
            # self.ids.temp_meter.size_hint = (1,None)
            # self.ids.temp_graph_cover.size_hint = (1,None)
            # self.ids.humidity_graph_cover.size_hint= (1,None)
            # self.ids.reactor_main_layout.spacing = 30


    
    def get_value(self,dt):
        self.main_header_color = netstatus_color
        self.ids.graph_temp.add_plot(self.plot_temp);
        self.ids.graph_humidity.add_plot(self.plot_humidity);
        self.ids.net.netstattxt = netstatus
        self.ids.net.netstatuscolor = netstatus_color
        self.plot_temp.points = [(i-25, j) for i, j in enumerate(levels_temp[2])]
        self.plot_humidity.points = [(i-25, j) for i, j in enumerate(levels_humidity[2])]
        # print self.plot.points
        self.temp_value = temp[2]
        self.humidity_value = 0
        self.temp_angle = 3.6*self.temp_value
        self.temp_strval = str(round(self.temp_value,2))+ u'\u00b0' + 'C'
        self.humidity_strval = str(round(self.humidity_value,2))+ "%"
        self.humidity_angle = 3.6*self.humidity_value

        if self.temp_value > 50:
            self.sen_color_temp = get_color_from_hex('#C73C4C')

        elif self.temp_value < 20:
            self.sen_color_temp = get_color_from_hex('#3DA3D1')

        else:
            self.sen_color_temp = get_color_from_hex('#3DA3D1')

        if self.humidity_value > 50:
            self.sen_color_humidity = get_color_from_hex('#C73C4C')

        elif self.humidity_value < 20:
            self.sen_color_humidity = get_color_from_hex('#3DA3D1')

        else:
            self.sen_color_humidity = get_color_from_hex('#3DA3D1')


class ReactorScreen4(ReactorScreen):
    def __init__(self,**kwargs):
        super(ReactorScreen4, self).__init__(**kwargs)
        self.name = "reactor4"
        Clock.schedule_once(self._finish_init)
        Clock.schedule_interval(self.get_value, 1)
        self.plot_temp = SmoothLinePlot(color = get_color_from_hex('#3DA3D1'))
        self.plot_humidity = SmoothLinePlot(color = get_color_from_hex('#3DA3D1'))


    def _finish_init(self, dt): 
        self.ids.main_label.text = "SENSOR 4"
        # print "added" 
        # if Window.size[0] > 500:
        #     self.ids.humid_meter.size_hint = (0.5,None)
        #     self.ids.temp_meter.size_hint = (0.5,None)
        #     self.ids.temp_graph_cover.size_hint = (0.5,None)
        #     self.ids.humidity_graph_cover.size_hint = (0.5,None)
        #     # print "yes"
        # else:
        #     pass
            # self.ids.humid_meter.size_hint = (1,None)
            # self.ids.temp_meter.size_hint = (1,None)
            # self.ids.temp_graph_cover.size_hint = (1,None)
            # self.ids.humidity_graph_cover.size_hint= (1,None)
            # self.ids.reactor_main_layout.spacing = 30


    
    def get_value(self,dt):
        self.main_header_color = netstatus_color
        self.ids.graph_temp.add_plot(self.plot_temp);
        self.ids.graph_humidity.add_plot(self.plot_humidity);
        self.ids.net.netstattxt = netstatus
        self.ids.net.netstatuscolor = netstatus_color
        self.plot_temp.points = [(i-25, j) for i, j in enumerate(levels_temp[3])]
        self.plot_humidity.points = [(i-25, j) for i, j in enumerate(levels_humidity[3])]
        # print self.plot.points
        self.temp_value = temp[3]
        self.humidity_value = 0
        self.temp_angle = 3.6*self.temp_value
        self.temp_strval = str(round(self.temp_value,2))+ u'\u00b0' + 'C'
        self.humidity_strval = str(round(self.humidity_value,2))+ "%"
        self.humidity_angle = 3.6*self.humidity_value

        if self.temp_value > 50:
            self.sen_color_temp = get_color_from_hex('#C73C4C')

        elif self.temp_value < 20:
            self.sen_color_temp = get_color_from_hex('#3DA3D1')

        else:
            self.sen_color_temp = get_color_from_hex('#3DA3D1')

        if self.humidity_value > 50:
            self.sen_color_humidity = get_color_from_hex('#C73C4C')

        elif self.humidity_value < 20:
            self.sen_color_humidity = get_color_from_hex('#3DA3D1')

        else:
            self.sen_color_humidity = get_color_from_hex('#3DA3D1')

        





### Main Screen Manager  ###

class ScreenManagement(ScreenManager):
    pass     

presentation = Builder.load_file("MyApp.kv")

class MyApp(App):
    def build(self):
        return presentation


if __name__ == '__main__':
    data = []
    temp = [30,80,30,30]
    dataRecv = ''
    netstatus = 'Waiting for Network...'
    netstatus_color = get_color_from_hex('#F26430')
    get_level_thread = Thread(target=get_data)
    get_level_thread.daemon = True
    get_level_thread.start()
    MyApp().run()