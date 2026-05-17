import pygame 
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
green = (0, 255, 0)

dis_w = 800
dis_h = 600
dis = pygame.display.set_mode((dis_w, dis_h))

pygame.display.set_caption("Змейка")

game_over = False
close_game = False  # Добавляем флаг для выхода после проигрыша
snake_block = 10
x1 = dis_w / 2
y1 = dis_h / 2
x1_change = 0
y1_change = 0 
snake_speed = 15
clock = pygame.time.Clock()
foodx = round(random.randrange(0, dis_w - snake_block) / 10.0) * 10.0
foody = round(random.randrange(0, dis_h - snake_block) / 10.0) * 10.0
snake_L = []
len_of_snake = 1

font_style = pygame.font.SysFont(None, 50)
font_style_small = pygame.font.SysFont(None, 35)

def our_snake(snake_block, snake_L):
    for x in snake_L:
        pygame.draw.rect(dis, purple, [x[0], x[1], snake_block, snake_block])  # Исправлено: pygame.draw.rect

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_w/6, dis_h/3])

def show_score(score):
    score_text = font_style_small.render(f"Счёт: {score}", True, black)
    dis.blit(score_text, [10, 10])

while not close_game:  # Основной цикл игры с перезапуском
    game_over = False
    # Сброс переменных при новом запуске
    x1 = dis_w / 2
    y1 = dis_h / 2
    x1_change = 0
    y1_change = 0
    snake_L = []
    len_of_snake = 1
    foodx = round(random.randrange(0, dis_w - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_h - snake_block) / 10.0) * 10.0
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                close_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:  # Запрещаем движение назад
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    x1_change = 0
                    y1_change = snake_block
        
        if x1 >= dis_w or x1 < 0 or y1 >= dis_h or y1 < 0:
            game_over = True
        
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        
        # Рисуем еду
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        
        # Обновляем змейку
        snake_head = [x1, y1]
        snake_L.append(snake_head)
        if len(snake_L) > len_of_snake:
            del snake_L[0]
        
        # Проверка столкновения с собой
        for segment in snake_L[:-1]:
            if segment == snake_head:
                game_over = True
        
        our_snake(snake_block, snake_L)
        
        # Проверка съедания еды
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_w - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_h - snake_block) / 10.0) * 10.0
            len_of_snake += 1
            snake_speed += 0.5  # Увеличиваем скорость с каждым съеденным кусочком
        
        show_score(len_of_snake - 1)
        pygame.display.update()
        clock.tick(snake_speed)
    
    # Вывод сообщения о проигрыше
    if not close_game:
        dis.fill(white)
        message(f"Ты проиграл! Счёт: {len_of_snake - 1}", black)
        message("Нажми C для новой игры или Q для выхода", purple)
        pygame.display.update()
        
        # Ожидание выбора игрока
        waiting = True
        while waiting and not close_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close_game = True
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        waiting = False  # Новая игра
                        snake_speed = 15  # Сброс скорости
                    elif event.key == pygame.K_q:
                        close_game = True
                        waiting = False

pygame.quit()
quit()