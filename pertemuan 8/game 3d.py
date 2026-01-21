class Character3D:
    def __init__(self, position):
        self.position = list(position)
        self.velocity = [0, 0, 0]
        self.rotation_y = 0
        self.scale = 1.0
        self.target_scale = 1.0
        self.walk_cycle = 0
        self.is_walking = False
        self.is_running = False

        # Warna chibi bunny hoodie
        self.skin_color = (255, 230, 220)
        self.hood_color = (255, 180, 200)
        self.pants_color = (230, 230, 230)

    def update(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[2] += self.velocity[2] * dt
        self.velocity[0] *= 0.85
        self.velocity[2] *= 0.85

        if self.is_walking:
            self.walk_cycle += dt * (10 if self.is_running else 6)
        else:
            self.walk_cycle *= 0.9

    def move(self, direction, speed=5):
        ang = math.radians(self.rotation_y)
        if direction == 'forward':
            self.velocity[0] += math.sin(ang) * speed * 0.15
            self.velocity[2] += math.cos(ang) * speed * 0.15
            self.is_walking = True
        elif direction == 'backward':
            self.velocity[0] -= math.sin(ang) * speed * 0.15
            self.velocity[2] -= math.cos(ang) * speed * 0.15
            self.is_walking = True

    def rotate(self, angle):
        self.rotation_y += angle

    def get_vertices(self):
        s = self.scale
        bob = math.sin(self.walk_cycle * 2) * 0.15 if self.is_walking else 0
        swing = math.sin(self.walk_cycle) * 0.4 if self.is_walking else 0

        verts = []

        # ================= HEAD (BESAR) =================
        head_y = 2.8 * s + bob
        r = 0.8 * s
        for i in range(10):
            a = math.radians(i * 36)
            verts.append([math.cos(a)*r, head_y, math.sin(a)*r])

        # ================= BUNNY EARS =================
        verts += [
            [-0.4*s, head_y + 1.2*s, 0],
            [-0.25*s, head_y + 0.3*s, 0],
            [ 0.4*s, head_y + 1.2*s, 0],
            [ 0.25*s, head_y + 0.3*s, 0],
        ]

        # ================= BODY =================
        verts += [
            [-0.6*s, 1.8*s + bob, -0.4*s],
            [ 0.6*s, 1.8*s + bob, -0.4*s],
            [ 0.6*s, 1.8*s + bob,  0.4*s],
            [-0.6*s, 1.8*s + bob,  0.4*s],
            [-0.5*s, 0.6*s + bob, -0.3*s],
            [ 0.5*s, 0.6*s + bob, -0.3*s],
            [ 0.5*s, 0.6*s + bob,  0.3*s],
            [-0.5*s, 0.6*s + bob,  0.3*s],
        ]

        # ================= ARMS =================
        verts += [
            [ 0.7*s, 1.6*s + bob, 0],
            [ 1.1*s, 1.1*s + swing + bob, 0],
            [-0.7*s, 1.6*s + bob, 0],
            [-1.1*s, 1.1*s - swing + bob, 0],
        ]

        # ================= LEGS =================
        verts += [
            [ 0.25*s, 0.6*s + bob, 0],
            [ 0.25*s, -0.9*s + swing + bob, 0],
            [-0.25*s, 0.6*s + bob, 0],
            [-0.25*s, -0.9*s - swing + bob, 0],
        ]

        # ================= ROTATION =================
        if self.rotation_y != 0:
            a = math.radians(self.rotation_y)
            c, si = math.cos(a), math.sin(a)
            verts = [[x*c + z*si, y, -x*si + z*c] for x,y,z in verts]

        return verts
