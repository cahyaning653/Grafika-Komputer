from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# ===== KARAKTER ROBLOX STYLE =====
class RobloxCharacter(Entity):
    def __init__(self, position=(0,0,0), body_color=color.blue, is_player=False):
        super().__init__()
        self.position = position
        self.is_player = is_player
        
        # Torso
        self.torso = Entity(
            model='cube',
            color=body_color,
            scale=(1, 1.2, 0.6),
            parent=self,
            texture='white_cube'
        )
        
        # Head
        head_color = color.rgb(255, 220, 177) if not is_player else color.rgb(255, 200, 150)
        self.head = Entity(
            model='cube',
            color=head_color,
            scale=(0.8, 0.8, 0.8),
            position=(0, 1, 0),
            parent=self,
            texture='white_cube'
        )
        
        # Face
        self.left_eye = Entity(
            model='cube',
            color=color.white,
            scale=(0.15, 0.2, 0.05),
            position=(-0.2, 1.1, 0.41),
            parent=self,
            texture='white_cube'
        )
        # Pupil left
        Entity(
            model='cube',
            color=color.rgb(0, 100, 200),
            scale=(0.08, 0.12, 0.03),
            position=(-0.2, 1.1, 0.43),
            parent=self
        )
        
        self.right_eye = Entity(
            model='cube',
            color=color.white,
            scale=(0.15, 0.2, 0.05),
            position=(0.2, 1.1, 0.41),
            parent=self,
            texture='white_cube'
        )
        # Pupil right
        Entity(
            model='cube',
            color=color.rgb(0, 100, 200),
            scale=(0.08, 0.12, 0.03),
            position=(0.2, 1.1, 0.43),
            parent=self
        )
        
        self.smile = Entity(
            model='cube',
            color=color.rgb(200, 100, 100),
            scale=(0.4, 0.1, 0.05),
            position=(0, 0.85, 0.41),
            parent=self,
            texture='white_cube'
        )
        
        # Arms
        arm_color = color.rgb(255, 220, 177) if not is_player else color.rgb(255, 200, 150)
        self.left_arm = Entity(
            model='cube',
            color=arm_color,
            scale=(0.35, 1.2, 0.35),
            position=(-0.7, 0, 0),
            origin=(0, 0.6, 0),
            parent=self,
            texture='white_cube'
        )
        self.right_arm = Entity(
            model='cube',
            color=arm_color,
            scale=(0.35, 1.2, 0.35),
            position=(0.7, 0, 0),
            origin=(0, 0.6, 0),
            parent=self,
            texture='white_cube'
        )
        
        # Legs
        pants_color = color.rgb(40, 116, 166) if is_player else color.rgb(85, 85, 85)
        self.left_leg = Entity(
            model='cube',
            color=pants_color,
            scale=(0.4, 1.2, 0.4),
            position=(-0.25, -1.2, 0),
            origin=(0, 0.6, 0),
            parent=self,
            texture='white_cube'
        )
        self.right_leg = Entity(
            model='cube',
            color=pants_color,
            scale=(0.4, 1.2, 0.4),
            position=(0.25, -1.2, 0),
            origin=(0, 0.6, 0),
            parent=self,
            texture='white_cube'
        )
        
        self.animation_time = random.uniform(0, 3.14)
        self.walk_speed = 2
        self.direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()
        
    def animate_walk(self, is_moving=True):
        if is_moving:
            self.animation_time += time.dt * 8
            
            # Swing arms
            swing = math.sin(self.animation_time) * 45
            self.left_arm.rotation_x = swing
            self.right_arm.rotation_x = -swing
            
            # Swing legs
            leg_swing = math.sin(self.animation_time) * 30
            self.left_leg.rotation_x = leg_swing
            self.right_leg.rotation_x = -leg_swing
            
            # Bob head
            self.head.y = 1 + abs(math.sin(self.animation_time * 2)) * 0.05
        else:
            # Reset to idle
            self.left_arm.rotation_x = lerp(self.left_arm.rotation_x, 0, time.dt * 5)
            self.right_arm.rotation_x = lerp(self.right_arm.rotation_x, 0, time.dt * 5)
            self.left_leg.rotation_x = lerp(self.left_leg.rotation_x, 0, time.dt * 5)
            self.right_leg.rotation_x = lerp(self.right_leg.rotation_x, 0, time.dt * 5)

# ===== NPC CLIMBER =====
class ClimberNPC(RobloxCharacter):
    def __init__(self, position, body_color):
        super().__init__(position, body_color, is_player=False)
        self.climb_timer = 0
        self.climb_target = Vec3(random.uniform(-15, 15), position[1] + random.uniform(5, 15), random.uniform(-15, 15))
        
    def update(self):
        # Simple climbing AI
        direction = (self.climb_target - self.position).normalized()
        
        if distance(self.position, self.climb_target) > 1:
            self.position += direction * self.walk_speed * time.dt
            
            # Face direction
            if direction.length() > 0:
                angle = math.degrees(math.atan2(direction.x, direction.z))
                self.rotation_y = angle
                self.animate_walk(True)
        else:
            # New target when reached
            self.climb_target = Vec3(random.uniform(-15, 15), random.uniform(5, 25), random.uniform(-15, 15))
            self.animate_walk(False)

# ===== MOUNTAIN COLLECTIBLES =====
class MountainFlag(Entity):
    def __init__(self, position):
        super().__init__(
            model='cube',
            color=color.rgb(255, 50, 50),
            scale=(0.2, 3, 0.2),
            position=position,
            collider='box'
        )
        # Flag cloth
        self.flag = Entity(
            model='cube',
            color=color.rgb(255, 200, 0),
            scale=(2, 1.5, 0.1),
            position=(position[0] + 1, position[1] + 2, position[2]),
            parent=self
        )
        self.wave_time = random.uniform(0, 6.28)
        self.original_y = position[1]
        self.points = 50
        
    def update(self):
        self.wave_time += time.dt * 3
        # Wave flag
        self.flag.rotation_y = math.sin(self.wave_time * 2) * 15

class Crystal(Entity):
    def __init__(self, position, crystal_color=color.cyan):
        super().__init__(
            model='cube',
            color=crystal_color,
            scale=0.6,
            position=position,
            collider='box',
            texture='white_cube'
        )
        self.float_time = random.uniform(0, 6.28)
        self.original_y = position[1]
        self.points = 10
        
    def update(self):
        self.float_time += time.dt * 2
        self.y = self.original_y + math.sin(self.float_time) * 0.3
        self.rotation_y += time.dt * 100

# ===== CREATE MOUNTAIN TERRAIN =====
def create_mountain_peak(position, size=10, height=15):
    """Create a pyramid-shaped mountain with natural colors"""
    levels = 8
    for i in range(levels):
        level_height = (height / levels) * i
        level_scale = size * (1 - i / levels)
        
        # Natural rock colors - browns and grays
        rock_colors = [
            color.rgb(115, 90, 70),    # Brown rock
            color.rgb(105, 85, 65),    # Dark brown
            color.rgb(125, 100, 80),   # Light brown
            color.rgb(95, 95, 85),     # Gray brown
            color.rgb(110, 95, 75)     # Medium brown
        ]
        
        Entity(
            model='cube',
            color=random.choice(rock_colors),
            scale=(level_scale, height/levels, level_scale),
            position=(position[0], position[1] + level_height, position[2]),
            collider='box',
            texture='white_cube'
        )
    
    # Snow on top - pure white
    Entity(
        model='cube',
        color=color.rgb(250, 250, 255),
        scale=(size * 0.35, 2.5, size * 0.35),
        position=(position[0], position[1] + height + 1.2, position[2]),
        texture='white_cube'
    )

# ===== SETUP WORLD =====
# Base ground - Natural grass with variation
ground = Entity(
    model='plane',
    texture='white_cube',
    scale=150,
    color=color.rgb(65, 140, 65),
    collider='box',
    texture_scale=(75, 75)
)

# Add grass patches with color variation
for i in range(50):
    grass_colors = [
        color.rgb(60, 130, 60),
        color.rgb(70, 145, 70),
        color.rgb(55, 125, 55),
        color.rgb(65, 135, 65)
    ]
    Entity(
        model='plane',
        color=random.choice(grass_colors),
        scale=random.uniform(5, 12),
        position=(random.uniform(-70, 70), 0.02, random.uniform(-70, 70)),
        rotation_y=random.uniform(0, 360)
    )

# Create multiple mountain peaks
create_mountain_peak((0, 0, 30), 15, 20)
create_mountain_peak((-25, 0, 20), 12, 15)
create_mountain_peak((25, 0, 15), 10, 12)
create_mountain_peak((-15, 0, -20), 8, 10)
create_mountain_peak((20, 0, -15), 14, 18)

# Add mountain paths/slopes with natural earth tones
for i in range(20):
    earth_colors = [
        color.rgb(105, 85, 65),   # Dark earth
        color.rgb(115, 95, 75),   # Medium earth
        color.rgb(125, 105, 85),  # Light earth
        color.rgb(100, 80, 60)    # Deep earth
    ]
    Entity(
        model='cube',
        color=random.choice(earth_colors),
        scale=(random.uniform(3, 6), random.uniform(1, 3), random.uniform(3, 6)),
        position=(random.uniform(-30, 30), random.uniform(0, 8), random.uniform(-30, 30)),
        rotation=(0, random.uniform(0, 360), 0),
        collider='box',
        texture='white_cube'
    )

# Player
player_char = RobloxCharacter(position=(0, 2, -20), body_color=color.rgb(255, 100, 50), is_player=True)

# First Person Controller
player_controller = FirstPersonController(
    position=(0, 2, -20),
    mouse_sensitivity=Vec2(40, 40),
    speed=6
)
player_controller.cursor.visible = False
player_controller.gravity = 0.5

# Attach player model
player_char.parent = player_controller
player_char.y = -1.5

# Sky - Natural gradient (sunrise/sunset effect)
class NaturalSky(Entity):
    def __init__(self):
        super().__init__(
            model='sphere',
            scale=500,
            double_sided=True
        )
        
        # Create gradient sky dome
        # Bottom: warm orange/yellow (horizon)
        # Top: blue sky
        self.color = color.rgb(135, 206, 250)  # Sky blue
        
        # Add horizon glow
        self.horizon = Entity(
            model='sphere',
            scale=480,
            color=color.rgb(255, 200, 150),
            alpha=0.3,
            double_sided=True
        )

sky = NaturalSky()

# Add realistic clouds with depth
clouds = []
for i in range(25):
    cloud_y = random.uniform(20, 45)
    cloud = Entity(
        model='sphere',
        color=color.rgb(255, 255, 255),
        scale=(random.uniform(8, 15), random.uniform(3, 6), random.uniform(8, 15)),
        position=(random.uniform(-80, 80), cloud_y, random.uniform(-80, 80)),
        alpha=random.uniform(0.6, 0.9)
    )
    clouds.append(cloud)

# Sun with warm glow
sun = Entity(
    model='sphere',
    color=color.rgb(255, 230, 100),
    scale=15,
    position=(60, 50, 70)
)

# Sun glow effect
Entity(
    model='sphere',
    color=color.rgba(255, 200, 100, 100),
    scale=25,
    position=(60, 50, 70)
)

# Distant mountains (background)
for i in range(8):
    dist_x = random.uniform(-100, 100)
    dist_z = random.uniform(50, 100)
    Entity(
        model='cube',
        color=color.rgb(80, 100, 130),
        scale=(random.uniform(20, 40), random.uniform(15, 30), random.uniform(20, 30)),
        position=(dist_x, random.uniform(5, 15), dist_z),
        alpha=0.6
    )

# Spawn Climber NPCs
npcs = []
climber_colors = [
    color.rgb(231, 76, 60),      # Red
    color.rgb(46, 204, 113),     # Green
    color.rgb(241, 196, 15),     # Yellow
    color.rgb(155, 89, 182),     # Purple
]

for i in range(4):
    pos = (random.uniform(-15, 15), random.uniform(2, 8), random.uniform(-15, 15))
    npc = ClimberNPC(pos, climber_colors[i])
    npcs.append(npc)

# Mountain Flags (main objectives)
flags = []
flag_positions = [
    (0, 22, 30),      # Top of main peak
    (-25, 17, 20),    # Second peak
    (25, 14, 15),     # Third peak
    (20, 20, -15)     # Fourth peak
]

for pos in flag_positions:
    flag = MountainFlag(pos)
    flags.append(flag)

# Crystals scattered around
crystals = []
crystal_colors = [
    color.rgb(0, 200, 255),
    color.rgb(255, 100, 255),
    color.rgb(100, 255, 100),
    color.rgb(255, 255, 100)
]

for i in range(12):
    pos = (random.uniform(-30, 30), random.uniform(3, 15), random.uniform(-30, 30))
    crystal = Crystal(pos, random.choice(crystal_colors))
    crystals.append(crystal)

# Trees at base - Natural green variations
for i in range(20):
    tree_pos = (random.uniform(-50, 50), 0, random.uniform(-50, 50))
    
    # Trunk - natural brown bark
    trunk_colors = [
        color.rgb(101, 67, 33),
        color.rgb(90, 60, 30),
        color.rgb(110, 75, 40)
    ]
    Entity(
        model='cube',
        color=random.choice(trunk_colors),
        scale=(0.7, random.uniform(3.5, 5), 0.7),
        position=(tree_pos[0], 2.5, tree_pos[2]),
        texture='white_cube'
    )
    
    # Leaves - forest green variations
    leaf_colors = [
        color.rgb(34, 139, 34),   # Forest green
        color.rgb(40, 150, 40),   # Bright green
        color.rgb(30, 130, 30),   # Dark green
        color.rgb(45, 160, 45)    # Light green
    ]
    Entity(
        model='cube',
        color=random.choice(leaf_colors),
        scale=(random.uniform(2.5, 3.5), random.uniform(2.5, 3.5), random.uniform(2.5, 3.5)),
        position=(tree_pos[0], 5.5, tree_pos[2]),
        texture='white_cube'
    )

# Bushes and small plants
for i in range(30):
    bush_pos = (random.uniform(-50, 50), 0, random.uniform(-50, 50))
    Entity(
        model='sphere',
        color=color.rgb(random.randint(30, 50), random.randint(120, 150), random.randint(30, 50)),
        scale=random.uniform(0.8, 1.5),
        position=(bush_pos[0], 0.5, bush_pos[2]),
        texture='white_cube'
    )

# Rocks - Natural gray and brown stones
for i in range(30):
    rock_colors = [
        color.rgb(100, 100, 95),   # Light gray
        color.rgb(80, 80, 75),     # Dark gray
        color.rgb(110, 95, 80),    # Brown-gray
        color.rgb(90, 85, 80)      # Medium gray
    ]
    Entity(
        model='sphere',
        color=random.choice(rock_colors),
        scale=random.uniform(0.5, 2.5),
        position=(random.uniform(-50, 50), 0.3, random.uniform(-50, 50)),
        texture='white_cube'
    )

# Add some flowers for color
flower_colors = [
    color.rgb(255, 100, 100),  # Red flowers
    color.rgb(255, 255, 100),  # Yellow flowers
    color.rgb(200, 100, 255),  # Purple flowers
    color.rgb(255, 150, 200)   # Pink flowers
]

for i in range(40):
    flower_pos = (random.uniform(-45, 45), 0, random.uniform(-45, 45))
    Entity(
        model='sphere',
        color=random.choice(flower_colors),
        scale=0.3,
        position=(flower_pos[0], 0.2, flower_pos[2])
    )

# UI
score = 0
flags_collected = 0

score_text = Text(
    text='Score: 0',
    position=window.top_left,
    origin=(-0.5, 0.5),
    scale=2,
    color=color.gold,
    background=True
)

flags_text = Text(
    text='Flags: 0/4',
    position=window.top_left,
    origin=(-0.5, 1.5),
    scale=2,
    color=color.red,
    background=True
)

instruction_text = Text(
    text='🏔️ Mountain Climbing! Reach the peaks and plant flags! | WASD: Move | SPACE: Jump | Mouse: Look | ESC: Exit',
    position=(0, 0.48),
    origin=(0, 0),
    scale=1.3,
    background=True
)

gem_info = Text(
    text='💎 Crystals: 10pts | 🚩 Flags: 50pts | Climb to the top!',
    position=(0, -0.48),
    origin=(0, 0),
    scale=1.2,
    color=color.white,
    background=True
)

def update():
    global score, flags_collected
    
    # Animate player walking
    is_moving = held_keys['w'] or held_keys['s'] or held_keys['a'] or held_keys['d']
    player_char.animate_walk(is_moving)
    
    # Animate clouds slowly
    for cloud in clouds:
        cloud.x += time.dt * 0.5
        if cloud.x > 100:
            cloud.x = -100
    
    # Collect crystals
    for crystal in crystals[:]:
        dist = distance(player_controller.position, crystal.position)
        if dist < 2:
            score += crystal.points
            score_text.text = f'Score: {score}'
            destroy(crystal)
            crystals.remove(crystal)
    
    # Collect flags
    for flag in flags[:]:
        dist = distance(player_controller.position, flag.position)
        if dist < 2.5:
            score += flag.points
            flags_collected += 1
            score_text.text = f'Score: {score}'
            flags_text.text = f'Flags: {flags_collected}/4'
            destroy(flag)
            flags.remove(flag)
    
    # Win condition
    if flags_collected >= 4:
        instruction_text.text = f'🎉 YOU CONQUERED THE MOUNTAIN! Final Score: {score} 🎉'
        instruction_text.color = color.green
        instruction_text.scale = 2

def input(key):
    if key == 'escape':
        application.quit()

mouse.locked = True
app.run()