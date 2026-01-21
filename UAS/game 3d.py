import pygame
import math
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.02
JUMP_POWER = 0.3

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GROUND_GREEN = (34, 139, 34)
GROUND_BROWN = (139, 115, 85)
GREEN = (34, 197, 94)
RED = (239, 68, 68)
YELLOW = (255, 215, 0)

# Warna Minecraft style
STEVE_SKIN = (255, 220, 177)
STEVE_HAIR = (92, 64, 51)
STEVE_SHIRT = (71, 171, 228)
STEVE_PANTS = (48, 76, 127)
STEVE_SHOES = (80, 80, 80)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Pendaki Gunung 3D - Minecraft Style")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)


class Mountain:
    """Class untuk gunung 3D"""
    def __init__(self, x, z, size, height_multiplier=1.5):
        self.x = x
        self.z = z
        self.size = size
        self.height = size * height_multiplier
        self.color = (random.randint(80, 120), random.randint(120, 160), random.randint(60, 100))
        
        # Vertices piramida (gunung)
        self.vertices = [
            [-size, 0, -size],  # base corner 1
            [size, 0, -size],   # base corner 2
            [size, 0, size],    # base corner 3
            [-size, 0, size],   # base corner 4
            [0, self.height, 0]  # peak
        ]
        
        self.faces = [
            [0, 1, 4],  # sisi 1
            [1, 2, 4],  # sisi 2
            [2, 3, 4],  # sisi 3
            [3, 0, 4],  # sisi 4
            [0, 1, 2, 3]  # base
        ]
    
    def get_height_at_position(self, player_x, player_z):
        """Hitung ketinggian gunung di posisi tertentu - perbaikan untuk climbing"""
        # Jarak dari pusat gunung
        dx = player_x - self.x
        dz = player_z - self.z
        
        # Jarak horizontal dari pusat
        distance = math.sqrt(dx * dx + dz * dz)
        
        # Jika dalam radius gunung
        if distance < self.size:
            # Tinggi linear dari puncak ke dasar
            # Semakin dekat ke pusat = semakin tinggi
            height_ratio = 1 - (distance / self.size)
            return self.height * height_ratio
        
        return 0


class MinecraftPlayer:
    """Class untuk pemain style Minecraft (blocky)"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 3
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = True
        self.scale = 1.0
        self.animation_frame = 0
        self.facing_right = True
        
        # Ukuran bagian tubuh Minecraft style (lebih blocky)
        # Kepala (kubus besar)
        self.head_size = 0.4
        self.head_vertices = self.create_cube(self.head_size)
        
        # Badan (rectangular)
        self.body_vertices = [
            [-0.25, -0.2, -0.15], [0.25, -0.2, -0.15], 
            [0.25, 0.4, -0.15], [-0.25, 0.4, -0.15],
            [-0.25, -0.2, 0.15], [0.25, -0.2, 0.15], 
            [0.25, 0.4, 0.15], [-0.25, 0.4, 0.15],
        ]
        
        # Tangan (arm)
        self.arm_vertices = self.create_cube(0.15, 0.5, 0.15)
        
        # Kaki (leg)
        self.leg_vertices = self.create_cube(0.15, 0.5, 0.15)
        
        self.cube_faces = [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
            [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]
        ]
    
    def create_cube(self, width, height=None, depth=None):
        """Buat vertices untuk kubus dengan ukuran tertentu"""
        if height is None:
            height = width
        if depth is None:
            depth = width
            
        w, h, d = width/2, height/2, depth/2
        return [
            [-w, -h, -d], [w, -h, -d], [w, h, -d], [-w, h, -d],
            [-w, -h, d], [w, -h, d], [w, h, d], [-w, h, d],
        ]


class Game:
    """Class utama game"""
    def __init__(self):
        self.state = "menu"
        self.player = MinecraftPlayer()
        self.mountains = []
        self.altitude = 0
        self.stamina = 100
        self.camera_rotation = 0.3
        self.speed = 0.08
        self.max_altitude = 0
        self.climb_speed = 0.05
        
        # Buat gunung yang lebih tinggi dan lebih banyak
        for i in range(6):
            x = (random.random() - 0.5) * 5
            z = i * 3 + 3
            size = 1.0 + random.random() * 0.8
            height_mult = 2.0 + random.random() * 1.0  # Gunung lebih tinggi
            self.mountains.append(Mountain(x, z, size, height_mult))
    
    def reset(self):
        """Reset game"""
        self.player = MinecraftPlayer()
        self.mountains = []
        self.altitude = 0
        self.stamina = 100
        self.camera_rotation = 0.3
        self.state = "playing"
        self.max_altitude = 0
        
        for i in range(6):
            x = (random.random() - 0.5) * 5
            z = i * 3 + 3
            size = 1.0 + random.random() * 0.8
            height_mult = 2.0 + random.random() * 1.0
            self.mountains.append(Mountain(x, z, size, height_mult))
    
    def transform_vertex(self, vertex, pos_x, pos_y, pos_z, rotation, scale, reflect_x=False):
        """Transformasi 3D lengkap"""
        x, y, z = vertex
        
        # 1. SKALA
        x *= scale
        y *= scale
        z *= scale
        
        # 2. REFLEKSI X-axis
        if reflect_x:
            x *= -1
        
        # 3. ROTASI Y-axis
        cos_r = math.cos(rotation)
        sin_r = math.sin(rotation)
        x_new = x * cos_r - z * sin_r
        z_new = x * sin_r + z * cos_r
        x = x_new
        z = z_new
        
        # 4. TRANSLASI
        x += pos_x
        y += pos_y
        z += pos_z
        
        # 5. PROYEKSI PERSPEKTIF
        distance = 7
        if distance + z != 0:
            factor = distance / (distance + z)
        else:
            factor = 1
            
        screen_x = WIDTH // 2 + x * factor * 90
        screen_y = HEIGHT * 0.7 - y * factor * 90
        
        return (int(screen_x), int(screen_y), z, factor)
    
    def draw_cube_3d(self, vertices, faces, pos_x, pos_y, pos_z, rotation, scale, color, reflect_x=False):
        """Gambar kubus 3D"""
        transformed = []
        for vertex in vertices:
            transformed.append(
                self.transform_vertex(vertex, pos_x, pos_y, pos_z, rotation, scale, reflect_x)
            )
        
        # Sort faces by z-depth for proper rendering
        face_depths = []
        for i, face in enumerate(faces):
            points = [transformed[j] for j in face]
            avg_z = sum(p[2] for p in points) / len(points)
            face_depths.append((avg_z, i))
        
        face_depths.sort(reverse=True)
        
        # Draw faces from back to front
        for avg_z, face_idx in face_depths:
            face = faces[face_idx]
            points = [transformed[j] for j in face]
            
            if avg_z < -1:
                continue
            
            # Brightness based on depth and face orientation
            brightness = max(0.4, min(1.0, 1 - avg_z / 20))
            
            # Different brightness for different faces (lighting effect)
            if face_idx == 2:  # top face
                brightness *= 1.2
            elif face_idx in [4, 5]:  # side faces
                brightness *= 0.8
            
            shaded_color = tuple(int(min(255, c * brightness)) for c in color)
            
            screen_points = [(p[0], p[1]) for p in points]
            if len(screen_points) >= 3:
                pygame.draw.polygon(screen, shaded_color, screen_points)
                pygame.draw.polygon(screen, BLACK, screen_points, 1)
    
    def draw_mountains(self):
        """Gambar semua gunung"""
        for mountain in self.mountains:
            # Draw mountain
            transformed = []
            for vertex in mountain.vertices:
                transformed.append(
                    self.transform_vertex(vertex, mountain.x, 0, mountain.z, 
                                        self.camera_rotation, 1.0)
                )
            
            # Sort faces by depth
            face_depths = []
            for i, face in enumerate(mountain.faces):
                points = [transformed[j] for j in face]
                avg_z = sum(p[2] for p in points) / len(points)
                face_depths.append((avg_z, i))
            
            face_depths.sort(reverse=True)
            
            # Draw mountain faces
            for avg_z, face_idx in face_depths:
                face = mountain.faces[face_idx]
                points = [transformed[j] for j in face]
                
                if avg_z < -1:
                    continue
                
                brightness = max(0.4, 1 - avg_z / 20)
                
                # Different shading for different faces
                if face_idx == 4:  # base
                    brightness *= 0.6
                else:  # sides
                    brightness *= (0.7 + face_idx * 0.1)
                
                shaded_color = tuple(int(c * brightness) for c in mountain.color)
                
                screen_points = [(p[0], p[1]) for p in points]
                if len(screen_points) >= 3:
                    pygame.draw.polygon(screen, shaded_color, screen_points)
                    pygame.draw.polygon(screen, BLACK, screen_points, 2)
            
            # Snow cap on peak
            if mountain.height > 2.0:
                peak = self.transform_vertex(
                    [0, mountain.height, 0],
                    mountain.x, 0, mountain.z,
                    self.camera_rotation, 1.0
                )
                radius = int(12 * peak[3])
                if radius > 0:
                    pygame.draw.circle(screen, WHITE, (peak[0], peak[1]), radius)
                    pygame.draw.circle(screen, (200, 200, 200), (peak[0], peak[1]), radius, 2)
    
    def draw_minecraft_player(self):
        """Gambar pemain style Minecraft dengan bagian tubuh terpisah"""
        walk_anim = math.sin(self.player.animation_frame * 0.4) * 0.3
        
        # REFLEKSI: Balik karakter tergantung arah hadap
        # facing_right = True -> normal (menghadap kanan)
        # facing_right = False -> reflect X-axis (menghadap kiri)
        reflect = not self.player.facing_right
        
        # Offset untuk animasi berjalan
        arm_swing = walk_anim if self.player.animation_frame > 0 else 0
        leg_swing = walk_anim if self.player.animation_frame > 0 else 0
        
        # Multiplier untuk posisi kiri/kanan berdasarkan arah hadap
        # Jika facing_right: 1, jika facing_left: -1
        direction = 1 if self.player.facing_right else -1
        
        # Body (badan)
        self.draw_cube_3d(
            self.player.body_vertices,
            self.player.cube_faces,
            self.player.x,
            self.player.y + 0.1,
            self.player.z,
            self.camera_rotation,
            self.player.scale,
            STEVE_SHIRT,
            reflect
        )
        
        # Head (kepala) - sedikit lebih tinggi
        head_offset = 0.05 * math.sin(self.player.animation_frame * 0.2) if self.player.animation_frame > 0 else 0
        self.draw_cube_3d(
            self.player.head_vertices,
            self.player.cube_faces,
            self.player.x,
            self.player.y + 0.6 + head_offset,
            self.player.z,
            self.camera_rotation,
            self.player.scale,
            STEVE_SKIN,
            reflect
        )
        
        # Hair (rambut) - layer di atas kepala
        hair_vertices = self.player.create_cube(0.42, 0.15, 0.42)
        self.draw_cube_3d(
            hair_vertices,
            self.player.cube_faces,
            self.player.x,
            self.player.y + 0.85 + head_offset,
            self.player.z,
            self.camera_rotation,
            self.player.scale,
            STEVE_HAIR,
            reflect
        )
        
        # Eyes (mata) - agar jelas arah hadap
        # Posisi mata menyesuaikan arah hadap
        eye_y = self.player.y + 0.75 + head_offset
        eye_z_offset = 0.21  # Di depan wajah
        eye_distance = 0.1  # Jarak antar mata
        
        if self.player.facing_right:
            # Menghadap kanan - mata di sisi kanan
            left_eye_x = self.player.x - eye_distance
            right_eye_x = self.player.x + eye_distance
        else:
            # Menghadap kiri - mata di sisi kiri (flip)
            left_eye_x = self.player.x + eye_distance
            right_eye_x = self.player.x - eye_distance
        
        # Gambar mata (kubus kecil hitam)
        eye_size = 0.05
        eye_vertices = self.player.create_cube(eye_size)
        
        # Left eye
        self.draw_cube_3d(
            eye_vertices,
            self.player.cube_faces,
            left_eye_x,
            eye_y,
            self.player.z + eye_z_offset * (1 if not reflect else -1),
            self.camera_rotation,
            self.player.scale,
            (50, 50, 50),  # Dark gray/black
            reflect
        )
        
        # Right eye
        self.draw_cube_3d(
            eye_vertices,
            self.player.cube_faces,
            right_eye_x,
            eye_y,
            self.player.z + eye_z_offset * (1 if not reflect else -1),
            self.camera_rotation,
            self.player.scale,
            (50, 50, 50),  # Dark gray/black
            reflect
        )
        
        # Arms (tangan) - posisi menyesuaikan arah hadap
        # Left arm (tangan kiri dari perspektif karakter)
        left_arm_x = -0.4 * direction * self.player.scale
        self.draw_cube_3d(
            self.player.arm_vertices,
            self.player.cube_faces,
            self.player.x + left_arm_x,
            self.player.y + 0.15 - arm_swing * 0.1 * direction,
            self.player.z + arm_swing * 0.15,
            self.camera_rotation,
            self.player.scale,
            STEVE_SHIRT,
            reflect
        )
        
        # Right arm (tangan kanan dari perspektif karakter)
        right_arm_x = 0.4 * direction * self.player.scale
        self.draw_cube_3d(
            self.player.arm_vertices,
            self.player.cube_faces,
            self.player.x + right_arm_x,
            self.player.y + 0.15 + arm_swing * 0.1 * direction,
            self.player.z - arm_swing * 0.15,
            self.camera_rotation,
            self.player.scale,
            STEVE_SHIRT,
            reflect
        )
        
        # Legs (kaki) - posisi menyesuaikan arah hadap
        leg_x_offset = 0.13 * direction
        
        # Left leg (kaki kiri dari perspektif karakter)
        self.draw_cube_3d(
            self.player.leg_vertices,
            self.player.cube_faces,
            self.player.x - leg_x_offset * self.player.scale,
            self.player.y - 0.25 - leg_swing * 0.1 * direction,
            self.player.z + leg_swing * 0.1,
            self.camera_rotation,
            self.player.scale,
            STEVE_PANTS,
            reflect
        )
        
        # Right leg (kaki kanan dari perspektif karakter)
        self.draw_cube_3d(
            self.player.leg_vertices,
            self.player.cube_faces,
            self.player.x + leg_x_offset * self.player.scale,
            self.player.y - 0.25 + leg_swing * 0.1 * direction,
            self.player.z - leg_swing * 0.1,
            self.camera_rotation,
            self.player.scale,
            STEVE_PANTS,
            reflect
        )
    
    def draw_background(self):
        """Gambar background"""
        # Sky gradient
        for y in range(int(HEIGHT * 0.7)):
            color_factor = y / (HEIGHT * 0.7)
            color = (
                int(135 + color_factor * 89),
                int(206 + color_factor * 44),
                int(235 + color_factor * 20)
            )
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))
        
        # Sun
        sun_y = 100 - int(self.camera_rotation * 10)
        pygame.draw.circle(screen, YELLOW, (WIDTH - 120, sun_y), 45)
        pygame.draw.circle(screen, (255, 200, 0), (WIDTH - 120, sun_y), 45, 3)
        
        # Clouds
        cloud_x1 = (120 + int(self.camera_rotation * 20)) % WIDTH
        cloud_x2 = (550 + int(self.camera_rotation * 15)) % WIDTH
        pygame.draw.ellipse(screen, WHITE, (cloud_x1, 90, 120, 50))
        pygame.draw.ellipse(screen, WHITE, (cloud_x2, 130, 150, 60))
        
        # Ground (grass blocks Minecraft style)
        ground_y = int(HEIGHT * 0.7)
        # Grass top
        pygame.draw.rect(screen, GROUND_GREEN, (0, ground_y, WIDTH, 30))
        # Dirt
        pygame.draw.rect(screen, GROUND_BROWN, (0, ground_y + 30, WIDTH, HEIGHT - ground_y - 30))
        
        # Grid lines for blocky effect
        for x in range(0, WIDTH, 40):
            pygame.draw.line(screen, (0, 100, 0), (x, ground_y), (x, ground_y + 30))
        for x in range(0, WIDTH, 40):
            pygame.draw.line(screen, (100, 80, 60), (x, ground_y + 30), (x, HEIGHT))
    
    def draw_ui(self):
        """Gambar UI"""
        # Stamina bar
        pygame.draw.rect(screen, (60, 60, 60), (18, 18, 214, 44))
        stamina_color = GREEN if self.stamina > 30 else RED
        pygame.draw.rect(screen, stamina_color, (25, 25, int(self.stamina * 2), 30))
        pygame.draw.rect(screen, WHITE, (25, 25, 200, 30), 3)
        stamina_text = small_font.render("STAMINA", True, WHITE)
        screen.blit(stamina_text, (30, 30))
        
        # Altitude
        pygame.draw.rect(screen, (60, 60, 60), (18, 68, 214, 44))
        altitude_text = font.render(f"⛰️ {int(self.altitude)}m", True, WHITE)
        screen.blit(altitude_text, (30, 75))
        
        # Max Altitude
        pygame.draw.rect(screen, (60, 60, 60), (18, 118, 214, 39))
        max_text = small_font.render(f"Max: {int(self.max_altitude)}m", True, YELLOW)
        screen.blit(max_text, (30, 128))
        
        # Instructions
        pygame.draw.rect(screen, (60, 60, 60), (WIDTH - 232, 18, 214, 160))
        instructions = [
            "W/↑: Maju",
            "S/↓: Mundur",
            "A/←: Kiri",
            "D/→: Kanan",
            "SPACE: Lompat",
        ]
        for i, text in enumerate(instructions):
            inst = small_font.render(text, True, WHITE)
            screen.blit(inst, (WIDTH - 220, 28 + i * 25))
        
        # Direction indicator (panah menunjukkan arah hadap)
        direction_text = "Hadap: " + ("➡️ KANAN" if self.player.facing_right else "⬅️ KIRI")
        direction_color = (100, 200, 255) if self.player.facing_right else (255, 200, 100)
        dir_surface = small_font.render(direction_text, True, direction_color)
        screen.blit(dir_surface, (WIDTH - 220, 155))
    
    def get_ground_height(self, x, z):
        """Dapatkan ketinggian tanah di posisi tertentu"""
        max_height = 0
        for mountain in self.mountains:
            h = mountain.get_height_at_position(x, z)
            max_height = max(max_height, h)
        return max_height
    
    def update(self, keys):
        """Update game logic"""
        if self.state != "playing":
            return
        
        moved = False
        old_x, old_z = self.player.x, self.player.z
        
        # Movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.x = max(self.player.x - self.speed, -3)
            self.player.facing_right = False
            moved = True
        
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.x = min(self.player.x + self.speed, 3)
            self.player.facing_right = True
            moved = True
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.z += self.speed
            self.stamina = max(self.stamina - 0.2, 0)
            moved = True
        
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.z = max(self.player.z - self.speed, 2)
            self.stamina = min(self.stamina + 0.1, 100)
            moved = True
        
        # Jump
        if keys[pygame.K_SPACE] and self.player.on_ground:
            self.player.velocity_y = JUMP_POWER
            self.player.is_jumping = True
            self.player.on_ground = False
        
        # Gravity
        if not self.player.on_ground:
            self.player.velocity_y -= GRAVITY
            self.player.y += self.player.velocity_y
        
        # Ground collision - stick to mountain surface
        ground_height = self.get_ground_height(self.player.x, self.player.z)
        
        if self.player.y <= ground_height:
            self.player.y = ground_height
            self.player.velocity_y = 0
            self.player.on_ground = True
            self.player.is_jumping = False
        else:
            self.player.on_ground = False
        
        # Calculate altitude
        self.altitude = self.player.y * 50 + self.player.z * 10
        self.max_altitude = max(self.max_altitude, self.altitude)
        
        # Scale based on height
        self.player.scale = max(0.7, 1 - self.player.y * 0.08)
        
        # Camera rotation
        self.camera_rotation += 0.003
        
        # Animation
        if moved:
            self.player.animation_frame += 1
        else:
            self.player.animation_frame = max(0, self.player.animation_frame - 2)
            self.stamina = min(self.stamina + 0.3, 100)
        
        # Win/Lose conditions
        if self.stamina <= 0:
            self.state = "gameover"
        
        if self.altitude >= 300:
            self.state = "win"
    
    def draw_menu(self):
        """Menu screen"""
        screen.fill(SKY_BLUE)
        
        title = font.render("⛰️ MINECRAFT MOUNTAIN CLIMBER", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))
        
        subtitle = small_font.render("Naiki gunung setinggi mungkin!", True, BLACK)
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
        
        start = font.render("Tekan SPACE untuk mulai", True, GREEN)
        screen.blit(start, start.get_rect(center=(WIDTH//2, HEIGHT//2 + 50)))
        
        info = [
            "WASD/Arrow Keys: Gerak",
            "SPACE: Lompat",
            "🎯 Target: 300m",
            "⚠️ Jaga stamina!",
        ]
        for i, line in enumerate(info):
            text = small_font.render(line, True, BLACK)
            screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2 + 120 + i*30)))
    
    def draw_gameover(self):
        """Game over screen"""
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        if self.state == "win":
            text = font.render("🎉 PUNCAK TERCAPAI! 🎉", True, YELLOW)
        else:
            text = font.render("STAMINA HABIS!", True, RED)
        screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
        
        score = font.render(f"Ketinggian: {int(self.altitude)}m", True, WHITE)
        screen.blit(score, score.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
        
        maxscore = small_font.render(f"Tertinggi: {int(self.max_altitude)}m", True, YELLOW)
        screen.blit(maxscore, maxscore.get_rect(center=(WIDTH//2, HEIGHT//2 + 60)))
        
        restart = small_font.render("SPACE: Main Lagi | ESC: Keluar", True, WHITE)
        screen.blit(restart, restart.get_rect(center=(WIDTH//2, HEIGHT//2 + 110)))


def main():
    """Main game loop"""
    game = Game()
    running = True
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game.state in ["gameover", "win"]:
                        running = False
                    else:
                        running = False
                
                if event.key == pygame.K_SPACE:
                    if game.state == "menu":
                        game.reset()
                    elif game.state in ["gameover", "win"]:
                        game.reset()
        
        keys = pygame.key.get_pressed()
        game.update(keys)
        
        if game.state == "menu":
            game.draw_menu()
        else:
            game.draw_background()
            game.draw_mountains()
            game.draw_minecraft_player()
            game.draw_ui()
            
            if game.state in ["gameover", "win"]:
                game.draw_gameover()
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()