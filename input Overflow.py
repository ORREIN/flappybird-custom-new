import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы окна
WIDTH, HEIGHT = 400, 600
FPS = 60
GROUND_HEIGHT = 80
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3
BIRD_RADIUS = 12
GRAVITY = 0.5
JUMP_FORCE = -8.5
PIPE_SPAWN_INTERVAL = 1500  # миллисекунд

# Цвета (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
BLUE = (135, 206, 235)
DARK_GREEN = (0, 150, 0)
BROWN = (139, 69, 19)

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30, bold=True)
small_font = pygame.font.SysFont("Arial", 20)

# Функция для отрисовки счёта
def draw_score(score, best_score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    best_text = small_font.render(f"Best: {best_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(best_text, (10, 45))

# Класс птицы
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.rect = pygame.Rect(x - BIRD_RADIUS, y - BIRD_RADIUS,
                                BIRD_RADIUS * 2, BIRD_RADIUS * 2)

    def jump(self):
        self.vel_y = JUMP_FORCE

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        self.rect.center = (self.x, self.y)

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), BIRD_RADIUS)
        pygame.draw.circle(screen, BLACK, (int(self.x) + 4, int(self.y) - 4), 2)  # глаз
        pygame.draw.polygon(screen, (255, 140, 0), [
            (int(self.x) - BIRD_RADIUS, int(self.y)),
            (int(self.x) - BIRD_RADIUS - 5, int(self.y) - 5),
            (int(self.x) - BIRD_RADIUS - 5, int(self.y) + 5)
        ])  # клюв

    def get_rect(self):
        return self.rect

    def is_off_screen(self):
        return self.y - BIRD_RADIUS <= 0 or self.y + BIRD_RADIUS >= HEIGHT - GROUND_HEIGHT

# Класс трубы
class Pipe:
    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.passed = False
        self.top_rect = pygame.Rect(x, 0, PIPE_WIDTH, gap_y - PIPE_GAP // 2)
        self.bottom_rect = pygame.Rect(x, gap_y + PIPE_GAP // 2, PIPE_WIDTH, HEIGHT - (gap_y + PIPE_GAP // 2) - GROUND_HEIGHT)

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)
        # Окантовка
        pygame.draw.rect(screen, DARK_GREEN, self.top_rect, 2)
        pygame.draw.rect(screen, DARK_GREEN, self.bottom_rect, 2)

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

# Основной класс игры
class Game:
    def __init__(self):
        self.bird = Bird(WIDTH // 3, HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.best_score = self.load_best_score()
        self.state = "MENU"  # MENU, GAME, GAMEOVER
        self.last_pipe_spawn = pygame.time.get_ticks()

    def load_best_score(self):
        try:
            with open("best_score.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_best_score(self):
        with open("best_score.txt", "w") as f:
            f.write(str(self.best_score))

    def spawn_pipe(self):
        gap_y = random.randint(100, HEIGHT - GROUND_HEIGHT - 100)
        self.pipes.append(Pipe(WIDTH, gap_y))

    def update(self):
        self.bird.update()

        # Добавление новых труб
        now = pygame.time.get_ticks()
        if now - self.last_pipe_spawn > PIPE_SPAWN_INTERVAL:
            self.spawn_pipe()
            self.last_pipe_spawn = now

        # Обновление труб и проверка счёта
        for pipe in self.pipes:
            pipe.update()
            if not pipe.passed and pipe.x + PIPE_WIDTH < self.bird.x:
                pipe.passed = True
                self.score += 1
                if self.score > self.best_score:
                    self.best_score = self.score
                    self.save_best_score()

            # Проверка столкновения с трубами
            if self.bird.get_rect().colliderect(pipe.top_rect) or self.bird.get_rect().colliderect(pipe.bottom_rect):
                self.state = "GAMEOVER"

        # Удаление ушедших труб
        self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

        # Проверка столкновения с верхом/низом
        if self.bird.is_off_screen():
            self.state = "GAMEOVER"

    def draw(self):
        screen.fill(BLUE)

        # Отрисовка труб
        for pipe in self.pipes:
            pipe.draw()

        # Отрисовка птицы
        self.bird.draw()

        # Отрисовка земли
        pygame.draw.rect(screen, BROWN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
        pygame.draw.rect(screen, BLACK, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT), 2)

        draw_score(self.score, self.best_score)

        # Состояния меню и game over
        if self.state == "MENU":
            title = font.render("FLAPPY BIRD", True, BLACK)
            instruction = small_font.render("Press SPACE or Click to Start", True, BLACK)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
            screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 2))

        elif self.state == "GAMEOVER":
            game_over_text = font.render("GAME OVER", True, BLACK)
            restart_text = small_font.render("Press SPACE or Click to Restart", True, BLACK)
            score_text = small_font.render(f"Your score: {self.score}", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()

    def reset(self):
        self.bird = Bird(WIDTH // 3, HEIGHT // 2)
        self.pipes.clear()
        self.score = 0
        self.last_pipe_spawn = pygame.time.get_ticks()
        self.state = "GAME"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.state == "MENU":
                    self.reset()
                elif self.state == "GAME":
                    self.bird.jump()
                elif self.state == "GAMEOVER":
                    self.reset()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # левая кнопка мыши
                if self.state == "MENU":
                    self.reset()
                elif self.state == "GAME":
                    self.bird.jump()
                elif self.state == "GAMEOVER":
                    self.reset()

# Основной цикл игры
def main():
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        if game.state == "GAME":
            game.update()

        game.draw()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
