###############LEVEL&PLAYER STATUS###############
__all__ = ['status']
class Status(object):
    def __init__(self):
        self.health = 100
        self.level = 1
        self.health_chng = None
    def reset(self):
        self.health = 100
        self.level = 1
        self.health_chng = None
status = Status()