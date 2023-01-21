import pygame
#class to make a game object to store data and 
class Game:
    def __init__(self):
        self.players = 0
        self.p1ready = False
        self.p2ready = False
        self.blockPos = (200,145)
        self.pos = [[50,500], [100,500]]
        self.blueKeyTaken = False
        self.redKeyTaken = False
        self.doors = [False, False]
        self.ready = True   #if both are connected
    
    def get_player_alive(self, p):
        if p == 0:
            return self.p1alive
        else:
            return self.p2alive
    
    def connected(self):
        return self.ready
    
    def get_player_pos(self, p):
        if p == 0:
            return self.pos[0]
        else:
            return self.pos[1]
    
    def update_player_pos(self, p, pos):
        if p == 0:
            self.pos[0] = pos
        else:
            self.pos[1] = pos
    
    def update_block(self, pos):
        self.blockPos = pos
    
    def player_connected(self, p):
        if p == 0:
            self.p1ready = True
        else:
            self.p2ready = True

    def player_disconnected(self, p):
        if p == 0:
            self.p1ready = False
        else:
            self.p2ready = False
