import tkinter as tk
import math

class MiniGameGrafika:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Game: Space Catcher (Manual Graphics)")
        
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        # State Game
        self.ufo_pos = [300, 200]
        self.ufo_scale = 1.0
        self.ufo_angle = 0
        self.star_pos = [100, 100]
        self.score = 0
        
        # Binding Input
        self.root.bind("<KeyPress>", self.handle_input)
        
        self.update_game()

    # --- 1. ALGORITMA GARIS (Bresenham) ---
    def draw_line(self, x0, y0, x1, y1, color="white"):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.canvas.create_rectangle(x0, y0, x0, y0, outline=color, width=0)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    # --- 2. ALGORITMA LINGKARAN (Midpoint) ---
    def draw_circle(self, x_center, y_center, r, color="yellow"):
        x = r
        y = 0
        if r > 0:
            self.put_pixel(x + x_center, -y + y_center, color)
            self.put_pixel(y + x_center, x + y_center, color)
            self.put_pixel(-x + x_center, y + y_center, color)
            self.put_pixel(-y + x_center, -x + y_center, color)
        
        P = 1 - r
        while x > y:
            y += 1
            if P <= 0:
                P = P + 2 * y + 1
            else:
                x -= 1
                P = P + 2 * y - 2 * x + 1
            
            if x < y: break
            self.put_pixel(x + x_center, y + y_center, color)
            self.put_pixel(-x + x_center, y + y_center, color)
            self.put_pixel(x + x_center, -y + y_center, color)
            self.put_pixel(-x + x_center, -y + y_center, color)
            self.put_pixel(y + x_center, x + y_center, color)
            self.put_pixel(-y + x_center, x + y_center, color)
            self.put_pixel(y + x_center, -x + y_center, color)
            self.put_pixel(-y + x_center, -x + y_center, color)

    def put_pixel(self, x, y, color):
        self.canvas.create_line(x, y, x + 1, y, fill=color)

    # --- 3. ALGORITMA POLIGON & TRANSFORMASI ---
    def draw_ufo(self):
        # Titik dasar poligon (berbentuk diamond/UFO)
        points = [[0, -20], [30, 0], [0, 20], [-30, 0]]
        transformed = []

        for p in points:
            # A. SKALA
            px, py = p[0] * self.ufo_scale, p[1] * self.ufo_scale
            
            # B. ROTASI
            rad = math.radians(self.ufo_angle)
            rx = px * math.cos(rad) - py * math.sin(rad)
            ry = px * math.sin(rad) + py * math.cos(rad)
            
            # C. TRANSLASI
            tx = rx + self.ufo_pos[0]
            ty = ry + self.ufo_pos[1]
            
            transformed.append((tx, ty))

        # Menggambar sisi poligon secara manual dengan Bresenham
        for i in range(len(transformed)):
            p1 = transformed[i]
            p2 = transformed[(i + 1) % len(transformed)]
            self.draw_line(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), "cyan")

    # --- 4. LOGIKA GAME ---
    def handle_input(self, event):
        step = 10
        if event.keysym == "Up": self.ufo_pos[1] -= step
        if event.keysym == "Down": self.ufo_pos[1] += step
        if event.keysym == "Left": self.ufo_pos[0] -= step
        if event.keysym == "Right": self.ufo_pos[0] += step
        
        # D. REFLEKSI (Jika menabrak dinding kanan, mental ke kiri)
        if self.ufo_pos[0] > self.canvas_width:
            self.ufo_pos[0] = self.canvas_width - 10 # Refleksi sederhana posisi

    def update_game(self):
        self.canvas.delete("all")
        
        # Update Rotasi Otomatis
        self.ufo_angle = (self.ufo_angle + 5) % 360
        
        # Gambar Batas (Garis)
        self.draw_line(10, 10, 590, 10)
        self.draw_line(10, 390, 590, 390)
        
        # Gambar Bintang (Lingkaran)
        self.draw_circle(self.star_pos[0], self.star_pos[1], 15, "yellow")
        
        # Gambar Karakter (Poligon + Transformasi)
        self.draw_ufo()
        
        # Cek Tabrakan (Sederhana)
        dist = math.sqrt((self.ufo_pos[0]-self.star_pos[1])**2 + (self.ufo_pos[1]-self.star_pos[1])**2)
        if abs(self.ufo_pos[0] - self.star_pos[0]) < 30 and abs(self.ufo_pos[1] - self.star_pos[1]) < 30:
            self.score += 1
            self.star_pos = [(self.star_pos[0] + 150) % 500, (self.star_pos[1] + 100) % 350]
            self.ufo_scale = 1.5 # Skala membesar saat menangkap
        else:
            if self.ufo_scale > 1.0: self.ufo_scale -= 0.05 # Kembali ke skala normal

        self.canvas.create_text(50, 30, text=f"Score: {self.score}", fill="white")
        self.root.after(50, self.update_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = MiniGameGrafika(root)
    root.mainloop()