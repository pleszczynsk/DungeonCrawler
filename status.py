__all__ = ['status']

class Status(object):
    def __init__(self):
        self.health = 100
        self.health_chng = None
    def reset(self):
        self.health = 100
        self.health_chng = None
status = Status()