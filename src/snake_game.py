import pygame
import random
import sys

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20
FPS = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
    def reset_game(self):
        self.snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (BLOCK_SIZE, 0)
        self.next_direction = (BLOCK_SIZE, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
    def spawn_food(self):
        while True:
            x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            if (x, y) not in self.snake:
                return (x, y)
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != (0, BLOCK_SIZE):
                    self.next_direction = (0, -BLOCK_SIZE)
                elif event.key == pygame.K_DOWN and self.direction != (0, -BLOCK_SIZE):
                    self.next_direction = (0, BLOCK_SIZE)
                elif event.key == pygame.K_LEFT and self.direction != (BLOCK_SIZE, 0):
                    self.next_direction = (-BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT and self.direction != (-BLOCK_SIZE, 0):
                    self.next_direction = (BLOCK_SIZE, 0)
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        return True
    def update(self):
        if self.game_over:
            return
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT):
            self.game_over = True
            return
        if new_head in self.snake:
            self.game_over = True
            return
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()
    def draw(self):
        self.screen.fill(BLACK)
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.screen, RED, (self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press SPACE to restart", True, YELLOW)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
