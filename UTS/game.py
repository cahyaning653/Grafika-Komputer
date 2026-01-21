import pygame
import random

pygame.init()

# =====================
# WARNA
# =====================
HITAM = (0, 0, 0)
PUTIH = (255, 255, 255)
MERAH = (255, 0, 0)
HIJAU = (0, 255, 0)
BIRU = (0, 150, 255)
KUNING = (255, 255, 0)
ORANGE = (255, 165, 0)
UNGU = (150, 0, 255)
PINK = (255, 105, 180)

WARNA_BATA = [MERAH, ORANGE, KUNING, HIJAU, BIRU, UNGU, PINK]

# =====================
# LAYAR
# =====================
LEBAR, TINGGI = 800, 600
layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Brick Breaker - Transformasi 2D")
jam = pygame.time.Clock()

font = pygame.font.Font(None, 36)
font_besar = pygame.font.Font(None, 64)

# =====================
# PADDLE (TRANSLASI, ROTASI, SKALA)
# =====================
class Paddle:
    def __init__(self):
        self.lebar_asli = 120
        self.lebar = 120
        self.tinggi = 20
        self.x = LEBAR // 2 - self.lebar // 2
        self.y = TINGGI - 50
        self.kecepatan = 8
        self.sudut = 0
        self.skala_timer = 0

    def gerak(self, arah):
        if arah == "KIRI" and self.x > 0:
            self.x -= self.kecepatan
        elif arah == "KANAN" and self.x < LEBAR - self.lebar:
            self.x += self.kecepatan

    def gambar(self):
        surface = pygame.Surface((self.lebar, self.tinggi), pygame.SRCALPHA)
        surface.fill(BIRU)

        rotated = pygame.transform.rotate(surface, self.sudut)
        rect = rotated.get_rect(center=(self.x + self.lebar // 2,
                                        self.y + self.tinggi // 2))
        layar.blit(rotated, rect)

        if self.skala_timer > 0:
            self.skala_timer -= 1
        else:
            self.lebar = self.lebar_asli
            self.sudut = 0

# =====================
# BOLA (REFLEKSI)
# =====================
class Bola:
    def __init__(self, level):
        self.radius = 10
        self.x = LEBAR // 2
        self.y = TINGGI // 2
        speed = 4 + level
        self.dx = random.choice([-speed, speed])
        self.dy = -speed

    def gerak(self):
        self.x += self.dx
        self.y += self.dy

        # Refleksi dinding
        if self.x - self.radius <= 0 or self.x + self.radius >= LEBAR:
            self.dx *= -1
        if self.y - self.radius <= 0:
            self.dy *= -1

    def gambar(self):
        pygame.draw.circle(layar, KUNING, (int(self.x), int(self.y)), self.radius)

    def cek_paddle(self, paddle):
        if paddle.y <= self.y + self.radius <= paddle.y + paddle.tinggi:
            if paddle.x <= self.x <= paddle.x + paddle.lebar:
                self.dy *= -1

                # ROTASI
                paddle.sudut = random.choice([-15, 15])

                # SKALA
                paddle.lebar = int(paddle.lebar_asli * 1.2)
                paddle.skala_timer = 15
                return True
        return False

    def jatuh(self):
        return self.y - self.radius > TINGGI

# =====================
# BATA WARNA-WARNI
# =====================
class Bata:
    def __init__(self, x, y, warna):
        self.rect = pygame.Rect(x, y, 75, 30)
        self.warna = warna
        self.aktif = True

    def gambar(self):
        if self.aktif:
            pygame.draw.rect(layar, self.warna, self.rect)
            pygame.draw.rect(layar, PUTIH, self.rect, 2)

    def cek(self, bola):
        if self.aktif and self.rect.collidepoint(bola.x, bola.y):
            self.aktif = False
            bola.dy *= -1
            return True
        return False

def buat_bata(level):
    bata = []
    baris = 3 + level

    for y in range(baris):
        warna = WARNA_BATA[y % len(WARNA_BATA)]
        for x in range(9):
            bata.append(Bata(x * 80 + 40, y * 40 + 60, warna))
    return bata

# =====================
# GAME UTAMA
# =====================
def main():
    paddle = Paddle()
    level = 1
    skor = 0
    best_score = 0
    nyawa = 3

    bola = Bola(level)
    bata = buat_bata(level)

    game_over = False

    while True:
        jam.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                    return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.gerak("KIRI")
        if keys[pygame.K_RIGHT]:
            paddle.gerak("KANAN")

        if not game_over:
            bola.gerak()
            bola.cek_paddle(paddle)

            for b in bata:
                if b.cek(bola):
                    skor += 10

            if bola.jatuh():
                nyawa -= 1
                bola = Bola(level)
                if nyawa == 0:
                    game_over = True
                    best_score = max(best_score, skor)

            # NAIK LEVEL
            if all(not b.aktif for b in bata):
                level += 1
                bola = Bola(level)
                bata = buat_bata(level)

        # =====================
        # RENDER
        # =====================
        layar.fill(HITAM)

        paddle.gambar()
        bola.gambar()
        for b in bata:
            b.gambar()

        layar.blit(font.render(f"Skor : {skor}", True, PUTIH), (10, 10))
        layar.blit(font.render(f"Best : {best_score}", True, HIJAU), (10, 45))
        layar.blit(font.render(f"Nyawa: {nyawa}", True, MERAH), (650, 10))
        layar.blit(font.render(f"Level: {level}", True, KUNING), (650, 45))

        if game_over:
            layar.blit(font_besar.render("GAME OVER", True, MERAH), (250, 250))
            layar.blit(font.render("Tekan SPASI untuk restart", True, PUTIH), (230, 320))

        pygame.display.flip()

# =====================
# JALANKAN
# =====================
main()
