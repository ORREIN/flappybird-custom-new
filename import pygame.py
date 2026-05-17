import pygame
import random
import sys

# Автор: Завод Птица
# Игра: Flappy Bird

pygame.init()

# Настройки экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Завод птица - Cherry team")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Шрифты
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 60)

# Игровые переменные
GRAVITY = 0.5
JUMP_STRENGTH = -9
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3
BIRD_SIZE = 30

class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.size = BIRD_SIZE
        
    def jump(self):
        self.velocity = JUMP_STRENGTH
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
    def draw(self):
        # Рисуем птицу (жёлтый прямоугольник с глазом и клювом)
        pygame.draw.rect(screen, YELLOW, [self.x, self.y, self.size, self.size])
        # Глаз
        pygame.draw.circle(screen, BLACK, (self.x + 20, self.y + 10), 4)
        pygame.draw.circle(screen, WHITE, (self.x + 18, self.y + 8), 2)
        # Клюв
        pygame.draw.polygon(screen, ORANGE, [(self.x + 30, self.y + 12), (self.x + 38, self.y + 16), (self.x + 30, self.y + 20)])
        # Крыло
        pygame.draw.ellipse(screen, ORANGE, [self.x + 5, self.y + 15, 20, 15])
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self):
        # Верхняя труба
        pygame.draw.rect(screen, GREEN, [self.x, 0, PIPE_WIDTH, self.height])
        pygame.draw.rect(screen, DARK_GREEN, [self.x, self.height - 30, PIPE_WIDTH, 30])
        # Нижняя труба
        pygame.draw.rect(screen, GREEN, [self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP])
        pygame.draw.rect(screen, DARK_GREEN, [self.x, self.height + PIPE_GAP, PIPE_WIDTH, 30])
        
    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)
        return top_rect, bottom_rect

def show_score(score):
    score_text = font.render(f"Счёт: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def show_game_over(score, best_score):
    screen.fill(BLUE)
    game_over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Счёт: {score}", True, WHITE)
    best_text = font.render(f"Рекорд: {best_score}", True, WHITE)
    restart_text = font.render("Нажмите ПРОБЕЛ для новой игры", True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - 30))
    screen.blit(best_text, (SCREEN_WIDTH//2 - best_text.get_width()//2, SCREEN_HEIGHT//2 + 10))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 70))
    pygame.display.update()

def show_start_screen():
    screen.fill(BLUE)
    title_text = big_font.render("FLAPPY BIRD", True, YELLOW)
    author_text = font.render("Автор: Завод Птица", True, WHITE)
    start_text = font.render("Нажмите ПРОБЕЛ для начала", True, WHITE)
    control_text = font.render("Управление: ПРОБЕЛ - прыжок", True, WHITE)
    
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(author_text, (SCREEN_WIDTH//2 - author_text.get_width()//2, SCREEN_HEIGHT//2 - 30))
    screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
    screen.blit(control_text, (SCREEN_WIDTH//2 - control_text.get_width()//2, SCREEN_HEIGHT//2 + 100))
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
    return True

def main():
    clock = pygame.time.Clock()
    best_score = 0
    
    while True:
        # Показать стартовый экран
        if not show_start_screen():
            break
            
        # Сброс игры
        bird = Bird()
        pipes = [Pipe(SCREEN_WIDTH + 100)]
        score = 0
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                        
            # Обновление
            bird.update()
            
            # Генерация труб
            if pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe(SCREEN_WIDTH))
                
            # Обновление труб
            for pipe in pipes:
                pipe.update()
                
            # Удаление вышедших труб
            pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]
            
            # Проверка прохождения труб
            for pipe in pipes:
                if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                    pipe.passed = True
                    score += 1
                    if score > best_score:
                        best_score = score
                        
            # Проверка столкновений
            bird_rect = bird.get_rect()
            
            # Столкновение с краями
            if bird.y <= 0 or bird.y + BIRD_SIZE >= SCREEN_HEIGHT:
                running = False
                
            # Столкновение с трубами
            for pipe in pipes:
                top_rect, bottom_rect = pipe.get_rects()
                if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                    running = False
                    
            # Отрисовка
            screen.fill(BLUE)
            
            # Рисуем облака для красоты
            pygame.draw.ellipse(screen, WHITE, [50, 100, 60, 40])
            pygame.draw.ellipse(screen, WHITE, [300, 200, 70, 45])
            pygame.draw.ellipse(screen, WHITE, [150, 400, 55, 35])
            
            # Рисуем трубы
            for pipe in pipes:
                pipe.draw()
                
            # Рисуем птицу
            bird.draw()
            
            # Показываем счёт
            show_score(score)
            
            # Обновление экрана
            pygame.display.update()
            clock.tick(60)
            
        # Показать экран Game Over
        show_game_over(score, best_score)
        
        # Ожидание перезапуска
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

if __name__ == "__main__":
    print("=" * 40)
    print("Flappy Bird")
    print("Автор: Завод Птица")
    print("Управление: ПРОБЕЛ - прыжок")
    print("=" * 40)
    main()
    pygame.quit()
    sys.exit()