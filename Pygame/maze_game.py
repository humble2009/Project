import pygame, sys , os, random, pickle
from colors import *


W,H = 1200, 800
pygame.init()
pygame.display.set_caption('PG05')
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

font = pygame.font.SysFont('consolas', 32)

draw_red = False
started = False
start_t = None
game_over = False
end_t = None
remaining_time = 30
line_size = 30
dx, dy = 0, 0
gm = 'edit'
redx, redy = 10, 400
r = pygame.Rect(redx, redy, 20, 20)
line_size = 30
#level1_obstacle = {(90, 210), (90, 270), (90, 180), (90, 150), (90, 240)}
#level1_target = {(150, 210)}
now_level = 0

obstacles = set()
targets = set()

def load():
    if os.path.isfile(f'map{now_level+1}.bin'):
        with open(f'map{now_level+1}.bin', 'rb') as f:
            return pickle.load(f)
    
    return [(set(), set(), (redx, redy))]

def save():
    global redx, redy, obstacles, targets
    game_map = [(obstacles, targets, (redx, redy))]
    with open(f'map{now_level+1}.bin', 'wb') as f:
        pickle.dump(game_map, f)
        print(f'map{now_level+1}.bin存了')

def reset_game():
    global game_over, remaining_time, dx, dy, started, r, redx, redy
    game_over = True
    remaining_time = 30
    dx, dy = 0, 0
    started = False
    r = pygame.Rect(redx, redy, 20, 20)
    gm == 'edit'

loaded_map = load()
obstacles, targets , (redx,redy)= loaded_map[0]
r.topleft = (redx, redy)
print(f'map{now_level+1}.bin載了')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                gm = 'play'
                if not started:
                    started = True
                    start_t = pygame.time.get_ticks()
                    remaining_time = 30
                # 方向鍵按下時才設定移動
                if event.key == pygame.K_UP:
                    dx, dy = 0, -5
                elif event.key == pygame.K_DOWN:
                    dx, dy = 0, 5
                elif event.key == pygame.K_LEFT:
                    dx, dy = -5, 0
                elif event.key == pygame.K_RIGHT:
                    dx, dy = 5, 0

            if event.key == pygame.K_e:
                gm = 'edit'              
                reset_game()
            
            if gm == 'edit':
                if event.key == pygame.K_l:
                    loaded_map = load()
                    obstacles, targets , r.topleft= loaded_map[0]
                    print(f'map{now_level+1}.bin載了')
            
                if event.key == pygame.K_s:
                    save()
            
                if event.key == pygame.K_DELETE:
                    obstacles.clear()
                    targets.clear()
                    draw_red = False
                    r = pygame.Rect(redx, redy, 20, 20)
        
        if gm == 'edit':
            mouse = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()
            mx, my = pygame.mouse.get_pos()
            gx, gy = (mx // line_size) * line_size, (my // line_size) * line_size #計算網格
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mx, my = pygame.mouse.get_pos()
                gx, gy = (mx // line_size) * line_size, (my // line_size) * line_size
                
                if keys[pygame.K_RCTRL]:
                    draw_red = True
                    redx, redy = gx, gy
                    r.topleft = (redx, redy)

                elif not (keys[pygame.K_LSHIFT] or keys[pygame.K_LALT] or keys[pygame.K_g]):
                    if (gx, gy) in obstacles:
                        obstacles.remove((gx, gy))
                    else:
                        obstacles.add((gx, gy))
                
            if keys[pygame.K_LCTRL] and mouse[0]:
                if (gx, gy) in targets:
                    targets.remove((gx, gy))
                if (gx, gy) in obstacles:
                    obstacles.remove((gx, gy))
    
    if gm == 'edit': #判斷網格
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:  
            mx, my = pygame.mouse.get_pos()
            gx, gy = (mx // line_size) * line_size, (my // line_size) * line_size
            if keys[pygame.K_LSHIFT]:
                obstacles.add((gx, gy))
            elif keys[pygame.K_LALT]:
                targets.add((gx, gy))
            elif keys[pygame.K_g]:
                if (gx, gy) in targets:
                    targets.remove((gx, gy))
    
    if gm == 'play':
        old_pos = r.topleft #先儲存上一次的位置
        r.move_ip(dx,dy) #移動
        if not(0<r.x < W - r.width and 0<r.y<H - r.height): #防止出畫面
            r.topleft = old_pos
    
        for wx,wy in obstacles: #撞牆
            wall_rect = pygame.Rect(wx, wy, line_size, line_size)
            if r.colliderect(wall_rect):
                r.topleft = old_pos
                break
        
        for tx, ty in targets: #碰終點
            target_rect = pygame.Rect(tx, ty, line_size, line_size)
            if r.colliderect(target_rect):
                now_level += 1
                if now_level >= 5: #換回第一關
                    now_level = 0
                print(now_level + 1)
                loaded_map = load()
                obstacles, targets , r.topleft= loaded_map[0]
                print(f'map{now_level+1}.bin載了')

                reset_game()

    screen.fill((10,10,10))
    
    if started:
        elasped = (pygame.time.get_ticks() - start_t) / 1000 #經過的時間
        remaining_time = 30 - elasped #開始扣
        if remaining_time <= 0: #時間到
            reset_game()
    
    #畫方塊
    for x, y in obstacles:
        pygame.draw.rect(screen, Colors.GRAY, (x, y, line_size, line_size))
    for x, y in targets:
        pygame.draw.rect(screen, Colors.GREEN, (x, y, line_size, line_size))
    
    #資訊
    time_txt = font.render(f'{remaining_time:.2f}', True, Colors.Light_Gold)
    level_txt = font.render(f"level:{now_level+1}", True, Colors.Light_Gold)
    screen.blit(time_txt, (800,50))
    screen.blit(level_txt, (1000,50))
    pygame.draw.rect(screen, Colors.RED, r)
    
    pygame.display.flip()
    clock.tick(60)