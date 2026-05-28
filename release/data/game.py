import socket
import pygame
import json
import time
import random



def run(ip):
    
    print(ip)
    port = 60002


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    
    trash = s.recv(1024 * 8).decode()
    
    trash = json.loads(trash)
    # print(type(trash), trash)
    name = f'player {random.randint(0, 10000)}'


    WIDTH = 800
    HEIGHT = 800
    FPS = 120

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    color_list = (BLACK, RED, GREEN, BLUE)
    color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    f = pygame.font.Font(None, 36)


    x = random.randint(40, 760)
    y = random.randint(40, 760)

    x_speed = 0
    y_speed = 0

    const_speed = 2
    m = 20

    U = 1
    speed = const_speed
    l = U
    running = True
    first_frame = True
    while running:
        start = time.time()
        
    # movement ========================================================================
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    y_speed = speed
                if event.key == pygame.K_UP:
                    y_speed = -speed                     
                if event.key == pygame.K_RIGHT:
                    x_speed = speed
                if event.key == pygame.K_LEFT:
                    x_speed = -speed
                # if event.key == pygame.K_p:
                #     m += 1
                # if event.key == pygame.K_l:
                #     m -= 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    y_speed = 0
                if event.key == pygame.K_UP:
                    y_speed = 0
                if event.key == pygame.K_RIGHT:
                    x_speed = 0
                if event.key == pygame.K_LEFT:
                    x_speed = 0

        if x >= WIDTH - 1.5 * m and x_speed > 0:
            x_speed = 0
        if x <= 0 - 0.5 * m and x_speed < 0:
            x_speed = 0
            
        if y >= WIDTH - 1.5 * m and y_speed > 0:
            y_speed = 0
        if y <= 0 - 0.5 * m and y_speed < 0:
            y_speed = 0
        
        x += x_speed
        y += y_speed
        
        
    # ================================================================================

    # колизия
        # player = pygame.Rect(x-(2**(-1/2))*m, y-(2**(-1/2))*m, 20, 20)
        player = pygame.Rect(x+m/2, y+m/2, m, m)
        
        for i in range(len(trash)):
            # print(len(trash))
            if player.collidepoint(trash[i][0], trash[i][1]):
                trash.pop(i) 
                m += 1
                break
                
    
    

    # net ============================================================================
        if l == U:
            l = 0
            data1 = {
                'name' : name,
                'x' : x,
                'y' : y,
                'm' : m,
                'color': color
            }
            data1 = json.dumps(data1)
            s.send(data1.encode())
            data = s.recv(1024).decode()
            
            if data == 'close':
                exit('FINISH')
            
            data = json.loads(data)
        l += 1
    # ================================================================================

    # eat
        for i in data:
            gamer = pygame.Rect(data[i]['cord'][0] + data[i]['stats'][0]/2, data[i]['cord'][1] + data[i]['stats'][0]/2,
                            data[i]['stats'][0], data[i]['stats'][0])
            if player.colliderect(gamer):
                if data[i]['stats'][0] > m: # смэрт

                    x = 20000
                    y = 20000
                    speed = 0
                    print('death')
        # print(data)
        k = 0
        for i in data:
            if data[i]['cord'][0] == data[i]['cord'][0] == 20000:
                k += 1
        if k == len(data) - 1 and first_frame == False and len(data) != 1:
            print('We have a winer!')
            input()
    
    # draw ===========================================================================
        screen.fill(WHITE)
        
        for i in range(len(trash)):
            # pygame.draw.circle(screen, BLACK, (trash[i][0], trash[i][1]), 5)
            i = pygame.Rect(trash[i][0], trash[i][1], 5, 5)
            pygame.draw.rect(screen, BLACK, i)
            
        for i in data:
            gamer = pygame.Rect(data[i]['cord'][0] + data[i]['stats'][0]/2, data[i]['cord'][1] + data[i]['stats'][0]/2,
                            data[i]['stats'][0], data[i]['stats'][0])
            # pygame.draw.circle(screen, data[i]['stats'][1], (data[i]['cord'][0], data[i]['cord'][1]), data[i]['stats'][0])
            pygame.draw.rect(screen, data[i]['stats'][1], gamer)
            
        # pygame.draw.rect(screen, RED, rect=player)
        text = f.render(str(m), True,
                  (0, 0, 0))  
        
        screen.blit(text, (2, 2))
        
        
        
        pygame.display.update()
        clock.tick(FPS)
        first_frame = False
        
        finish = time.time()
        try:
            fps = int(1/(finish-start))
        except:
            fps = int(1/(finish-start + 0.001))
            
        print(f'FPS: {fps}')
        speed = const_speed * (FPS/fps)
    # ================================================================================
    pygame.quit()
    

if __name__ == '__main__':
    run(ip = socket.gethostbyname(socket.gethostname()))
    # run(ip = input())
