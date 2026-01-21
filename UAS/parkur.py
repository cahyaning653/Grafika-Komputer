from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math

# Inisialisasi aplikasi
app = Ursina()

# Variabel game
game_state = {
    'stage': 1,
    'max_stage': 20,
    'deaths': 0,
    'time_elapsed': 0,
    'coins_collected': 0,
    'total_coins': 0,
    'checkpoint_pos': Vec3(0, 2, 0),
    'last_checkpoint': 0
}

# Sky
sky = Sky()

# Ground base yang lebih besar
ground = Entity(
    model='plane',
    scale=(100, 1, 100),
    texture='white_cube',
    color=color.rgb(40, 140, 40),
    collider='box',
    position=(0, -1, 0)
)

# Platform spawn yang lebih besar
spawn = Entity(
    model='cube',
    scale=(10, 1, 10),
    position=(0, 0, 0),
    color=color.rgb(60, 60, 60),
    collider='box'
)

# Text START
Text(
    text='START',
    parent=spawn,
    position=(0, 0.6, 0),
    scale=10,
    color=color.white,
    billboard=True
)

# Buat stages dengan jarak lebih mudah
stages = []
x_pos = 0
y_pos = 1.5
z_pos = 6

for i in range(game_state['max_stage']):
    # Platform sangat dekat dan mudah
    if i < 5:
        platform_size = 5
        y_gap = random.uniform(0.5, 0.8)
        z_gap = random.uniform(2, 2.5)
        stage_color = color.rgb(100, 200, 100)
    elif i < 10:
        platform_size = 4.5
        y_gap = random.uniform(0.6, 1)
        z_gap = random.uniform(2.2, 2.8)
        stage_color = color.rgb(150, 200, 100)
    elif i < 15:
        platform_size = 4
        y_gap = random.uniform(0.8, 1.2)
        z_gap = random.uniform(2.5, 3)
        stage_color = color.rgb(200, 200, 100)
    else:
        platform_size = 3.5
        y_gap = random.uniform(1, 1.4)
        z_gap = random.uniform(2.8, 3.5)
        stage_color = color.rgb(200, 150, 100)
    
    x_pos = random.uniform(-2, 2)
    y_pos += y_gap
    z_pos += z_gap
    
    platform = Entity(
        model='cube',
        scale=(platform_size, 0.6, platform_size),
        position=(x_pos, y_pos, z_pos),
        color=stage_color,
        collider='box'
    )
    platform.stage_number = i + 1
    
    # Text nomor stage yang lebih besar
    txt = Text(
        text=str(i + 1),
        parent=platform,
        position=(0, 0.4, 0),
        scale=8,
        color=color.white,
        billboard=True
    )
    
    stages.append(platform)

# Puncak lebih dekat
summit_y = y_pos + 2
summit_z = z_pos + 4

summit = Entity(
    model='cube',
    scale=(8, 1, 8),
    position=(0, summit_y, summit_z),
    color=color.gold,
    collider='box'
)

# Text FINISH
Text(
    text='FINISH',
    parent=summit,
    position=(0, 0.6, 0),
    scale=10,
    color=color.white,
    billboard=True
)

# Bendera
flag_pole = Entity(
    model='cube',
    scale=(0.3, 5, 0.3),
    position=(0, summit_y + 3, summit_z),
    color=color.black
)

flag = Entity(
    model='cube',
    scale=(2, 1.2, 0.1),
    position=(1, summit_y + 4, summit_z),
    color=color.red
)

# Trophy
trophy = Entity(
    model='sphere',
    scale=1.2,
    position=(0, summit_y + 1.5, summit_z),
    color=color.gold
)

# Koin - lebih banyak dan lebih mudah diambil
coins = []
for stage in stages:
    coin = Entity(
        model='sphere',
        scale=0.6,
        position=stage.position + Vec3(0, 1.8, 0),
        color=color.yellow,
        collider='sphere'
    )
    coins.append(coin)

game_state['total_coins'] = len(coins)

# CHECKPOINT LAMPU (seperti Roblox!)
checkpoints = []
checkpoint_stages = [4, 8, 12, 16]

for cp_idx in checkpoint_stages:
    if cp_idx <= len(stages):
        cp_pos = stages[cp_idx - 1].position
        
        # Base checkpoint (platform lebih besar)
        cp_base = Entity(
            model='cube',
            scale=(6, 0.8, 6),
            position=cp_pos + Vec3(0, -0.2, 0),
            color=color.rgb(80, 80, 80),
            collider='box'
        )
        
        # Tiang lampu
        cp_pole = Entity(
            model='cylinder',
            scale=(0.3, 4, 0.3),
            position=cp_pos + Vec3(0, 2, 0),
            color=color.rgb(50, 50, 50)
        )
        
        # Lampu (bulat seperti Roblox)
        cp_light = Entity(
            model='sphere',
            scale=1.2,
            position=cp_pos + Vec3(0, 4.5, 0),
            color=color.red,  # Merah = belum aktif
            collider='sphere'
        )
        cp_light.activated = False
        cp_light.stage_num = cp_idx
        cp_light.cp_pos = cp_pos
        
        # Efek cahaya
        cp_glow = Entity(
            model='sphere',
            scale=1.5,
            position=cp_pos + Vec3(0, 4.5, 0),
            color=color.rgba(255, 0, 0, 100),
            alpha=0.3
        )
        cp_light.glow = cp_glow
        
        # Text checkpoint
        cp_text = Text(
            text=f'CHECKPOINT {len(checkpoints) + 1}',
            parent=cp_pole,
            position=(0, 3, 0),
            scale=6,
            color=color.white,
            billboard=True
        )
        
        checkpoints.append(cp_light)

# Platform bergerak - lebih dekat dengan stage utama
moving_platforms = []
for i in [6, 14]:
    if i < len(stages):
        plat = Entity(
            model='cube',
            scale=(4, 0.6, 4),
            position=stages[i].position + Vec3(2.5, 1.2, 0),
            color=color.violet,
            collider='box'
        )
        plat.start_x = plat.x
        plat.direction = 1
        moving_platforms.append(plat)

# Player dengan kemampuan lebih baik
player = FirstPersonController(
    position=(0, 2, 0),
    speed=6,  # Lebih cepat
    jump_height=2.5,  # Lompat lebih tinggi
    mouse_sensitivity=Vec2(100, 100)
)

# UI yang lebih jelas
ui_stage = Text(
    text=f'Stage: 1/{game_state["max_stage"]}',
    position=(-0.85, 0.46),
    scale=1.8,
    background=True,
    color=color.white
)

ui_checkpoint = Text(
    text='Last Checkpoint: START',
    position=(-0.85, 0.4),
    scale=1.4,
    background=True,
    color=color.lime
)

ui_deaths = Text(
    text='Deaths: 0',
    position=(-0.85, 0.34),
    scale=1.3,
    background=True,
    color=color.red
)

ui_time = Text(
    text='Time: 0s',
    position=(-0.85, 0.28),
    scale=1.3,
    background=True,
    color=color.cyan
)

ui_coins = Text(
    text=f'Coins: 0/{game_state["total_coins"]}',
    position=(-0.85, 0.22),
    scale=1.3,
    background=True,
    color=color.yellow
)

ui_hint = Text(
    text='Tip: Kumpulkan checkpoint lampu hijau untuk save!',
    position=(0, 0.46),
    scale=1.2,
    background=True,
    color=color.lime
)

ui_controls = Text(
    text='WASD-Move | SPACE-Jump | R-Respawn | ESC-Quit',
    position=(-0.85, -0.46),
    scale=1.1,
    background=True
)

ui_victory = Text(
    text='',
    position=(0, 0),
    scale=2.5,
    color=color.gold,
    background=True,
    visible=False
)

# Lighting lebih terang
light = DirectionalLight()
light.look_at(Vec3(1, -1, -1))
AmbientLight(color=Vec4(0.7, 0.7, 0.7, 1))

# Partikel efek untuk checkpoint
def create_checkpoint_effect(position):
    for i in range(10):
        particle = Entity(
            model='sphere',
            scale=0.2,
            position=position,
            color=color.lime
        )
        particle.animate_position(
            position + Vec3(random.uniform(-2, 2), random.uniform(1, 3), random.uniform(-2, 2)),
            duration=1,
            curve=curve.out_quad
        )
        particle.fade_out(duration=1)
        destroy(particle, delay=1)

def update():
    # Update timer
    game_state['time_elapsed'] += time.dt
    ui_time.text = f'Time: {int(game_state["time_elapsed"])}s'
    
    # Platform bergerak lebih lambat
    for plat in moving_platforms:
        plat.x += plat.direction * 1.5 * time.dt  # Lebih lambat
        if abs(plat.x - plat.start_x) > 6:  # Range lebih besar
            plat.direction *= -1
    
    # Rotasi koin
    for coin in coins:
        coin.rotation_y += 120 * time.dt
        coin.y += math.sin(time.time() * 3) * 0.01
    
    # Efek checkpoint lampu
    for cp in checkpoints:
        if not cp.activated:
            cp.rotation_y += 50 * time.dt
            # Efek berkedip untuk lampu yang belum aktif
            cp.glow.alpha = 0.2 + math.sin(time.time() * 3) * 0.1
        else:
            cp.glow.alpha = 0.4 + math.sin(time.time() * 5) * 0.2
    
    # Rotasi bendera dan trophy
    flag.rotation_y += 50 * time.dt
    trophy.rotation_y += 80 * time.dt
    trophy.y = summit_y + 1.5 + math.sin(time.time() * 2) * 0.2
    
    # Cek stage progress - radius lebih besar
    for stage in stages:
        dist = math.sqrt((player.x - stage.x)**2 + (player.z - stage.z)**2)
        if dist < 5 and abs(player.y - stage.y) < 3:
            if stage.stage_number > game_state['stage']:
                game_state['stage'] = stage.stage_number
                ui_stage.text = f'Stage: {game_state["stage"]}/{game_state["max_stage"]}'
    
    # Cek jatuh
    if player.y < -3:
        player.position = game_state['checkpoint_pos']
        player.rotation_y = 0
        game_state['deaths'] += 1
        ui_deaths.text = f'Deaths: {game_state["deaths"]}'
        print(f"Respawn ke checkpoint! Deaths: {game_state['deaths']}")
    
    # Cek victory
    dist_summit = math.sqrt((player.x - summit.x)**2 + (player.z - summit.z)**2)
    if dist_summit < 5 and player.y > summit_y - 1 and not ui_victory.visible:
        ui_victory.text = f'🏆 VICTORY! 🏆\nTime: {int(game_state["time_elapsed"])}s | Deaths: {game_state["deaths"]}\nCoins: {game_state["coins_collected"]}/{game_state["total_coins"]}'
        ui_victory.visible = True
        print("=" * 50)
        print("SELAMAT! PUNCAK TERCAPAI!")
        print(f"Waktu: {int(game_state['time_elapsed'])} detik")
        print(f"Deaths: {game_state['deaths']}")
        print(f"Koin: {game_state['coins_collected']}/{game_state['total_coins']}")
        print("=" * 50)

def input(key):
    if key == 'escape':
        quit()
    
    if key == 'r':
        player.position = game_state['checkpoint_pos']
        player.rotation_y = 0
        game_state['deaths'] += 1
        ui_deaths.text = f'Deaths: {game_state["deaths"]}'
        print("Respawn manual!")
    
    # Koleksi koin - radius lebih besar
    for coin in coins[:]:
        dist = math.sqrt((player.x - coin.x)**2 + (player.y - coin.y)**2 + (player.z - coin.z)**2)
        if dist < 2.5:
            destroy(coin)
            coins.remove(coin)
            game_state['coins_collected'] += 1
            ui_coins.text = f'Coins: {game_state["coins_collected"]}/{game_state["total_coins"]}'
            print(f"💰 Koin! Total: {game_state['coins_collected']}/{game_state['total_coins']}")
    
    # Checkpoint lampu - radius lebih besar
    for cp in checkpoints:
        if not cp.activated:
            dist = math.sqrt((player.x - cp.x)**2 + (player.y - cp.y)**2 + (player.z - cp.z)**2)
            if dist < 4:
                # Aktivasi checkpoint
                cp.activated = True
                cp.color = color.lime  # Hijau = aktif
                cp.glow.color = color.rgba(0, 255, 0, 150)
                
                # Update spawn point
                game_state['checkpoint_pos'] = Vec3(cp.cp_pos.x, cp.cp_pos.y + 1, cp.cp_pos.z)
                game_state['last_checkpoint'] = cp.stage_num
                
                # Update UI
                ui_checkpoint.text = f'Last Checkpoint: STAGE {cp.stage_num}'
                
                # Efek partikel
                create_checkpoint_effect(cp.position)
                
                print(f"✅ CHECKPOINT {cp.stage_num} ACTIVATED!")
                print(f"   Spawn point updated!")

# Info awal yang lebih detail
print("=" * 60)
print("🏔️  GAME PENDAKIAN GUNUNG 3D - EASY MODE")
print("=" * 60)
print("\n📦 INSTALASI:")
print("   Thonny → Tools → Manage packages → Install 'ursina'")
print("   Atau: pip install ursina")
print("\n🎮 KONTROL:")
print("   WASD       - Bergerak")
print("   SPACE      - Lompat (tinggi!)")
print("   Mouse      - Lihat sekeliling")
print("   R          - Respawn ke checkpoint")
print("   ESC        - Keluar")
print("\n💡 CHECKPOINT LAMPU:")
print("   🔴 MERAH  - Belum diaktifkan")
print("   🟢 HIJAU  - Sudah aktif (spawn point)")
print("\n🎯 FITUR:")
print("   ✓ Platform lebih besar dan jarak lebih dekat")
print("   ✓ Lompatan lebih tinggi")
print("   ✓ 4 Checkpoint lampu seperti Roblox")
print("   ✓ 20 Stage yang lebih mudah")
print("   ✓ Koin di setiap stage")
print("\n🏆 TARGET:")
print("   Capai puncak gunung dengan bendera merah!")
print("   Kumpulkan semua koin untuk perfect score!")
print("=" * 60)

# Jalankan game
app.run()