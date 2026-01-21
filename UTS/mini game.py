import pygame
import random
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

# Setup layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Kelas Pemain
class Player:
    def __init__(self):
        self.width = 80
        self.height = 20
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 50
        self.speed = 7
        self.color = BLUE
    
    def move(self, direction):
        if direction == "LEFT" and self.x > 0:
            self.x -= self.speed
        elif direction == "RIGHT" and self.x < WIDTH - self.width:
            self.x += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Tambahkan detail visual
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)

# Kelas Objek Jatuh
class FallingObject:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(3, 7)
        self.type = random.choice(['good', 'bad'])
        self.color = GREEN if self.type == 'good' else RED
    
    def fall(self):
        self.y += self.speed
    
    def draw(self):
        if self.type == 'good':
            # Gambar lingkaran untuk objek baik
            pygame.draw.circle(screen, self.color, 
                             (self.x + self.width // 2, self.y + self.height // 2), 
                             self.width // 2)
        else:
            # Gambar persegi untuk objek buruk
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def is_off_screen(self):
        return self.y > HEIGHT
    
    def check_collision(self, player):
        if (self.y + self.height >= player.y and 
            self.x + self.width > player.x and 
            self.x < player.x + player.width):
            return True
        return False

# Fungsi utama game
def main():
    player = Player()
    falling_objects = []
    score = 0
    lives = 3
    spawn_timer = 0
    game_over = False
    
    running = True
    while running:
        clock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # Restart game
                    return main()
        
        if not game_over:
            # Input pemain
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.move("LEFT")
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.move("RIGHT")
            
            # Spawn objek jatuh
            spawn_timer += 1
            if spawn_timer > 40:  # Spawn setiap ~0.67 detik
                falling_objects.append(FallingObject())
                spawn_timer = 0
            
            # Update objek jatuh
            for obj in falling_objects[:]:
                obj.fall()
                
                # Cek collision
                if obj.check_collision(player):
                    if obj.type == 'good':
                        score += 10
                    else:
                        lives -= 1
                        if lives <= 0:
                            game_over = True
                    falling_objects.remove(obj)
                
                # Hapus objek yang keluar layar
                elif obj.is_off_screen():
                    falling_objects.remove(obj)
        
        # Render
        screen.fill(BLACK)
        
        # Gambar pemain dan objek
        if not game_over:
            player.draw()
            for obj in falling_objects:
                obj.draw()
        
        # Tampilkan skor dan nyawa
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        
        # Instruksi
        if not game_over:
            instruction_font = pygame.font.Font(None, 24)
            inst_text = instruction_font.render("Arrow Keys/A-D to move | Catch Green, Avoid Red", True, YELLOW)
            screen.blit(inst_text, (WIDTH // 2 - 200, HEIGHT - 30))
        
        # Game over screen
        if game_over:
            game_over_text = font.render("GAME OVER!", True, RED)
            final_score_text = font.render(f"Final Score: {score}", True, WHITE)
            restart_text = font.render("Press SPACE to Restart", True, YELLOW)
            
            screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
            screen.blit(final_score_text, (WIDTH // 2 - 120, HEIGHT // 2))
            screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 60))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

# Jalankan game
if __name__ == "__main__":
    main()