'''
Showcase of Kivy Features
=========================

This showcases many features of Kivy. You should see a
menu bar across the top with a demonstration area below. The
first demonstration is the accordion layout. You can see, but not
edit, the kv language code for any screen by pressing the bug or
'show source' icon. Scroll through the demonstrations using the
left and right icons in the top right or selecting from the menu
bar.

The file showcase.kv describes the main container, while each demonstration
pane is described in a separate .kv file in the data/screens directory.
The image data/background.png provides the gradient background while the
icons in data/icon directory are used in the control bar. The file
data/faust_github.jpg is used in the Scatter pane. The icons are
from `http://www.gentleface.com/free_icon_set.html` and licensed as
Creative Commons - Attribution and Non-commercial Use Only; they
sell a commercial license.

The file android.txt is used to package the application for use with the
Kivy Launcher Android application. For Android devices, you can
copy/paste this directory into /sdcard/kivy/showcase on your Android device.

'''

from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

import requests
import re
import urllib.parse
import base64
import hashlib
import binascii

datas = []
data_set = {}
text_set = {}

class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ShowcaseScreen, self).add_widget(*args)


class ShowcaseApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])

    def build(self):
        self.title = 'lighted hackbar'
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = sorted([
            'send packets', "Tutorial", "Encode"
        ])
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
            '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        self.go_next_screen()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_current_title(self, instance, value):
        self.root.ids.spnr.text = value

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        self.update_sourcecode()

    def go_hierarchy_previous(self):
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen

    def read_sourcecode(self):
        fn = self.available_screens[self.index]
        with open(fn) as fd:
            return fd.read()

    def toggle_source_code(self):
        self.show_sourcecode = not self.show_sourcecode
        if self.show_sourcecode:
            height = self.root.height * .3
        else:
            height = 0

        Animation(height=height, d=.3, t='out_quart').start(
                self.root.ids.sv)

        self.update_sourcecode()

    def update_sourcecode(self):
        if not self.show_sourcecode:
            self.root.ids.sourcecode.focus = False
            return
        self.root.ids.sourcecode.text = self.read_sourcecode()
        self.root.ids.sv.scroll_y = 1

    def showcase_floatlayout(self, layout):
        def do_something(self):
            print("sending......")
            print(user_agent.text)
            headers_ = {}
            if user_agent.text:
                headers_['user-agent'] = user_agent.text
            if Referer.text:
                headers_['Referer'] = Referer.text
            if cookie.text:
                headers_['cookies'] = cookie.text
            
            try:
                print(headers_)
                r = requests.get(URL.text, headers = headers_, timeout=5)
                r.encoding = 'utf-8'
                print(r.text)
            except:
                print("Invalid Parameters !")
        
        URL = TextInput(text='', multiline=False, x = 150, y=435,size_hint=(None, None), height=30, width=500)
        layout.add_widget(URL)
        user_agent = TextInput(text='', multiline=False, x = 150, y=385,size_hint=(None, None), height=30, width=300)
        layout.add_widget(user_agent)
        Referer = TextInput(text='', multiline=False, x = 150, y=335,size_hint=(None, None), height=30, width=300)
        layout.add_widget(Referer)
        cookie = TextInput(text='', multiline=False, x = 150, y=285,size_hint=(None, None), height=30, width=300)
        layout.add_widget(cookie)
        confirm = Button(size_hint=(None, None), x=650, y=50, height=30, width=80, text='send')
        layout.add_widget(confirm)
        confirm.bind(on_press=do_something)
        

    def showcase_boxlayout(self, layout):
        def getPostData(self):

            try:
                global datas
                datas = []
                html = requests.get(URL.text).text
                pos = 0
                while pos != -1:
                        pos1 = html.find('<input')
                        pos2 = html.find('<textarea')
                        if pos1 == -1:
                            pos = pos2
                        elif pos2 == -1:
                            pos = pos1
                        else:
                            pos = min(pos1, pos2)

                        pos_end = html[pos:].find('>')
                        name = re.search("name[^\S]*=[^\S]*[\'\"][\w]*[\'\"]", html[pos:pos+pos_end+1])
                        if name:
                            name = name.group().replace('\'', '\"').split('\"')[1]
                            datas.append(name)
                        html = html[pos+pos_end+1:]
            except:
                print("Invalid URL")
            
            # add box for each data
            for i, data in enumerate(datas):
                data_set[i] = Label(text = data, size_hint=(None, None), x=130, y=230-i*50, height=30, width=80)
                layout.add_widget(data_set[i])
                text_set[i] = TextInput(text='', multiline=False, x = 200, y=230-i*50,size_hint=(None, None), height=30, width=300)
                layout.add_widget(text_set[i])



        def do_something(self):
            print("sending......")
            print(user_agent.text)
            headers_ = {}
            if user_agent.text:
                headers_['user-agent'] = user_agent.text
            if Referer.text:
                headers_['Referer'] = Referer.text
            if cookie.text:
                headers_['cookies'] = cookie.text

            print(datas)
            params = {}
            for i, d in enumerate(datas):
            	params[d] = text_set[i].text

            print(params)

            
            try:
                r = requests.get(URL.text, headers = headers_, data=params, timeout=5)
                r.encoding = 'utf-8'
                print(r.text)
            except:
                print("Invalid Parameters !")
        
        URL = TextInput(text='', multiline=False, x = 150, y=435,size_hint=(None, None), height=30, width=500)
        layout.add_widget(URL)
        user_agent = TextInput(text='', multiline=False, x = 150, y=385,size_hint=(None, None), height=30, width=300)
        layout.add_widget(user_agent)
        Referer = TextInput(text='', multiline=False, x = 150, y=335,size_hint=(None, None), height=30, width=300)
        layout.add_widget(Referer)
        cookie = TextInput(text='', multiline=False, x = 150, y=285,size_hint=(None, None), height=30, width=300)
        layout.add_widget(cookie)
        confirm = Button(size_hint=(None, None), x=650, y=50, height=30, width=80, text='send')
        layout.add_widget(confirm)
        confirm.bind(on_press=do_something)
        postData = Button(size_hint=(None, None),x=60,y=230,height=40,width=80,text='Post')
        layout.add_widget(postData)
        postData.bind(on_press=getPostData)


    def show_webencoding_method(self, layout):
        def urlencode(self):
            URLEncode.text = urllib.parse.quote(URLEncode.text)

        urlconfirm = Button(size_hint=(None, None), x=60, y=433, width=100, height=33, text='URLEncode')
        urlconfirm.bind(on_press=urlencode)
        layout.add_widget(urlconfirm)
        URLEncode = TextInput(text='', multiline=False, x = 180, y=435,size_hint=(None, None), height=30, width=500)
        layout.add_widget(URLEncode)

    def show_encoding_method(self, layout):
        def base64encode(self):            
            base64text.text = base64.b64encode(bytes(base64text.text, 'utf-8'))
        def md5encode(self):
            m = hashlib.md5()
            m.update(bytes(md5text.text, 'utf-8'))
            md5text.text = m.hexdigest()
        def hexencode(self):
            try:
                hextext.text = binascii.hexlify(bytes(hextext.text, 'utf-8'))
            except:
                print("[hex] Invalid input")

        base64confirm = Button(size_hint=(None, None), x=60, y=433, width=100, height=33, text='base64')
        base64confirm.bind(on_press=base64encode)
        layout.add_widget(base64confirm)
        base64text = TextInput(text='', multiline=False, x = 180, y=435,size_hint=(None, None), height=30, width=500)
        layout.add_widget(base64text)
        md5confirm = Button(size_hint=(None, None), x=60, y=383, width=100, height=33, text='md5')
        md5confirm.bind(on_press=md5encode)
        layout.add_widget(md5confirm)
        md5text = TextInput(text='', multiline=False, x = 180, y=385,size_hint=(None, None), height=30, width=500)
        layout.add_widget(md5text)
        hexconfirm = Button(size_hint=(None, None), x=60, y=333, width=100, height=33, text='hex')
        hexconfirm.bind(on_press=hexencode)
        layout.add_widget(hexconfirm)
        hextext = TextInput(text='', multiline=False, x = 180, y=335,size_hint=(None, None), height=30, width=500)
        layout.add_widget(hextext)
    
    def search_source_code(self, layout):
        def search(self):
            #try:
            code = requests.get(URL.text, timeout=5).text
            print(code)
            #except:
             #   print("Invlid URL")

        confirm = Button(size_hint=(None, None), x=320, y=200, width=100, height=33, text='search')
        confirm.bind(on_press=search)
        layout.add_widget(confirm)
        URL = TextInput(text='', multiline=False, x = 140, y=255,size_hint=(None, None), height=30, width=500)
        layout.add_widget(URL)

    def show_decoding_method(self, layout):
        def base64decode(self):            
            base64text.text = base64.b64decode(bytes(base64text.text, 'utf-8'))
        def md5decode(self):
            m = hashlib.md5()
            m.update(bytes(md5text.text, 'utf-8'))
            md5text.text = m.hexdigest()
        def hexdecode(self):
            try:
                hextext.text = binascii.unhexlify(bytes(hextext.text, 'utf-8'))
            except:
                print("[hex] Invalid input")

        base64confirm = Button(size_hint=(None, None), x=60, y=433, width=100, height=33, text='base64')
        base64confirm.bind(on_press=base64decode)
        layout.add_widget(base64confirm)
        base64text = TextInput(text='', multiline=False, x = 180, y=435,size_hint=(None, None), height=30, width=500)
        layout.add_widget(base64text)
        md5confirm = Button(size_hint=(None, None), x=60, y=383, width=100, height=33, text='md5')
        md5confirm.bind(on_press=md5decode)
        layout.add_widget(md5confirm)
        md5text = TextInput(text='', multiline=False, x = 180, y=385,size_hint=(None, None), height=30, width=500)
        layout.add_widget(md5text)
        hexconfirm = Button(size_hint=(None, None), x=60, y=333, width=100, height=33, text='hex')
        hexconfirm.bind(on_press=hexdecode)
        layout.add_widget(hexconfirm)
        hextext = TextInput(text='', multiline=False, x = 180, y=335,size_hint=(None, None), height=30, width=500)
        layout.add_widget(hextext)

    def showcase_gridlayout(self, layout):
        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 15:
                layout.rows = 3 if layout.rows is None else None
                layout.cols = None if layout.rows == 3 else 3
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
Button:
    text:
        'rows: {}\\ncols: {}'.format(self.parent.rows, self.parent.cols)\
        if self.parent else ''
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_stacklayout(self, layout):
        orientations = ('lr-tb', 'tb-lr',
                        'rl-tb', 'tb-rl',
                        'lr-bt', 'bt-lr',
                        'rl-bt', 'bt-rl')

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 11:
                layout.clear_widgets()
                cur_orientation = orientations.index(layout.orientation)
                layout.orientation = orientations[cur_orientation - 1]
            layout.add_widget(Builder.load_string('''
Button:
    text: self.parent.orientation if self.parent else ''
    size_hint: .2, .2
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_anchorlayout(self, layout):

        def change_anchor(self, *l):
            if not layout.get_parent_window():
                return
            anchor_x = ('left', 'center', 'right')
            anchor_y = ('top', 'center', 'bottom')
            if layout.anchor_x == 'left':
                layout.anchor_y = anchor_y[anchor_y.index(layout.anchor_y) - 1]
            layout.anchor_x = anchor_x[anchor_x.index(layout.anchor_x) - 1]

            Clock.schedule_once(change_anchor, 1)
        Clock.schedule_once(change_anchor, 1)

    def _update_clock(self, dt):
        self.time = time()


if __name__ == '__main__':
    ShowcaseApp().run()
