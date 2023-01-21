import time
from network import Network
import pygame
from player import Player
from items import *

WIDTH = 800
HEIGHT = 600
FPS = 60
BLOCKS = []
isJump = False
jumpCount = 10
hit = False
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
movine_block = Block(screen,(150,150), 40, 40, 1)
blueKey = KEY([100,410], 0)
redKey = KEY([300,530],1)
blueDoor = DOOR(0)
redDoor = DOOR(1)

#Generate the blocks for the playground and store it in BLOCKS array
def make_Blocks(win):
    BLOCKS.append(Block(win, (10,10), 38*20+10, 20, 0)) 
    BLOCKS.append(Block(win, (10,HEIGHT-30), 38*20+10, 20, 0)) 
    BLOCKS.append(Block(win, (10,30), 20, 20*27, 1)) 
    BLOCKS.append(Block(win, (WIDTH-40,30), 20, 20*27, 1)) 
    BLOCKS.append(Block(win, (30,HEIGHT-150), 25*20+10, 20, 0)) 
    BLOCKS.append(Block(win, (10+20*6,HEIGHT-270), 25*20+10, 20, 0)) 
    BLOCKS.append(Block(win, (30,HEIGHT-410), 25*20+10, 20, 0))

#Draw each block in BLOCKS array
def draw_Blocks():
    for block in BLOCKS:
        block.draw()

#The main function to redraw the window
def redrawWindow(win, player, player2, blueKey, redKey):
    win.fill((0,0,0))
    blueKey.draw(win)
    redKey.draw(win)
    draw_Blocks()
    blueDoor.draw(win)
    redDoor.draw(win)
    player.draw(win)
    player2.draw(win)
    movine_block.draw()
    pygame.display.update()

#Function to make the block fall to the ground or on top of other player.
def fall_block(b, p, p2):
    b.y += 3
    hit = False
    for block in BLOCKS:
        if pygame.Rect(b).colliderect(pygame.Rect(block)):
            b.y -= 3
            hit = True
            break
    if pygame.Rect(p.rect).colliderect(pygame.Rect(b)) and not hit:
        b.y -= 3
    elif pygame.Rect(p2.rect).colliderect(pygame.Rect(b)) and not hit:
        b.y -= 3

#Handle player movement at each iteration
def handle_player_movement(win, p, p2):
    global isJump, jumpCount, hit, movine_block
    keys = pygame.key.get_pressed()
    #Have to check muliple things and collisions when moved to the left
    if keys[pygame.K_LEFT]:
        p.x -= p.vel
        counter = 0
        p.update()
        #Check player collision with blocks
        for block in BLOCKS:
            if pygame.Rect(p.rect).colliderect(pygame.Rect(block)) and counter == 0:
                p.x += p.vel
                counter += 1
                break
        #Check player collision with the moving block
        if pygame.Rect(p.rect).colliderect(pygame.Rect(movine_block)):
            movine_block.update((movine_block.x - p.vel, movine_block.y))
            #Check if the moving block is colliding with other blocks/player
            for block in BLOCKS:
                if pygame.Rect(movine_block).colliderect(pygame.Rect(block)) and block.id == 1 and counter == 0:
                    movine_block.update((movine_block.x + p.vel, movine_block.y))
                    p.x += p.vel
                    counter += 1
                    break
                elif pygame.Rect(movine_block).colliderect(pygame.Rect(p2.rect)) and counter == 0:
                    movine_block.update((movine_block.x + p.vel, movine_block.y))
                    p.x += p.vel
                    counter += 1
                    break
        #Check if player collide with other player
        if pygame.Rect(p.rect).colliderect(pygame.Rect(p2.rect)) and counter == 0:
            p.x += p.vel
            counter += 1
    #Same check for the right movement
    if keys[pygame.K_RIGHT]:
        p.x += p.vel
        counter = 0
        p.update()
        for block in BLOCKS:
            if pygame.Rect(p.rect).colliderect(pygame.Rect(block)) and counter == 0:
                p.x -= p.vel
                counter += 1
                break
        if pygame.Rect(p.rect).colliderect(pygame.Rect(movine_block)):
            movine_block.update((movine_block.x + p.vel, movine_block.y))
            for block in BLOCKS:
                if pygame.Rect(movine_block).colliderect(pygame.Rect(block)) and block.id == 1 and counter == 0:
                    movine_block.update((movine_block.x - p.vel, movine_block.y))
                    p.x -= p.vel
                    counter += 1
                    break
                elif pygame.Rect(movine_block).colliderect(pygame.Rect(p2.rect)) and counter == 0:
                    movine_block.update((movine_block.x - p.vel, movine_block.y))
                    p.x -= p.vel
                    counter += 1
                    break
            
        if pygame.Rect(p.rect).colliderect(pygame.Rect(p2.rect)) and counter == 0:
            p.x -= p.vel
            counter += 1
    #Check if player collected bluekey
    if pygame.Rect(p.rect).colliderect(pygame.Rect(blueKey.rect)) and p.id == 0:
        blueKey.isTaken = True
        p.hasKey = True
    #check if player collected redkey
    if pygame.Rect(p.rect).colliderect(pygame.Rect(redKey.rect)) and p.id == 1:
        redKey.isTaken = True
        p.hasKey = True
    #Check if player is at the bluedoor
    if pygame.Rect(p.rect).colliderect(pygame.Rect(blueDoor.rect)) and p.id == 0 and p.hasKey == True:
        blueDoor.opened = True
    #check if player is at the reddoor 
    if pygame.Rect(p.rect).colliderect(pygame.Rect(redDoor.rect)) and p.id == 1 and p.hasKey == True:
        redDoor.opened = True   

    #Check key up for jumping
    if keys[pygame.K_UP] and not isJump and not hit:
        isJump = True
        hit = False
    #Jumping code
    if isJump:
        if not hit:
            neg = 1
            if jumpCount < 0:
                neg = -1
            p.y -= (jumpCount ** 2) * 0.4 * neg
            p.update()
            for block in BLOCKS:
                if pygame.Rect(p.rect).colliderect(pygame.Rect(block)):
                    p.y += (jumpCount ** 2) * 0.5 * neg
                    hit = True
                    break
            if pygame.Rect(p.rect).colliderect(pygame.Rect(p2.rect)):
                p.y += (jumpCount ** 2) * 0.5 * neg
                hit = True
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    
    #Make the player fall
    p.y +=3
    p.update()
    player_hit = False
    for block in BLOCKS:
        if pygame.Rect(p.rect).colliderect(pygame.Rect(block)):
            p.y -= 3
            hit = False
            player_hit = True
            break
        elif pygame.Rect(p.rect).colliderect(pygame.Rect(movine_block)):
            p.y -= 3
            hit = False
            player_hit = True
            break
    #check if player land on other player
    if pygame.Rect(p.rect).colliderect(pygame.Rect(p2.rect)) and not player_hit:
        p.y -= p.vel
        hit = False
    
#Drawing waiting screen for the both players to join
def waiting_screen(win):
    win.fill((0,0,0))
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render('Waiting for the other player to connect...', False, (255,255,255))
    win.blit(text, (WIDTH/2 - 300, HEIGHT/2))
    pygame.display.update()

#Drawing winning screen at the end
def winning_screen(win):
    win.fill((0,0,0))
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render('Congratulations, you won!', False, (255,255,255))
    win.blit(text, (WIDTH/2 - 200, HEIGHT/2))
    pygame.display.update()



#Main function the create all the needed variables and object and start game loop
def main():
    clock = pygame.time.Clock()
    n = Network()
    make_Blocks(screen)
    player = int(n.get_id())
    print("YOU ARE PLAYER:", player)
    p = Player(player, (0,0))
    player2 = 0
    if player == 0:
        player2 = 1
    else:
        player2 = 0
    p2 = Player(player2, (0,0))
    run = True
    while run:
        clock.tick(FPS)
        #try to get game info
        try:
            req = {
                "request" : "get",
                "data" : None
            }
            game = n.send(req) #The game store the info of the game the has been receieved from the server
        except:
            run = False
            print("Couldn't get the game.")
            break
        
        #If a player disconnects
        if game['state'] == False:
            run = False
            pygame.quit()
        #Wait for both players to join
        if not (game["p1ready"] and game["p2ready"]):
            waiting_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    n.send({"request":"DISCONNECT", "data":None})
                    pygame.quit()
            continue

        if(p.id == 0):
            p.update_pos(game["player1"])
            p2.update_pos(game["player2"])
            p.hasKey = game["keys"][0]
            p2.hasKey = game["keys"][1]
        else:
            p.update_pos(game["player2"])
            p2.update_pos(game["player1"])
            p.hasKey = game["keys"][1]
            p2.hasKey = game["keys"][0]
        movine_block.update(game["block"])
        blueDoor.opened = game["doors"][0]
        redDoor.opened = game["doors"][1]

        #Check for winning
        if game["doors"] == [True, True]:
            winning_screen(screen)
            time.sleep(3)
            run = False
            n.send({"request":"DISCONNECT", "data":None})
            pygame.quit()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                n.send({"request":"DISCONNECT", "data":None})
                pygame.quit()
        blueKey.isTaken = game["keys"][0]
        redKey.isTaken = game["keys"][1]
        
        handle_player_movement(screen, p, p2)
        
        fall_block(movine_block, p, p2)
        p.update()

        req = {
            'request' : 'update', #För att informera servern om att uppdatera
            'data' : p.get_pos(), #Spelarens nya position
            'block' : (movine_block.x,movine_block.y), #Blockets position
            'keys' : [blueKey.isTaken, redKey.isTaken], #Nycklarnas status
            'doors' : [blueDoor.opened, redDoor.opened] #Dörrarnas status
        }
        n.send(req) #Send back the collected info about the game at the end of each iteration to the server to store the changes
        redrawWindow(screen, p, p2, blueKey, redKey)

main()