import cocos
from cocos.layer import *
from cocos.menu import *
from cocos.text import *
import pyglet

class Title_Layer(ColorLayer):
    #FONT_SIZE = 30
    def __init__(self):
        w,h = director.get_window_size()
        super(Title_Layer,self).__init__(32,100,32,16, width= w, height= h)

        self.font_title['font_name'] = 'Arial'
        self.font_title['font_size'] = 32
        self.font_title['color'] = (204, 164, 164, 255)

        title = Label('BattlefieldCrawler', **self.font_title)
        #title.position=(w/2,h)
        self.add(title)

class Options_Menu(Menu):
    def __init__(self):
        super(Options_Menu, self).__init__('Battlefield Crawler')
        '''self.font_title['font_name'] = 'Arial'
        self.font_title['font_size'] = 32
        self.font_title['color'] = (204,164,164,255)'''
        self.font_item['font_name'] = 'Arial'
        self.font_item['font_size'] = 20
        self.font_item['color'] = (255,255,255,255)

        self.font_item_selected['font_name'] = 'Arial'
        self.font_item_selected['font_size'] = 20
        self.font_item_selected['color'] = (160,126,174,255)

        self.menu_anchor_y = CENTER
        self.menu_anchor_x = CENTER

        op_menu = []
        op_menu.append( ToggleMenuItem('Pokaż licznik FPS: ', self.on_show_fps, director.show_FPS) )
        op_menu.append( MenuItem('Pełny Ekran', self.on_fullscreen))
        op_menu.append( MenuItem('Powrót', self.on_quit))
        self.create_menu(op_menu, shake(), shake_back())

    def on_fullscreen(self):
        director.window.set_fullscreen( not director.window.fullscreen )
    def on_quit(self):
        self.parent.switch_to(0)
    def on_show_fps(self, x):
        director.show_FPS = x

class Main_Menu( Menu ):
    def __init__(self):
        super(Main_Menu, self).__init__('Battlefield Crawler')
        '''self.font_title['font_name'] = 'Arial'
        self.font_title['font_size'] = 32
        self.font_title['color'] = (204, 164, 164, 255)'''
        self.font_item['font_name'] = 'Arial'
        self.font_item['font_size'] = 20
        self.font_item['color'] = (255,255,255,255)

        self.font_item_selected['font_name'] = 'Arial'
        self.font_item_selected['font_size'] = 20

        self.font_item_selected['color'] = (160,126,174,255)

        self.menu_anchor_y = CENTER
        self.menu_anchor_x = CENTER

        main_menu = []
        main_menu.append(MenuItem('Nowa Gra', self.on_new_game))
        main_menu.append(MenuItem('Opcje', self.on_option_menu))
        main_menu.append(MenuItem('Wyjdź', self.on_quit))
        self.create_menu(main_menu, shake(), shake_back())

    def on_new_game(self):
        import characters
        director.push(characters.get_newgame())
    def on_option_menu(self):
        self.parent.switch_to(1)
    def on_quit(self):
        pyglet.app.exit()

if __name__ == "__main__":
    director.init(resizable = True, width =1280, height=720, caption = "Battlefield Crawler")
    
    scene = cocos.scene.Scene()
    scene.add( MultiplexLayer(
                Main_Menu(),
                Options_Menu()
                            ))
    scene.add(cocos.layer.ColorLayer(105, 94, 109, 255), z=-1)
    director.run(scene)