from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen,FadeTransition
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color
import time
import os
from functools import partial
from client import *

def get_filenames(location):
    #print location
    files = os.listdir(location+"/")
    print files
    arr = []
    for i in files:
        directory = location+"/"+i
        arr.append(directory)
    return arr

def get_files(name):

    # f1=open("C:\Users\Prabhjot\SkyDrive\Documents\Git\\networkingproject\\"+name+".txt" ,'rb')
    
    headline = []
    # x = " "
    image_file_name = []
    txt_file_name = []

    # while x:
    #     x = f1.read()
    #     data += x
    # data = data.split("helloFROMtheINSIDE")
    # f1.close()
    # j=0
    # i=0
    # dat = []
    # while True:

    #     string = data[i]
    #     if string[-4:]==".txt":
    #         x=data[i+1]
    #         x = x.split('#')
    #         txt_file_name.append(string[:-4])
    #         dat.append(x[0])
    #     elif string[-4:]==".jpg":
    #         fname = string[:-4]
    #         jpeg_data[fname] = data[i+1]
    #         #print "fname = ",fname
    #         #print "Next file = ",data[i+2]
    #     else:
    #         break

    #     i=i+2
    #     #print i
    #     j=j+1

    files = get_filenames(name)
    for file_name in files:
        if file_name[-4:]==".txt":

            f = open(file_name,'r')
            data = f.read()
            f.close()
            
            data = data.split('#')
            txt_file_name.append(file_name[:-4])
            headline.append(data[0])

        elif file_name[-4:]==".jpg":
            fname = file_name[:-4]
            image_file_name.append(fname)

    return txt_file_name,headline,image_file_name
def get_file_details(name,news_type):
    f1=open("C:\Users\Prabhjot\SkyDrive\Documents\Git\\networkingproject\\"+news_type+"\\"+name+".txt" ,'r')
    #print "Name , News_Type ================================= ",name,news_type
    x = " "
    data = ""
    while x:
        x = f1.read()
        data += x
        
    dat = data.split('#')
    f1.close()
    return dat

class Header(BoxLayout):
    def __init__(self,screen,**kwargs):
        super (Header,self).__init__(**kwargs)

        self.orientation = 'horizontal'
        self.size_hint = (1,0.1)

        btn_top      = Button(id = 'top_stories' , text = 'Top Stories',background_color=(1,1,10,7))
        btn_business = Button(id = 'business' , text = 'Business',background_color=(1,1,10,7))
        btn_latest   = Button(id = 'latest' , text = 'Latest',background_color=(1,1,10,7))
        btn_sports   = Button(id = 'across_toi' , text = 'Sports',background_color=(1,1,10,7))
        btn_refresh  = Button(id = 'refresh' , text = 'Refresh',background_color=(1,1,10,7),size_hint = (0.3,1))

        btn_top.bind(on_press = partial(self.onClick,'top_stories',screen))
        btn_business.bind(on_press = partial(self.onClick,'business',screen))
        btn_latest.bind(on_press = partial(self.onClick,'latest',screen))
        btn_sports.bind(on_press = partial(self.onClick,'across_toi',screen))
        btn_refresh.bind(on_press = partial(self.refresh,screen))

        self.add_widget(btn_top)
        self.add_widget(btn_latest)
        self.add_widget(btn_business)
        self.add_widget(btn_sports)
        self.add_widget(btn_refresh)

    def onClick(self,*args):
 
        args[1].current = args[0]
        screen = args[1].get_screen(args[0])

        for child in screen.children[0].children[1].children:
            if child.id == args[0]:
                child.background_color=(1,0,0,1)
            else:
                child.background_color=(1,1,10,7)

    def refresh(self,*args):
        news_type = args[0].current

        screen = args[0].get_screen(news_type)
        args[0].remove_widget(screen)
        client_in_the_house(1,news_type)

        if news_type == 'business':
            screen = Business(args[0],name = 'business')
            args[0].add_widget(screen)
            args[0].current = news_type
        if news_type == 'top_stories':
            screen = Top(args[0],name = 'top_stories')
            args[0].add_widget(screen)
            args[0].current = news_type
        if news_type == 'latest':
            screen = Latest(args[0],name = 'latest')
            args[0].add_widget(screen)
            args[0].current = news_type
        if news_type == 'across_toi':
            screen = Sports(args[0],name = 'across_toi')
            args[0].add_widget(screen)
            args[0].current = news_type

class scrollview1(ScrollView):

    def __init__(self,txt_file_name,headline,image_file_name,news_type,sm,**kwargs):
        super (scrollview1,self).__init__(**kwargs)

        

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(30):

            try :
                if txt_file_name[i] in image_file_name == True:
                    src = txt_file_name[i]+".jpg"
                else :
                    src = "IMG_1865.jpg"
            except :
                break

            box1 = BoxLayout(orientation = 'horizontal',size_hint_y=None)
            img  = Image(source = src,keep_ratio = False,size_hint = (0.25,1))
            print i

            btn  = Button(text = headline[i], background_color = (1,0,0,1),size_hint = (1.75,1),halign = 'left',valign = 'middle',padding = (8,2))
            btn.bind(on_press = partial(self.onClick,txt_file_name[i],news_type,sm))
            #btn.bind(on_size = partial(self.onClick))
            btn.bind(texture_size=btn.setter('size'))
            btn.bind(width=lambda s, w:
                       s.setter('text_size')(s, (w, None)))

            box1.add_widget(img)
            box1.add_widget(btn)
            layout.add_widget(box1)

            btn.text_size = (1000,btn.height+350)

        self.add_widget(layout)
    def onClick(self,*args):

        chk = args[2].has_screen(args[0])

        if chk==False:
            screen = Detail(args[0],args[1],args[2],name = args[0])
            args[2].add_widget(screen)
            args[2].current = args[0]

        else:
            args[2].current = args[0]


class Detail(Screen):
    def __init__(self,file_name,news_type,sm,**kwargs):
        super (Detail,self).__init__(**kwargs)
        image_exists = True


        float_layout = FloatLayout(size_hint = (1,1))

        scroll_view  = ScrollView()
        box_layout   = BoxLayout(orientation = 'vertical',size_hint = (1,1),background_color = (0,1,1,2))
        data         = get_file_details(file_name,news_type)

        img_src = file_name+".jpg"
        print "Img_src = ",img_src
        if os.path.exists(img_src)==False:
            img_src = "IMG_1865.jpg"
            image_exists = False
        
        img         = Image(id = 'img' , source = img_src,size_hint=(1,0.6))
        back_img    = Image(source = 'IMG_1865.jpg',allow_strech = True , keep_ratio = False , size_hint = (1.28,1.4),pos = (0,0))
        image_text  = Label(id = 'image_text' , text = '[size=20][b]'+data[1]+'[/b][/size]',size_hint = (1,0.1),markup = True)
        text        = Label(id = 'text' , text = '[color=ffffff]'+data[2]+'[/color]',markup = True,halign = 'left' ,
                             valign = 'middle',size_hint_y = None,font_size='18sp')
        back_button = Button(text = 'Back',pos = (36,625),size_hint=(0.05,0.09))
        
        img2 = Image(source = 'back.png',size_hint=(1,1),allow_strech = True , keep_ratio = False ,)
        img2.bind(width=lambda s, w:
                   s.setter('text_size')(s, (w, None)))
        # img2.bind(on_size = img2.setter('pos'))
        back_button.add_widget(img2)
        img2.pos = (20,605)

        back_button.bind(on_press = partial(self.onClick,news_type,text,sm))
        text.bind(on_size = partial(self.onClick))
        text.bind(texture_size=text.setter('size'))
        text.bind(width=lambda s, w:
                   s.setter('text_size')(s, (w, None)))
        
        
        scroll_view.add_widget(text)

        if image_exists:
            box_layout.add_widget(img)
        box_layout.add_widget(image_text)
        box_layout.add_widget(scroll_view)
        float_layout.add_widget(back_img)
        float_layout.add_widget(box_layout)
        float_layout.add_widget(back_button)

        self.add_widget(float_layout)

    def onClick(self,*args):
        args[2].current = args[0]


class Screen1(Screen):
    def __init__(self,**kwargs):
        super (Screen1,self).__init__(**kwargs)
        layout1 = BoxLayout(orientation = 'vertical')
        b1 = Button(id = 'b1',text = "First",background_color = (1,0,0,1))
        b1.bind(on_release = self.change_screen)
        b2 = Button(id = 'b2',text = "First",background_color = (1,0,0,1))
        b2.bind(on_release = self.change_screen)
        
        layout1.add_widget(b1)
        layout1.add_widget(b2)
        self.add_widget(layout1)

    def change_screen(self,*args):
       pass# self.manager.current = 'screen2'


class Top(Screen):
    def __init__(self,sm,**kwargs):
        super (Top,self).__init__(**kwargs)

        box_parent = BoxLayout(orientation = 'vertical')

        header = Header(sm)

        layout2 = BoxLayout(orientation = 'vertical',size_hint = (1,0.9))

        txt_file_name,headline,image_file_name = get_files("top_stories")

        scrollview = scrollview1(txt_file_name,headline,image_file_name,"top_stories",sm)
        layout2.add_widget(scrollview)

        box_parent.add_widget(header)
        box_parent.add_widget(layout2)

        self.add_widget(box_parent)
        

    def change_screen(self,*args):
        print self.manager , args
        self.manager.current = 'screen1'
        
class Business(Screen):
    def __init__(self,sm,**kwargs):
        super (Business,self).__init__(**kwargs)

        box_parent = BoxLayout(orientation = 'vertical')

        header = Header(sm)

        layout2 = BoxLayout(orientation = 'vertical',size_hint = (1,0.9))

        txt_file_name,headline,image_file_name = get_files("business")

        scrollview = scrollview1(txt_file_name,headline,image_file_name,"business",sm)
        layout2.add_widget(scrollview)

        box_parent.add_widget(header)
        box_parent.add_widget(layout2)

        self.add_widget(box_parent)
        

    def change_screen(self,*args):
        print self.manager , args
        self.manager.current = 'screen1'

class Latest(Screen):
    def __init__(self,sm,**kwargs):
        super (Latest,self).__init__(**kwargs)

        box_parent = BoxLayout(orientation = 'vertical')

        header = Header(sm)

        layout2 = BoxLayout(orientation = 'vertical',size_hint = (1,0.9))

        txt_file_name,headline,image_file_name = get_files("latest")

        scrollview = scrollview1(txt_file_name,headline,image_file_name,"latest",sm)
        layout2.add_widget(scrollview)

        box_parent.add_widget(header)
        box_parent.add_widget(layout2)

        self.add_widget(box_parent)
        

    def change_screen(self,*args):
        print self.manager , args
        self.manager.current = 'screen1'

class Sports(Screen):
    def __init__(self,sm,**kwargs):
        super (Sports,self).__init__(**kwargs)

        box_parent = BoxLayout(orientation = 'vertical')

        header = Header(sm)

        layout2 = BoxLayout(orientation = 'vertical',size_hint = (1,0.9))

        txt_file_name,headline,image_file_name = get_files("across_toi")

        scrollview = scrollview1(txt_file_name,headline,image_file_name,"across_toi",sm)
        layout2.add_widget(scrollview)

        box_parent.add_widget(header)
        box_parent.add_widget(layout2)

        self.add_widget(box_parent)
        

    def change_screen(self,*args):
        print self.manager , args
        self.manager.current = 'screen1'



class TestApp(App):
    def build(self):
        sm = ScreenManager()

        top = Top(sm,name = 'top_stories')
        business = Business(sm,name = 'business')
        latest = Latest(sm,name = 'latest')
        sports = Sports(sm,name = 'across_toi')

        sm.add_widget(business)
        sm.add_widget(top)
        sm.add_widget(latest)
        sm.add_widget(sports)
        sm.transition = FadeTransition()

        print "Initial Print = ",sm.children
        return sm
if __name__=="__main__":
    os.system('python client.py')
    TestApp().run()

