import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle
from matplotlib.animation import FuncAnimation
import math, random, time

# ========== TRANSFORMASI 2D ==========
def translasi(points, dx, dy):
    T = np.array([[1, 0, dx],
                  [0, 1, dy],
                  [0, 0, 1]])
    P = np.vstack([points.T, np.ones(points.shape[0])])
    return (T @ P)[:2].T

def rotasi(points, angle_deg, pivot):
    rad = np.radians(angle_deg)
    R = np.array([[np.cos(rad), -np.sin(rad)],
                  [np.sin(rad), np.cos(rad)]])
    return ((R @ (points - pivot).T).T) + pivot

def skala(points, sx, sy, pivot):
    S = np.array([[sx, 0],
                  [0, sy]])
    return ((S @ (points - pivot).T).T) + pivot

def refleksi_y(points):
    R = np.array([[-1, 0],
                  [0, 1]])
    return (R @ points.T).T


# ========== KARAKTER UTAMA ==========
class Hero:
    def __init__(self, ax, x, y):
        self.ax = ax
        self.x, self.y = x, y
        self.vy = 0
        self.facing_right = True
        self.on_ground = True
        self.attack = False
        self.frame = 0
        self.hp = 3

        # Transformasi tambahan
        self.scale = 1.0
        self.scale_timer = 0
        self.spinning = False
        self.spin_angle = 0

        self.create_parts(ax, x, y)

    def create_parts(self, ax, x, y):
        s = self.scale

        self.head = Circle((x + 1, y + 4.5), 1*s, fc='#ffebc1', ec='black')
        self.hair = Polygon([[x, y + 5.3], [x + 2, y + 5.3], [x + 1, y + 6.2]],
                             fc='#7c3aed', ec='black')
        self.hat = Polygon([[x + 0.3, y + 5.5], [x + 1, y + 6.6], [x + 1.7, y + 5.5]],
                           fc='#dc2626', ec='black', lw=2)
        self.eye = Circle((x + 1.3, y + 4.7), 0.13*s, fc='black')

        self.body = Rectangle((x + 0.3, y + 2), 1.4*s, 2*s,
                              fc='#1d4ed8', ec='black')
        self.legL = Rectangle((x + 0.4, y + 1), 0.45*s, 1*s,
                              fc='#3b82f6', ec='black')
        self.legR = Rectangle((x + 1.1, y + 1), 0.45*s, 1*s,
                              fc='#3b82f6', ec='black')

        sw = np.array([[x + 2.2, y + 2.3],
                       [x + 4.2, y + 2.5],
                       [x + 4.2, y + 2.1],
                       [x + 2.2, y + 2.0]])
        self.sword = Polygon(sw, fc='silver', ec='gray', lw=3)

        self.parts = [self.head, self.hair, self.hat, self.eye,
                      self.body, self.legL, self.legR, self.sword]

        for p in self.parts:
            ax.add_patch(p)

    def scale_up(self):
        self.scale = 1.5
        self.scale_timer = time.time()

    def update_scale(self):
        if self.scale > 1 and time.time() - self.scale_timer > 2:
            self.scale = 1.0
            for p in self.parts: p.remove()
            self.create_parts(self.ax, self.x, self.y)

    def spin_attack(self):
        self.spinning = True
        self.spin_angle = 0  # reset spin

    def move(self, dx):
        self.x += dx
        self.facing_right = dx > 0
        self.update()

    def jump(self):
        if self.on_ground:
            self.vy = 9
            self.on_ground = False

    def attack_sword(self):
        self.attack = True
        self.frame = 0

    def update(self):
        self.update_scale()

        self.y += self.vy * 0.1
        self.vy -= 0.48
        if self.y <= 0:
            self.y = 0
            self.on_ground = True

        self.frame += 1
        bounce = math.sin(self.frame*0.4)*0.12

        # ROTASI tubuh saat spin attack
        if self.spinning:
            pivot = np.array([self.x+1, self.y+3])
            for p in self.parts:
                if isinstance(p, Polygon):
                    p.set_xy(rotasi(p.get_xy(), 7, pivot))
            self.spin_angle += 7
            if self.spin_angle >= 360:
                self.spinning = False

        # Update posisi tubuh
        self.head.center = (self.x + 1, self.y + 4.5 + bounce)
        self.eye.center = (self.x + (1.3 if self.facing_right else .7),
                           self.y + 4.7 + bounce)
        self.hair.set_xy([[self.x, self.y+5.3+bounce],
                          [self.x+2, self.y+5.3+bounce],
                          [self.x+1, self.y+6.2+bounce]])
        self.hat.set_xy([[self.x+0.3, self.y+5.5+bounce],
                         [self.x+1, self.y+6.6+bounce],
                         [self.x+1.7, self.y+5.5+bounce]])
        self.body.set_xy((self.x + 0.3, self.y + 2 + bounce))

        # Translasi kaki
        step = math.sin(self.frame*0.5)*0.4
        self.legL.set_xy((self.x + 0.4 + step, self.y+1))
        self.legR.set_xy((self.x + 1.1 - step, self.y+1))

        # Pedang
        sw = np.array([[self.x + 2.2, self.y + 2.3],
                       [self.x + 4.2, self.y + 2.5],
                       [self.x + 4.2, self.y + 2.1],
                       [self.x + 2.2, self.y + 2.0]])

        # Rotasi ketika attack
        if self.attack and not self.spinning:
            pivot = np.array([self.x+1.6, self.y+2.4])
            ang = -100 if self.facing_right else 100
            sw = rotasi(sw, ang, pivot)
            if self.frame > 10:
                self.attack = False

        # REFLEKSI saat menghadap kiri
        if not self.facing_right:
            sw[:, 0] = 2*(self.x + 1) - sw[:, 0]

        self.sword.set_xy(sw)


# ========== MUSUH KUMAN ==========
class Enemy:
    def __init__(self, ax, x, y, speed=1):
        self.x, self.y = x, y
        self.speed = speed
        self.hp = 1
        self.body = Circle((x, y+1.3), 1.1,
                           fc='#34d399', ec='black')
        ax.add_patch(self.body)

    def update(self, hx):
        if self.hp > 0:
            self.x += 0.06*np.sign(hx-self.x)*self.speed
            self.body.center = (self.x, self.y+1.3)

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.body.set_alpha(0)


# ========== SCENE (Background Gunung) ==========
fig, ax = plt.subplots(figsize=(15, 8))
ax.set_xlim(-50, 50)
ax.set_ylim(-5, 30)
ax.axis('off')

ax.add_patch(Rectangle((-60,-5),120,40,fc='#bfe8ff'))
mount = [[[-60,-5],[-10,25],[60,-5]],
         [[-45,-5],[5,18],[50,-5]]]
for m in mount:
    ax.add_patch(Polygon(m, fc='#4e6b50', ec='black'))
ax.add_patch(Rectangle((-60,-5),120,10,fc='#4ade80'))

# GAME STATE
hero = Hero(ax, -30, 0)
enemies = [Enemy(ax, 25, 0)]
keys = {'left':False,'right':False,'up':False,'space':False}
score = 0
level = 1
game_over = False

info = ax.text(-48,27,"",fontsize=12,color="white",
               bbox=dict(fc='black'))

# Input keyboard
def kd(e):
    if e.key=='left': keys['left']=True
    if e.key=='right': keys['right']=True
    if e.key=='up': keys['up']=True
    if e.key==' ': keys['space']=True

def ku(e):
    if e.key=='left': keys['left']=False
    if e.key=='right': keys['right']=False
    if e.key=='up': keys['up']=False
    if e.key==' ': keys['space']=False

fig.canvas.mpl_connect('key_press_event', kd)
fig.canvas.mpl_connect('key_release_event', ku)

# GAME LOOP
def animate(i):
    global score, level, game_over
    
    if game_over:
        info.set_text("💀 GAME OVER!    Score: "+str(score))
        return

    if keys['left']: hero.move(-.7)
    if keys['right']: hero.move(.7)
    if keys['up']: hero.jump()
    if keys['space']: hero.attack_sword()

    hero.update()

    for e in enemies:
        if e.hp>0:
            e.update(hero.x)

            sx,sy = hero.sword.get_xy()[1]
            ex,ey = e.body.center

            # Rotasi & Skala aktif saat kena musuh
            if abs(sx-ex)<2 and abs(sy-ey)<2 and hero.attack:
                e.hit()
                score += 10
                hero.spin_attack()
                hero.scale_up()

            hx,hy = hero.head.center
            if abs(hx-ex)<1.5 and abs(hy-ey)<2:
                hero.hp -= 1
                if hero.hp <= 0:
                    game_over = True

    if all(e.hp<=0 for e in enemies):  # Level naik
        level += 1
        for i in range(level+1):
            enemies.append(Enemy(ax, random.randint(-40,40), 0, speed=1+level*0.25))

    info.set_text(f"❤️ {hero.hp} | Score: {score} | Level: {level}")

anim = FuncAnimation(fig, animate, interval=18)
plt.show()
