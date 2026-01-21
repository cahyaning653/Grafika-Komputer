from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random, math

app = Ursina()
window.color = color.rgb(135, 206, 235)

# ================= KARAKTER ROBLOX =================
class RobloxCharacter(Entity):
    def __init__(self, position=(0,0,0), body_color=color.azure):
        super().__init__(position=position)

        # Badan
        self.torso = Entity(model='cube', scale=(1,1.2,0.6),
                            color=body_color, parent=self)

        # Kepala
        self.head = Entity(model='cube', scale=0.8, y=1,
                           color=color.rgb(255,220,177), parent=self)

        # Tangan
        self.left_arm = Entity(model='cube', scale=(0.35,1.2,0.35),
                               x=-0.7, origin=(0,0.6,0),
                               color=color.rgb(255,220,177), parent=self)

        self.right_arm = Entity(model='cube', scale=(0.35,1.2,0.35),
                                x=0.7, origin=(0,0.6,0),
                                color=color.rgb(255,220,177), parent=self)

        # Kaki
        self.left_leg = Entity(model='cube', scale=(0.4,1.2,0.4),
                               x=-0.25, y=-1.2, origin=(0,0.6,0),
                               color=color.rgb(60,60,60), parent=self)

        self.right_leg = Entity(model='cube', scale=(0.4,1.2,0.4),
                                x=0.25, y=-1.2, origin=(0,0.6,0),
                                color=color.rgb(60,60,60), parent=self)

        self.anim = random.random() * 10
        self.dir = Vec3(random.uniform(-1,1),0,random.uniform(-1,1)).normalized()
        self.speed = random.uniform(1.2, 2)

    def walk(self):
        self.anim += time.dt * 6
        s = math.sin(self.anim)

        self.left_arm.rotation_x = s * 45
        self.right_arm.rotation_x = -s * 45
        self.left_leg.rotation_x = -s * 30
        self.right_leg.rotation_x = s * 30

        self.position += self.dir * self.speed * time.dt
        self.rotation_y = math.degrees(math.atan2(self.dir.x, self.dir.z))

        if abs(self.x) > 55 or abs(self.z) > 55:
            self.dir *= -1

# ================= TANAH =================
ground = Entity(
    model='plane',
    scale=150,
    texture='white_cube',
    texture_scale=(75,75),
    color=color.rgb(70,150,70),
    collider='box'
)

# ================= POHON DETAIL =================
def tree(pos):
    # Batang
    Entity(model='cube', scale=(0.8,4,0.8),
           position=(pos[0],2,pos[2]),
           color=color.rgb(101,67,33))
    # Daun
    Entity(model='sphere', scale=3,
           position=(pos[0],5,pos[2]),
           color=color.rgb(34,139,34))
    Entity(model='sphere', scale=2.2,
           position=(pos[0],6.7,pos[2]),
           color=color.rgb(50,160,50))

for _ in range(30):
    tree((random.uniform(-50,50),0,random.uniform(-50,50)))

# ================= CANDI (BATU) =================
def candi(pos):
    for i in range(4):
        Entity(
            model='cube',
            scale=(6-i, 1.2, 6-i),
            position=(pos[0], pos[1]+i*1.2, pos[2]),
            color=color.rgb(120,120,120)
        )
    Entity(
        model='cube',
        scale=(2,2,2),
        position=(pos[0], pos[1]+5, pos[2]),
        color=color.rgb(150,150,150)
    )

candi((20,0,20))
candi((-25,0,25))

# ================= RUMAH DESA =================
def house(pos):
    Entity(model='cube', scale=(6,3,6),
           position=(pos[0],1.5,pos[2]),
           color=color.rgb(200,180,140))
    Entity(model='cube', scale=(6.5,2,6.5),
           position=(pos[0],4,pos[2]),
           color=color.rgb(150,50,50))

for _ in range(5):
    house((random.uniform(-40,40),0,random.uniform(-40,40)))

# ================= PLAYER =================
player_char = RobloxCharacter((0,2,-20), color.orange)
player = FirstPersonController(position=(0,2,-20), speed=6)
player.gravity = 0.5
player_char.parent = player
player_char.y = -1.5

# ================= NPC =================
npc_colors = [color.red, color.green, color.yellow, color.cyan, color.violet]
npcs = []

for _ in range(7):
    npc = RobloxCharacter(
        (random.uniform(-30,30),0,random.uniform(-30,30)),
        random.choice(npc_colors)
    )
    npcs.append(npc)

# ================= SKY =================
Sky()

# ================= UPDATE =================
def update():
    if held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']:
        player_char.walk()

    for npc in npcs:
        npc.walk()

def input(key):
    if key == 'escape':
        application.quit()

mouse.locked = True
app.run()
