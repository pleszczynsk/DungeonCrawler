import cocos
from cocos.director import director
import cocos.collision_model as colmod
import cocos.euclid as euc
from cocos.scene import Scene

import pyglet
from pyglet.window import key
from pyglet.gl import *


import random
import math

__all__ = ['get_newgame']

consts = {
    "game_area":{
        "width":800,
        "height": 600,
        "r": 8.0,
        "wall_scale_min": 0.75,
         "wall_scale_max": 2.25,
        "top_speed": 100.0,
        "acceleration": 85.0,
        "ang_velocity": 240.0,
        "bindings":{
            key.LEFT: 'left',
            key.RIGHT: 'right',
            key.UP: 'up'
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

x_window, y_window = director.get_window_size()
scale_x = x_window/consts["game_area"]["width"]
scale_y = y_window/consts["game_area"]["height"]

def world_view(v):
    return v.x *scale_x, v.y * scale_y

class Player(cocos.sprite.Sprite):
    palette ={}
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
        world = consts['game_area']
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
        pics["wall"] = pyglet.resource.image('assets/wall.png')
        self.pics = pics

        cell_size = self.rPlayer * self.wall_scale_max * 2.0 * 1.25
        self.collisions = colmod.CollisionManagerGrid(0.0,self.width,
                                                      0.0,self.height,
                                                      cell_size, cell_size)
        self.bindings = world['bindings']
        buttons = {}
        for i in self.bindings:
            buttons[self.bindings[i]] = 0
        self.buttons = buttons

        self.toRemove = set()
        self.schedule(self.update)
        self.empty_level()
        self.level_launch()

    def level_launch(self):
        self.generate_level()

    def empty_level(self):
        for node in self.get_children():
            self.remove(node)
        assert len(self.children) == 0
        self.player = None
        self.toRemove.clear()
        self.impulse_dir = euc.Vector2(0.0, 1.0)

    def generate_level(self):
        wall_num = 10
        min_separation_rel = 3.0

        width = self.width
        height = self.height
        rPlayer = self.rPlayer
        min_separation = min_separation_rel * rPlayer
        wall_scale_min = self.wall_scale_min
        wall_scale_max = self.wall_scale_max
        pics = self.pics
        z = 0

        cx,cy = (0.5 * width, 0.5 * height)
        self.player = Player(cx,cy,rPlayer, 'player', pics['player'])
        self.collisions.add(self.player)

        for i in range(wall_num):
            s = random.random()
            r = rPlayer * (wall_scale_min *s + wall_scale_max * (1.0 -s))
            wall = Player(cx,cy,r,'wall',pics['wall'])
            count = 0
            while count < 100:
                cx = r + random.random() * (width - 2.0 * r)
                cy = r + random.random() * (height - 2.0 * r)
                wall.update_center(euc.Vector2(cx,cy))
                if self.collisions.any_near(wall, min_separation) is None:
                    self.add(wall, z=z)
                    z += 1
                    self.collisions.add(wall)
                    break
                count += 1
        self.add(self.player, z=z)
        z += 1

    def update(self,dt):
        self.collisions.clear()
        for z, node in self.children:
            self.collisions.add(node)

        buttons = self.buttons
        ma = buttons['right'] - buttons['left']
        if ma != 0:
            self.player.rotation +=ma * dt *self.ang_velocity
            a = math.radians(self.player.rotation)
            self.impulse_dir = euc.Vector2(math.sin(a), math.cos(a))

        new_velocity = self.player.vel
        mv = buttons['up']
        nv = new_velocity.magnitude()
        if mv != 0:
            new_velocity += dt * mv * self.acceleration * self.impulse_dir
            if nv > self.top_speed:
                new_velocity *= self.top_speed / nv
        if mv == 0:
            new_velocity = euc.Vector2(0.0, 0.0)

        player_position = self.player.cshape.center
        new_position = player_position
        r = self.player.cshape.r

        while dt > 1.e-6:
            new_position = player_position + dt * new_velocity
            dt_minus = dt
            if new_position.x < r or new_position.x > (self.width - r) or new_position.y < r or new_position.y > (self.height - r):
                new_velocity = euc.Vector2(0.0,0.0)
            dt -= dt_minus

        self.player.vel = new_velocity
        self.player.update_center(new_position)

        for node in self.toRemove:
            self.remove(node)
        self.toRemove.clear()

    def on_key_press(self, k, m):
        binds = self.bindings
        if k in binds:
            self.buttons[binds[k]] = 1
            return True
        return False

    def on_key_release(self, k, m):
        binds = self.bindings
        if k in binds:
            self.buttons[binds[k]] = 0
            return True
        return False

def get_newgame():
    scene = Scene()
    palette = consts['view']['palette']
    Player.palette = palette
    r, g, b = palette['bg']
    playview = World()
    scene.add(playview, z = 0)
    return scene