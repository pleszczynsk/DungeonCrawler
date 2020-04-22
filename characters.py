import cocos
from cocos.director import director
import cocos.collision_model as colmod
import cocos.euclid as euc
import cocos.actions as act

import pyglet
from pyglet.window import key
from pyglet.gl import *

consts = {
    "game_area":{
        "width":400,
        "height: 300",
        "r": 8.0,
        "wall_scale_min": 0,75,
         "wall_scale_max": 2,25,
        "top_speed": 100.0
        "acceleration": 85.0
        "ang_velocity": 240.0
        "bindings":{
            key.LEFT: 'left',
            key.RIGHT: 'right'
            key.UP: 'up',
        }
    },
    "view":{
        "palette":{
            'bg': (0, 65, 133),
            'player': (237, 27, 36),
            'wall': (247, 148, 29),
        }
    }
}

x_window,y_window = director.get_window_size()
scale_x = x_window/consts["game_area"]["width"]
scale_y = y_window/consts["game_area"]["width"]

def world_view(v):
    return v.x *scale_x, v.y * scale_y

class Player(cocos.sprite.Sprite):
    palete ={}
    def __init__(self, cx, cy, radius, btype, img, vel = None):
        super(Player,self).__init__(img)
        self.scale = (radius *1.05) * scale_x/(self.image.width/2.0)
        self.btype = btype
        self.color = self.palette[btype]
        self.cshape = colmod.CircleShape(euc.Vector2(cx,cy), radius)
        self.update_center(self.cshape.center)
        if vel is None:
            vel = euc.Vector2(0.0,0.0)
        self.vel = vel

    def update_center(self, cshape_center):
        self.position = world_view(cshape_center)
        self.cshape.center = cshape_center

class World(cocos.layer.Layer):
    is_event_handler = True
    def __init__(self):
        super(World, self).__init__()
        world = consts['world']
        self.width = world['width']
        self.height = world['height']
        self.rPlayer = world['r']
        self.wall_scale_min = world['wall_scale_min']
        self.wall_scale_max = world['wall_scale_max']
        self.top_speed = world['top_speed']
        self.ang_velocity = world['ang_velocity']
        self.acceleration = world['acceleration']

        pics = {}
        pics["player"] = pyglet.resource.image('assets/player.png')

