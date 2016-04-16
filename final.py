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
from kivy.uix.popup import Popup
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color
import time
import os
from functools import partial
from client import *
from kivy.graphics import Color,Rectangle

def get_filenames(location):
    files = os.listdir(location+"/")
    arr = []
    for i in files:
        directory = location+"/"+i
        arr.append(directory)
    return arr

def get_files(name):

        headlines = []
        image_file_name = []
        txt_file_name = []

        data = ""

        files = get_filenames(name)
        for file_name in files:
            data = ""
            if file_name[-4:]==".txt":
                f = open(file_name,'r')   
                data = f.read()
                f.close()
                
                data = data.split('#')
                txt_file_name.append(file_name[:-4])
                headlines.append(data[0])

            elif file_name[-4:]==".jpg":
                image_file_name.append(file_name[:-4])
        
        return txt_file_name,headlines,image_file_name

def get_file_details(name,news_type):
        f1=open(name+".txt" ,'r')
        x = " "
        data = ""
        while x:
            x = f1.read()
            data += x
            
        dat = data.split('#')
        f1.close()
        return dat

class Header(BoxLayout):
    def __init__(self,sm,**kwargs):
        super (Header,self).__init__(**kwargs)

        self.orientation = 'horizontal'
        self.size_hint = (1,0.1)

        btn_top      = Button(id = 'top_stories' , text = '[size=20][b]Top Stories[/b][/size]',background_color=(0,1,1,1),markup = True)
        btn_business = Button(id = 'business' , text = '[size=20][b]Business[/b][/size]',background_color=(0,.2,.8,1),markup = True)
        btn_latest   = Button(id = 'latest' , text = '[size=20][b]Latest[b][/size]',background_color=(0,1,1,1),markup = True)
        btn_sports   = Button(id = 'across_toi' , text = '[size=20][b]Sports[/b][/size]',background_color=(0,1,1,1),markup = True)
        btn_refresh  = Button(id = 'refresh' , text = '[b]Refresh[/b]',background_color=(0,1,1,1),size_hint = (0.3,1),markup = True)

        btn_top.bind(on_press = partial(self.onClick,'top_stories',sm))
        btn_business.bind(on_press = partial(self.onClick,'business',sm))
        btn_latest.bind(on_press = partial(self.onClick,'latest',sm))
        btn_sports.bind(on_press = partial(self.onClick,'across_toi',sm))
        btn_refresh.bind(on_press = partial(self.refresh,sm))

        self.add_widget(btn_refresh)
        self.add_widget(btn_top)
        self.add_widget(btn_latest)
        self.add_widget(btn_business)
        self.add_widget(btn_sports)

    def onClick(self,*args):
 
        args[1].current = args[0]
        screen = args[1].get_screen(args[0])

        for child in screen.children[0].children[1].children:
            if child.id == args[0]:
                child.background_color=(0,.2,.8,1)
            else:
                child.background_color=(0,1,1,1)

    def refresh(self,*args):
        
        news_type = args[0].current

        try :
            client(news_type)
        except:
            popup = Popup(title='Error', size_hint = (None,None) , size=(200, 200),content=Label(text='Server Not Responding'))
            popup.open()
            return;

        screen = args[0].get_screen(news_type)
        args[0].remove_widget(screen) 

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

        for child in screen.children[0].children[1].children:
                if child.id == news_type:
                    child.background_color=(0,.2,.8,1)
                else:
                    child.background_color=(0,1,1,1)

class scrollview1(ScrollView):

    def __init__(self,txt_file_name,headlines,image_file_name,news_type,sm,**kwargs):
        super (scrollview1,self).__init__(**kwargs)

        layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        for i in range(30):
            try :
                if txt_file_name[i] in image_file_name:
                    src = txt_file_name[i]+".jpg"
                else :
                    src = "IMG_1865.jpg"
            except :
                break

            box1 = BoxLayout(orientation = 'horizontal',size_hint_y=None)
            img  = Image(source = src,keep_ratio = False,size_hint = (0.25,1))
            

            btn  = Button(text = headlines[i], background_color = (0,.2,.8,1),size_hint = (1.75,1),halign = 'left',
                    valign = 'middle',padding = (8,2))
            btn.bind(on_press = partial(self.onClick,txt_file_name[i],news_type,sm))
            #btn.bind(on_size = partial(self.onClick))
            btn.bind(texture_size=btn.setter('size'))
            btn.bind(width=lambda s, w:
                       s.setter('text_size')(s, (w, None)))

            box1.add_widget(img)
            box1.add_widget(btn)
            layout.add_widget(box1)

           #btn.text_size = (1000,btn.height+350)

            with btn.canvas.before:
                Color(img)
                btn.rect = Rectangle(size=self.size , pos = self.pos)
            btn.bind(pos = self.update_rect , size = self.update_rect)

        self.add_widget(layout)
    
    def onClick(self,*args):

        chk = args[2].has_screen(args[0])

        if chk==False:
            screen = Detail(args[0],args[1],args[2],name = args[0])
            args[2].add_widget(screen)
            args[2].current = args[0]

        else:
            screen_obj = args[2].get_screen(args[0])
            args[2].remove_widget(screen_obj)
            screen = Detail(args[0],args[1],args[2],name = args[0])
            args[2].add_widget(screen)
            args[2].current = args[0]

    def update_rect(self,instance,value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

class Detail(Screen):
    def __init__(self,file_name,news_type,sm,**kwargs):
        super (Detail,self).__init__(**kwargs)
        image_exists = True


        float_layout = FloatLayout(size_hint = (1,1))

        scroll_view  = ScrollView()
        box_layout   = BoxLayout(orientation = 'vertical',size_hint = (1,1),background_color = (0,1,1,2))
        data         = get_file_details(file_name,news_type)

        img_src      = file_name+".jpg"
        
        if os.path.exists(img_src)==False:
            img_src  = "IMG_1865.jpg"
            image_exists = False
        
        news_img    = Image(id = 'img' , source = img_src,size_hint=(1,0.6))
        back_img    = Image(source = 'IMG_1871.jpg',allow_strech = True ,
                             keep_ratio = False , size_hint = (1.28,1.4),pos = (0,0))
        
        image_text  = Label(id = 'image_text' , text = '[size=20][b]'+data[1]+'[/b][/size]',
                            size_hint = (1,0.1),markup = True,underline =True)

        
        back_button = Button(text = 'Back',pos = (36,625),size_hint=(0.05,0.09))
        
        img2        = Image(source = 'back_2.png',size_hint=(0.02,0.02),allow_strech = True , keep_ratio = False ,)

        back_button.add_widget(img2)
        img2.pos    = (20,605)


        img2.bind(width=lambda s, w:
                   s.setter('text_size')(s, (w, None)))
        img2.bind(on_size = img2.setter('pos'))

        back_button.bind(on_press = partial(self.onClick,news_type,sm))
        
        try :
            text        = Label(id = 'text' , text = '[color=ffffff]'+data[2]+'[/color]',
                            markup = True,halign = 'left',valign = 'middle' ,size_hint_y = None,font_size='18sp')
            text.bind(on_size = partial(self.onClick))
            text.bind(texture_size=text.setter('size'))
            text.bind(width=lambda s, w:
                   s.setter('text_size')(s, (w, None)))
            scroll_view.add_widget(text)
        except:
            self.trigger_popup(sm,file_name)


        if image_exists:
           box_layout.add_widget(news_img)
        else :
            box_layout.padding = (5,50)
            image_text  = Label(id = 'image_text' , text = '[size=30][b]'+data[1]+'[/b][/size]',
                            size_hint = (1,0.1),markup = True,underline =True) 

        box_layout.add_widget(image_text)
        box_layout.add_widget(scroll_view)
        
        float_layout.add_widget(back_img)
        float_layout.add_widget(box_layout)
        float_layout.add_widget(back_button)

        self.add_widget(float_layout)

    def onClick(self,*args):
        args[1].current = args[0]

    def trigger_popup(self,*args):
        popup = Popup(title='Error', size_hint = (None,None) , size=(200, 200),content=Label(text='No Text Available'))
        popup.open()


class Top(Screen):
    def __init__(self,sm,**kwargs):
        super (Top,self).__init__(**kwargs)

        box_parent = BoxLayout(orientation = 'vertical')
        header     = Header(sm)
        layout2    = BoxLayout(orientation = 'vertical',size_hint = (1,0.9))

        txt_file_name,headlines,image_file_name = get_files("top_stories")

        scrollview = scrollview1(txt_file_name,headlines,image_file_name,"top_stories",sm)
        
        layout2.add_widget(scrollview)
        
        box_parent.add_widget(header)
        box_parent.add_widget(layout2)

        self.add_widget(box_parent)      

    

class Business(Screen):
    def __init__(self,sm,**kwargs):
        super (Business,self).__init__(**kwargs)

        box_parent = BoxLayout(orientation = 'vertical')
        header     = Header(sm)
        layout2    = BoxLayout(orientation = 'vertical',size_hint = (1,0.9))

        txt_file_name,headlines,image_file_name = get_files("business")

        scrollview = scrollview1(txt_file_name,headlines,image_file_name,"business",sm)
        
        layout2.add_widget(scrollview)

        box_parent.add_widget(header)
        box_parent.add_widget(layout2)

        self.add_widget(box_parent)      

    

class Latest(Screen):
    def __init__(self,sm,**kwargs):
        super (Latest,self).__init__(**kwargs)
        box_parent = BoxLayout(orientation = 'vertical')
        header     = Header(sm)
        layout2    = BoxLayout(orientation = 'vertical',size_hint = (1,0.9))

        txt_file_name,headlines,image_file_name = get_files("latest")

        scrollview = scrollview1(txt_file_name,headlines,image_file_name,"latest",sm)
        layout2.add_widget(scrollview)

        box_parent.add_widget(header)
        box_parent.add_widget(layout2)

        self.add_widget(box_parent)
        
    
class Sports(Screen):
    def __init__(self,sm,**kwargs):
        super (Sports,self).__init__(**kwargs)

        box_parent = BoxLayout(orientation = 'vertical')
        header     = Header(sm)
        layout2    = BoxLayout(orientation = 'vertical',size_hint = (1,0.9))

        txt_file_name,headlines,image_file_name = get_files("across_toi")

        scrollview = scrollview1(txt_file_name,headlines,image_file_name,"across_toi",sm)
        layout2.add_widget(scrollview)

        box_parent.add_widget(header)
        box_parent.add_widget(layout2)

        self.add_widget(box_parent)
        
    


class TestApp(App):
    def build(self):
        sm = ScreenManager()

        top      = Top(sm,name = 'top_stories')
        business = Business(sm,name = 'business')
        latest   = Latest(sm,name = 'latest')
        sports   = Sports(sm,name = 'across_toi')

        sm.add_widget(business)
        sm.add_widget(top)
        sm.add_widget(latest)
        sm.add_widget(sports)

        sm.transition = FadeTransition()

        return sm


if __name__=="__main__":
    os.system('python client.py')
    TestApp().run()
