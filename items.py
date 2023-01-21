import pygame
#Block class to generate the playground
class Block:
    def __init__(self, win, pos, width, height, id):
        self.id = id  #0 för horisontell, 1 för vertikal
        self.x = pos[0]
        self.y = pos[1]
        self.win = win
        self.width = width
        self.height = height
        self.color = (150,150,150)
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.win, self.color, self.rect)
        pygame.draw.rect(self.win, (200,200,200), (self.x+2, self.y+2, self.width-4, self.height-4))
    
    def update(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = (self.x, self.y, self.width, self.height)

#KEY class to generate the two keys
class KEY:
    def __init__(self, pos, id):
        self.id = id
        self.isTaken = False
        self.x = pos[0]
        self.y = pos[1]
        self.rect = (self.x, self.y, 30, 30)
        if id == 0:
            self.image = pygame.transform.scale(pygame.image.load(r'blueKey.png'), (30,30))
        else:
            self.image = pygame.transform.scale(pygame.image.load(r'redKey.png'), (30,30))

    def draw(self, win):
        if not self.isTaken:
            win.blit(self.image, (self.x, self.y))

#Door class to generate the two doors
class DOOR:
    def __init__(self, id):
        self.id = id
        self.opened = False
        if id == 0:
            self.x = 50
            self.y = 90
            self.image = pygame.transform.scale(pygame.image.load(r'waterDoor.png'), (40,100))
            self.imageOpen = pygame.transform.scale(pygame.image.load(r'waterDoorOpen.png'), (40,100))
            self.rect = (self.x + 10, self.y, 20, 100)    
        else:
            self.x = 120
            self.y = 90
            self.image = pygame.transform.scale(pygame.image.load(r'fireDoor.png'), (40,100))
            self.imageOpen = pygame.transform.scale(pygame.image.load(r'fireDoorOpen.png'), (40,100))
            self.rect = (self.x + 10, self.y, 20, 100)

    def draw(self, win):
        if self.opened == False:
            win.blit(self.image, (self.x, self.y))
        else:
            win.blit(self.imageOpen, (self.x, self.y))