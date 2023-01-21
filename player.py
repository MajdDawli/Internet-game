import pygame
#class to make player object to store its data and have usefull functions
class Player:
    def __init__(self, id, pos):
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.width = 20
        self.height = 40
        self.rect = (self.x, self.y, self.width, self.height)
        self.vel = 3
        self.hasKey = False
        if id == 0:
            self.image = pygame.transform.scale(pygame.image.load(r'watergirl.png'), (self.width, self.height))
            self.imageWithKey = pygame.transform.scale(pygame.image.load(r'blueWithKey.png'), (self.width, self.height))
        else:
            self.image = pygame.transform.scale(pygame.image.load(r'fireboy.png'), (self.width, self.height))
            self.imageWithKey = pygame.transform.scale(pygame.image.load(r'redWithKey.png'), (self.width, self.height))
    
    def draw(self, win):
        if self.hasKey == False:
            win.blit(self.image, (self.x, self.y))
        else:
            win.blit(self.imageWithKey, (self.x, self.y))

    def update(self):    
        self.rect = (self.x, self.y, self.width, self.height)
    
    def update_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = (self.x, self.y, self.width, self.height)
    
    def get_pos(self):
        return (self.x, self.y)