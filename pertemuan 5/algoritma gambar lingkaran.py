import turtle
import math

# Setup turtle
screen = turtle.Screen()
screen.title("Praktikum - Menggambar Garis, Lingkaran, dan Poligon")
screen.setup(width=800, height=600)
screen.bgcolor("white")

t = turtle.Turtle()
t.speed(3)

# ==================== FUNGSI ALGORITMA ====================

def dda_line(x1, y1, x2, y2, color="black"):
    """
    Algoritma DDA (Digital Differential Analyzer) untuk menggambar garis
    """
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.color(color)
    
    dx = x2 - x1
    dy = y2 - y1
    
    # Menentukan jumlah langkah
    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)
    
    # Menghitung increment
    if steps != 0:
        x_inc = dx / steps
        y_inc = dy / steps
    else:
        return
    
    # Menggambar titik-titik
    x = x1
    y = y1
    
    for i in range(int(steps) + 1):
        t.goto(round(x), round(y))
        x += x_inc
        y += y_inc

def bresenham_line(x1, y1, x2, y2, color="blue"):
    """
    Algoritma Bresenham untuk menggambar garis
    """
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.color(color)
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    # Menentukan arah increment
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    
    err = dx - dy
    x, y = x1, y1
    
    while True:
        t.goto(x, y)
        
        if x == x2 and y == y2:
            break
        
        e2 = 2 * err
        
        if e2 > -dy:
            err -= dy
            x += sx
        
        if e2 < dx:
            err += dx
            y += sy

def midpoint_circle(xc, yc, r, color="red"):
    """
    Algoritma Midpoint Circle untuk menggambar lingkaran
    """
    t.color(color)
    
    x = 0
    y = r
    p = 1 - r
    
    def plot_circle_points(xc, yc, x, y):
        """Plot 8 simetris points"""
        points = [
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x)
        ]
        return points
    
    # Plot initial points
    points = plot_circle_points(xc, yc, x, y)
    t.penup()
    t.goto(points[0])
    t.pendown()
    
    all_points = []
    
    while x <= y:
        all_points.extend(plot_circle_points(xc, yc, x, y))
        x += 1
        
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
    
    # Sort points untuk menggambar lingkaran yang smooth
    # Menggunakan sudut untuk sorting
    sorted_points = sorted(all_points, key=lambda pt: math.atan2(pt[1] - yc, pt[0] - xc))
    
    t.penup()
    t.goto(sorted_points[0])
    t.pendown()
    for point in sorted_points:
        t.goto(point)
    t.goto(sorted_points[0])

def draw_polygon(n, size, x, y, color="green"):
    """
    Menggambar poligon beraturan dengan n sisi
    Bisa dibuat sendiri tanpa library grafis lain
    """
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    
    angle = 360 / n
    
    for i in range(n):
        t.forward(size)
        t.right(angle)

# ==================== DEMONSTRASI ====================

# Judul
t.penup()
t.goto(0, 250)
t.color("black")
t.write("Praktikum: Menggambar Garis, Lingkaran, dan Poligon", 
        align="center", font=("Arial", 14, "bold"))

# 1. Menggambar Garis dengan DDA
t.penup()
t.goto(-350, 200)
t.write("1. Garis DDA", align="left", font=("Arial", 10, "normal"))
dda_line(-300, 150, -100, 180, "black")

# 2. Menggambar Garis dengan Bresenham
t.penup()
t.goto(-350, 100)
t.write("2. Garis Bresenham", align="left", font=("Arial", 10, "normal"))
bresenham_line(-300, 50, -100, 80, "blue")

# 3. Menggambar Lingkaran dengan Midpoint Circle
t.penup()
t.goto(-350, -50)
t.write("3. Lingkaran Midpoint", align="left", font=("Arial", 10, "normal"))
midpoint_circle(-200, -100, 50, "red")

# 4. Menggambar Poligon (Segitiga)
t.penup()
t.goto(50, 200)
t.write("4. Segitiga", align="left", font=("Arial", 10, "normal"))
draw_polygon(3, 80, 100, 150, "green")

# 5. Menggambar Poligon (Segi Enam)
t.penup()
t.goto(50, 50)
t.write("5. Segi Enam", align="left", font=("Arial", 10, "normal"))
draw_polygon(6, 50, 150, 20, "purple")

# 6. Menggambar Poligon (Bintang - Segi Delapan)
t.penup()
t.goto(50, -100)
t.write("6. Segi Delapan", align="left", font=("Arial", 10, "normal"))
draw_polygon(8, 40, 150, -130, "orange")

# Hide turtle dan tampilkan hasil
t.hideturtle()

# Informasi
t.penup()
t.goto(0, -250)
t.color("gray")
t.write("Program menggunakan Python + Turtle (tanpa library grafis lain)", 
        align="center", font=("Arial", 9, "italic"))

# Tutup window saat diklik
screen.exitonclick() 