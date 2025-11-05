lebar = 10
tinggi = 10

x1, y1 = 0, 0
x2, y2 = 5, 3

grid = [["." for _ in range(lebar)] for _ in range(tinggi)]

dx = x2 - x1
dy = y2 - y1

steps = max(abs(dx), abs(dy))

x_inc = dx / steps
y_inc = dy / steps

x = x1
y = y1

for i in range(steps + 1):
    grid[int(round(y))][int(round(x))] = "x"
    x += x_inc
    y += y_inc
    
for baris in grid:
    print(" ".join(baris))