import cocos
import cocos.collision_model as colmod
import cocos.euclid as euc
from cocos.scene import Scene

from cocos.layer import *
from cocos.text import *

import pyglet
from pyglet.window import key
from pyglet.gl import *

import random
import math
import game
from status import status

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
            key.UP: 'up',
            key.DOWN: 'down',
            key.ESCAPE: 'escape'
        }
    },
    "view":{
        "palette":{
            'bg': (214, 197, 167),
            'player': (255, 255, 255),
            'wall': (247, 148, 29),
        }
    }
}

x_window, y_window = director.get_window_size()
scale_x = x_window/consts["game_area"]["width"]
scale_y = y_window/consts["game_area"]["height"]

def world_view(v):
    return v.x *scale_x, v.y * scale_y

class Player(cocos.sprite.Sprite): #Entity class
    palette ={}
    def __init__(self, cx, cy, radius, btype, img, vel = None):
        super(Player,self).__init__(img)
        self.scale = (radius *1.05) * scale_x/(self.image.width/2.0)
        self.btype = btype
        self.cshape = colmod.CircleShape(euc.Vector2(cx,cy), radius)
        self.update_center(self.cshape.center)
        if vel is None:
            vel = euc.Vector2(0.0,0.0)
        self.vel = vel
    def update_center(self, cshape_center):
        self.position = world_view(cshape_center)
        self.cshape.center = cshape_center

class HUD(Layer): #Interface
    def __init__(self):
        w,h = director.get_window_size()
        super(HUD, self).__init__()
        self.add(ColorLayer(32, 32, 32, 32, width=w, height=48), z=-1)
        self.health = Label('Zdrowie:',font_size = 20, color = (255,255,255,200),
                            anchor_x = 'center', anchor_y = 'bottom')
        self.stamina = Label('Kondycja:', font_size=20, color=(255, 255, 255, 200),
                            anchor_x='center', anchor_y='bottom')
        self.level = Label('Poziom:', font_size=20, color=(255, 255, 255, 200),
                            anchor_x='center', anchor_y='bottom')
        self.health.position = (w-(1/2*w),h-(h-10))
        self.stamina.position = (1/5*w,h-(h-10))
        self.level.position = w-(1/4*w),h-(h-10)
        self.add(self.health)
        self.add(self.stamina)
        self.add(self.level)
    def draw(self):
        super(HUD,self).draw()
        self.health.element.text = 'Zdrowie:%d' % status.health
        self.stamina.element.text = 'Kondycja:%d' % status.stamina
        self.level.element.text = 'Poziom:%d' % status.level
    if status.health_chng:
        status.health_chng.draw()

class drawHUD(Layer):
    def __init__(self):
        super(drawHUD,self).__init__()
        self.add(HUD())
###############LEVEL GENERATION###############
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
        pics["enemy"] = pyglet.resource.image('assets/enemy.png')
        pics["health"] = pyglet.resource.image('assets/health.png')
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
        wall_num = 50
        enemy_num = 10 * status.level
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

        if status.level % 5 == 0: #Health placement
            r = 7
            enemy = Player(cx, cy, r, 'health', pics['health'])
            count = 0
            while count < 100:
                cx = r + random.random() * (width - 2.0 * r)
                cy = r + random.random() * (height - 2.0 * r)
                enemy.update_center(euc.Vector2(cx, cy))
                if self.collisions.any_near(enemy, min_separation) is None:
                    self.add(enemy, z=z)
                    z += 1
                    self.collisions.add(enemy)
                    break
                count += 1

        for i in range(wall_num): #Bomb craters placement
            s = random.random()
            r = rPlayer * (wall_scale_min *s + wall_scale_max * (3.0 -s))
            wall = Player(cx,cy,r,'wall',pics['wall'])
            count = 0
            while count < 100:
                cx = r + random.random() * (width - 2.0 * r)
                cy = r + random.random() * (height - 2.0 * r)
                wall.update_center(euc.Vector2(cx,cy))
                if self.collisions.any_near(wall, min_separation) is None:
                    self.add(wall, z=z)
                    wall.rotation  += random.random() * 360
                    z += 1
                    self.collisions.add(wall)
                    break
                count += 1

        for i in range(enemy_num): #Enemy placement
            r = 7
            enemy = Player(cx,cy,r,'enemy',pics['enemy'])
            count = 0
            while count < 100:
                cx = r + random.random() * (width - 2.0 * r)
                cy = r + random.random() * (height - 2.0 * r)
                enemy.update_center(euc.Vector2(cx,cy))
                if self.collisions.any_near(enemy, min_separation - 0.5 *status.level) is None:
                    self.add(enemy, z=z)
                    z += 1
                    self.collisions.add(enemy)
                    break
                count += 1

        self.add(self.player, z=z)
        z += 1

    def update(self,dt): #Updates the scene
        self.collisions.clear()
        for z, node in self.children:
            self.collisions.add(node)
        buttons = self.buttons
###############PLAYER CONTROLS & COLLISIONS###############
        ma = buttons['right'] - buttons['left']
        if ma != 0:
            self.player.rotation += ma * dt *self.ang_velocity
            a = math.radians(self.player.rotation)
            self.impulse_dir = euc.Vector2(math.sin(a), math.cos(a))

        new_velocity = self.player.vel
        mv = buttons['up']
        mvdn = buttons['down']
        nv = new_velocity.magnitude()

        if mvdn != 0: #reverse movement
            new_velocity += mvdn * self.acceleration * -(self.impulse_dir)
            new_velocity *= (status.stamina/100.0)
            if status.stamina > 10:
                status.stamina -= 0.2
            if nv > self.top_speed:
                new_velocity *= self.top_speed / nv
        if mv != 0: #forward movement
            new_velocity += mv * self.acceleration * self.impulse_dir
            new_velocity *= (status.stamina / 100.0)
            if status.stamina > 10:
                status.stamina -= 0.2
            if nv > self.top_speed:
                new_velocity *= self.top_speed / nv
        if mv == 0 and mvdn == 0: #stop moving
            new_velocity = euc.Vector2(0.0, 0.0)
        player_position = self.player.cshape.center
        r = self.player.cshape.r

        while dt > 1.e-6:
            new_position = player_position + dt * new_velocity
            dt_minus = dt
            if new_position.x < r or new_position.x > (self.width - r) or new_position.y < r or new_position.y > (self.height - r):
                status.level += 1
                director.push(get_newgame())
            for colliding in self.collisions.iter_colliding(self.player):
                typecoll = colliding.btype
                if typecoll == 'wall':
                    new_velocity = -new_velocity
                elif typecoll == 'enemy':
                    status.health -= 0.1*status.level #Enemy damage multiplies each level
                elif typecoll == 'health':
                    status.health = 100

            dt -= dt_minus
            if status.stamina <= 100 and mvdn == 0 and mv == 0:
                status.stamina += 1
        self.player.vel = new_velocity
        self.player.update_center(new_position)
#key bindings
        if buttons['escape'] != 0 or status.health <= 0.0:
            status.reset() #player stats, level reset to defaults
            scene = cocos.scene.Scene()
            scene.add(game.MultiplexLayer(
                game.Main_Menu(),
                game.Options_Menu()
            ))
            director.run(scene)

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

def get_newgame(): #generating a new game screen
    scene = Scene()
    hud = HUD()
    palette = consts['view']['palette']
    Player.palette = palette
    r, g, b = palette['bg']
    scene.add(cocos.layer.ColorLayer(r, g, b, 255), z=-1)
    playview = World()
    scene.add(playview, z = 0)
    scene.add(hud, z=3, name='hud')
    return scene