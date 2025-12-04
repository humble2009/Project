import pygame
import sys
import random
from colors import *

pygame.init()
pygame.display.set_caption("project2")
screen = pygame.display.set_mode((1280, 720))

WIDTH, HEIGHT = 1280, 720
font = pygame.font.SysFont('consolas', 32)
mouse_color = Colors.RED

def generate_squares(a, b):
    result = []
    for i in range(a):
        s = random.randint(10, 100)
        for j in range(b):
            x = random.randint(0, WIDTH - s)
            y = random.randint(0, HEIGHT - s)
            result.append((x, y, s))
    print(result)
    return result

def reset_game():
    global squares, started, start_time, hits, clicks, game_over, end_time
    squares = generate_squares(5, 5)
    started = False
    start_time = None
    hits = 0
    clicks = 0
    game_over = False
    end_time = None

reset_game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x1, y1 = event.pos
            clicks += 1
            for i in squares:
                x, y, s = i
                if x <= x1 <= x + s and y <= y1 <= y + s:
                    squares.remove(i)
                    hits += 1
                    if not started:
                        started = True
                        start_time = pygame.time.get_ticks()
                    break
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_color = Colors.RED
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_color = Colors.WHITE
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_game()

    screen.fill(Colors.GRAY)
    
    # Calculate elapsed time
    if started and not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  #遊戲開始就計時
    elif game_over and end_time is not None:
        elapsed_time = (end_time - start_time) / 1000 # 遊戲結束停止計時
    else:
        elapsed_time = 0  #遊戲沒開始

    if len(squares) == 0 and not game_over:
        game_over = True
        end_time = pygame.time.get_ticks()

    if game_over:
        accuracy = (hits / clicks) * 100 if clicks > 0 else 0
        font_time = font.render(f"Time: {elapsed_time:.2f} sec", True, Colors.WHITE)
        accuracy_time = font.render(f"Accuracy: {accuracy:.2f}% ({hits}/{clicks})", True, Colors.WHITE)
        screen.blit(font_time, (WIDTH / 2 - 100, 100))
        screen.blit(accuracy_time, (WIDTH / 2 - 100, 150))

    if not game_over:
        for x, y, s in squares:
            pygame.draw.rect(screen, Colors.WHITE, (x, y, s, s))

    txt_time = font.render(f"Time: {elapsed_time:.2f} sec", True, Colors.WHITE)
    screen.blit(txt_time, (WIDTH / 2 - 100, 100))

    posx, posy = pygame.mouse.get_pos()
    pygame.draw.line(screen,  mouse_color, (posx - 10, posy), (posx + 10, posy))
    pygame.draw.line(screen, mouse_color, (posx, posy - 10), (posx, posy + 10))

    pygame.mouse.set_visible(False)
    pygame.display.flip()