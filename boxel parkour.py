import pygame
import random
import sys
import os
import math

# --- HIGH SCORE, SEED & CHECKPOINT SETUP ---
if not os.path.exists("score.py"):
    with open("score.py", "w") as f:
        f.write("high_1 = 0\nhigh_2 = 0\nhigh_3 = 0\nhigh_4 = 0\nhigh_5 = 0\nhigh_6 = 0\nhigh_7 = 0\n")
        f.write(
            'seed_1 = "Very Easy"\nseed_2 = "Easy"\nseed_3 = "Medium"\nseed_4 = "Hard"\nseed_5 = "Nightmare"\nseed_6 = "Impossible"\nseed_7 = "Professional"\n')
        f.write("cp_1 = 0\ncp_2 = 0\ncp_3 = 0\ncp_4 = 0\ncp_5 = 0\ncp_6 = 0\ncp_7 = 0\n")
        f.write(
            "comp_1 = False\ncomp_2 = False\ncomp_3 = False\ncomp_4 = False\ncomp_5 = False\ncomp_6 = False\ncomp_7 = False\n")
        # Auto-activations and new settings default to True now
        f.write("auto_spice_activation = True\nauto_mushroom_activation = True\nauto_float_activation = True\n")
        f.write("achievement = True\ncolour = True\n")

import score

needs_patch = False
for i, name in enumerate(["Very Easy", "Easy", "Medium", "Hard", "Nightmare", "Impossible", "Professional"], 1):
    if not hasattr(score, f"seed_{i}"):
        setattr(score, f"seed_{i}", name)
        needs_patch = True
    val = getattr(score, f"cp_{i}", 0)
    if isinstance(val, dict) or val is None:
        setattr(score, f"cp_{i}", 0)
        needs_patch = True
    if not hasattr(score, f"comp_{i}"):
        setattr(score, f"comp_{i}", False)
        needs_patch = True

# Patch new variables if they don't exist, defaulting to True
for var in ["auto_spice_activation", "auto_mushroom_activation", "auto_float_activation", "achievement", "colour"]:
    if not hasattr(score, var):
        setattr(score, var, True)
        needs_patch = True


def save_scores():
    with open("score.py", "w") as f:
        f.write(
            f"high_1 = {getattr(score, 'high_1', 0)}\nhigh_2 = {getattr(score, 'high_2', 0)}\nhigh_3 = {getattr(score, 'high_3', 0)}\n")
        f.write(
            f"high_4 = {getattr(score, 'high_4', 0)}\nhigh_5 = {getattr(score, 'high_5', 0)}\nhigh_6 = {getattr(score, 'high_6', 0)}\nhigh_7 = {getattr(score, 'high_7', 0)}\n")
        f.write(
            f'seed_1 = "{getattr(score, "seed_1", "Very Easy")}"\nseed_2 = "{getattr(score, "seed_2", "Easy")}"\nseed_3 = "{getattr(score, "seed_3", "Medium")}"\n')
        f.write(
            f'seed_4 = "{getattr(score, "seed_4", "Hard")}"\nseed_5 = "{getattr(score, "seed_5", "Nightmare")}"\nseed_6 = "{getattr(score, "seed_6", "Impossible")}"\nseed_7 = "{getattr(score, "seed_7", "Professional")}"\n')
        f.write(
            f'cp_1 = {getattr(score, "cp_1", 0)}\ncp_2 = {getattr(score, "cp_2", 0)}\ncp_3 = {getattr(score, "cp_3", 0)}\n')
        f.write(
            f'cp_4 = {getattr(score, "cp_4", 0)}\ncp_5 = {getattr(score, "cp_5", 0)}\ncp_6 = {getattr(score, "cp_6", 0)}\ncp_7 = {getattr(score, "cp_7", 0)}\n')
        f.write(
            f'comp_1 = {getattr(score, "comp_1", False)}\ncomp_2 = {getattr(score, "comp_2", False)}\ncomp_3 = {getattr(score, "comp_3", False)}\n')
        f.write(
            f'comp_4 = {getattr(score, "comp_4", False)}\ncomp_5 = {getattr(score, "comp_5", False)}\ncomp_6 = {getattr(score, "comp_6", False)}\ncomp_7 = {getattr(score, "comp_7", False)}\n')
        f.write(f'auto_spice_activation = {getattr(score, "auto_spice_activation", True)}\n')
        f.write(f'auto_mushroom_activation = {getattr(score, "auto_mushroom_activation", True)}\n')
        f.write(f'auto_float_activation = {getattr(score, "auto_float_activation", True)}\n')
        f.write(f'achievement = {getattr(score, "achievement", True)}\n')
        f.write(f'colour = {getattr(score, "colour", True)}\n')


if needs_patch: save_scores()

# --- CONSTANTS & GLOBALS ---
WIDTH, HEIGHT = 800, 450
FPS = 60
BLOCK_SIZE = 40

GRAVITY = 0.5
JUMP_STRENGTH = -8.25
MAX_STOP_FRAMES = 8 * FPS
COOLDOWN_FRAMES = 10 * FPS
WIN_SCORE = 10000000

# Color Globals (will be updated by update_palette)
BG_COLOR = (25, 30, 45)
PLAYER_COLOR = (0, 255, 200)
BLOCK_COLOR = (120, 160, 255)
SPIKE_COLOR = (255, 70, 110)
GRID_COLOR = (45, 50, 65)
OUTLINE_COLOR = (20, 25, 40)
MOVING_OUTLINE = (255, 220, 80)
STAMINA_COLOR = (50, 240, 150)
CRUMBLE_COLOR = (255, 160, 50)
PHASE_OUTLINE = (180, 80, 255)
CHECKPOINT_OUTLINE = (100, 255, 255)
SLAB_COLOR = (150, 180, 220)


def update_palette():
    global BG_COLOR, PLAYER_COLOR, BLOCK_COLOR, SPIKE_COLOR, GRID_COLOR, OUTLINE_COLOR
    global MOVING_OUTLINE, STAMINA_COLOR, CRUMBLE_COLOR, PHASE_OUTLINE, CHECKPOINT_OUTLINE, SLAB_COLOR
    if getattr(score, "colour", True):
        BG_COLOR = (25, 30, 45)
        PLAYER_COLOR = (0, 255, 200)
        BLOCK_COLOR = (120, 160, 255)
        SPIKE_COLOR = (255, 70, 110)
        GRID_COLOR = (45, 50, 65)
        OUTLINE_COLOR = (20, 25, 40)
        MOVING_OUTLINE = (255, 220, 80)
        STAMINA_COLOR = (50, 240, 150)
        CRUMBLE_COLOR = (255, 160, 50)
        PHASE_OUTLINE = (180, 80, 255)
        CHECKPOINT_OUTLINE = (100, 255, 255)
        SLAB_COLOR = (150, 180, 220)
    else:
        BG_COLOR = (20, 20, 25)
        PLAYER_COLOR = (0, 200, 255)
        BLOCK_COLOR = (80, 80, 95)
        SPIKE_COLOR = (255, 50, 100)
        GRID_COLOR = (35, 35, 40)
        OUTLINE_COLOR = (10, 10, 15)
        MOVING_OUTLINE = (220, 180, 50)
        STAMINA_COLOR = (50, 220, 150)
        CRUMBLE_COLOR = (255, 140, 50)
        PHASE_OUTLINE = (150, 50, 255)
        CHECKPOINT_OUTLINE = (100, 200, 255)
        SLAB_COLOR = (120, 120, 130)


update_palette()

# Weights order: ["flat", "hill_up", "hill_down", "gentle_hill_up", "gentle_hill_down", "stairs_up", "stairs_down", "moving_platform", "crumble_platform", "phasing_platform", "mouth_gate", "ladder_climb", "stepping_stones", "phantom_mouth", "fade_platforms"]
DIFFICULTIES = [
    {"name": "Very Easy", "var": "high_1", "seed_var": "seed_1", "cp_var": "cp_1", "comp_var": "comp_1", "speed": 4.5,
     "gap_range": (1, 2), "spike_chance": 0.15, "max_spikes": 2,
     "weights": [80, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0], "color": (100, 255, 100)},
    {"name": "Easy", "var": "high_2", "seed_var": "seed_2", "cp_var": "cp_2", "comp_var": "comp_2", "speed": 5,
     "gap_range": (2, 2), "spike_chance": 0.30, "max_spikes": 2,
     "weights": [75, 2, 2, 10, 6, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0], "color": (150, 255, 50)},
    {"name": "Medium", "var": "high_3", "seed_var": "seed_3", "cp_var": "cp_3", "comp_var": "comp_3", "speed": 5.5,
     "gap_range": (2, 3), "spike_chance": 0.45, "max_spikes": 3,
     "weights": [60, 5, 5, 10, 10, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0], "color": (255, 255, 50)},
    {"name": "Hard", "var": "high_4", "seed_var": "seed_4", "cp_var": "cp_4", "comp_var": "comp_4", "speed": 6,
     "gap_range": (3, 3), "spike_chance": 0.65, "max_spikes": 3,
     "weights": [40, 8, 8, 7, 8, 7, 7, 15, 0, 0, 15, 5, 0, 0, 0], "color": (255, 150, 50)},
    {"name": "Nightmare", "var": "high_5", "seed_var": "seed_5", "cp_var": "cp_5", "comp_var": "comp_5", "speed": 6.5,
     "gap_range": (3, 4), "spike_chance": 0.85, "max_spikes": 4,
     "weights": [30, 10, 10, 4, 4, 8, 9, 20, 5, 0, 20, 5, 5, 0, 10], "color": (255, 50, 50)},
    {"name": "Impossible", "var": "high_6", "seed_var": "seed_6", "cp_var": "cp_6", "comp_var": "comp_6", "speed": 7.5,
     "gap_range": (4, 4), "spike_chance": 0.95, "max_spikes": 4,
     "weights": [30, 10, 10, 0, 0, 8, 7, 20, 10, 10, 20, 5, 0, 15, 15], "color": (150, 0, 255)},
    {"name": "Professional", "var": "high_7", "seed_var": "seed_7", "cp_var": "cp_7", "comp_var": "comp_7",
     "speed": 8.0, "gap_range": (4, 4), "spike_chance": 1.0, "max_spikes": 5,
     "weights": [30, 10, 10, 0, 0, 8, 7, 20, 10, 10, 20, 5, 0, 15, 15], "color": (255, 255, 255)}
]

# --- IMAGE LOADING ---
pygame.init()
SPICE_IMG = pygame.Surface((24, 24), pygame.SRCALPHA)
pygame.draw.circle(SPICE_IMG, (255, 140, 0), (12, 12), 12)
pygame.draw.circle(SPICE_IMG, (255, 230, 80), (12, 12), 6)

MUSHROOM_IMG = pygame.Surface((24, 24), pygame.SRCALPHA)
pygame.draw.circle(MUSHROOM_IMG, (180, 50, 220), (12, 12), 12)
pygame.draw.circle(MUSHROOM_IMG, (230, 120, 255), (12, 12), 6)

FLOAT_IMG = pygame.Surface((24, 24), pygame.SRCALPHA)
pygame.draw.circle(FLOAT_IMG, (255, 255, 255), (12, 12), 12)
pygame.draw.circle(FLOAT_IMG, (180, 250, 255), (12, 12), 6)


# --- DECORATIONS & VISUAL FEEDBACK ---
class ParallaxSparkle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(2, 5)
        self.speed_mult = random.uniform(0.1, 0.4)
        shade = random.randint(180, 255)
        self.color = (shade, shade, shade)
        self.pulse_offset = random.uniform(0, math.pi * 2)

    def draw(self, surface, cam_x, cam_y):
        draw_x = (self.x - cam_x * self.speed_mult) % WIDTH
        draw_y = (self.y - cam_y * self.speed_mult) % HEIGHT
        pulse = (math.sin(pygame.time.get_ticks() / 300.0 + self.pulse_offset) + 1) / 2
        cur_size = max(1, int(self.size * pulse))
        pygame.draw.circle(surface, self.color, (int(draw_x), int(draw_y)), cur_size)


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size_range=(3, 6), vy_range=(-5, -1)):
        super().__init__()
        self.x = x
        self.y = y
        self.vx = random.uniform(-3.0, 3.0)
        self.vy = random.uniform(vy_range[0], vy_range[1])
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.color = color
        self.size = random.randint(size_range[0], size_range[1])
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += GRAVITY * 0.4
        self.life -= 1
        self.rect.topleft = (int(self.x), int(self.y))

        if self.life <= 0:
            self.kill()

    def draw(self, surface, cam_x, cam_y):
        s = max(1, int(self.size * (self.life / self.max_life)))
        pygame.draw.rect(surface, self.color, (int(self.x - cam_x), int(self.y - cam_y), s, s), border_radius=2)


class PhantomMeteor(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, size):
        super().__init__()
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.rect = pygame.Rect(x - size, y - size, size * 2, size * 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (int(self.x), int(self.y))


# --- CLASSES ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = BLOCK_SIZE - 12
        self.reset()

    def reset(self):
        self.world_x = BLOCK_SIZE * 3
        self.y = BLOCK_SIZE * 2
        self.vy = 0
        self.on_ground = False
        self.on_ladder = False
        self.standing_on = None
        self.rect = pygame.Rect(self.world_x, self.y, self.size, self.size)
        self.prev_bottom = self.rect.bottom
        self.prev_right = self.rect.right
        self.last_safe_y = self.y
        self.coyote_frames = 0
        self.jump_buffer = 0
        self.angle = 0.0
        self.cp_index = 0

        # Skill Timers
        self.is_spiced = False
        self.spice_timer = 0
        self.is_mushroomed = False
        self.mushroom_timer = 0
        self.is_floating = False
        self.float_timer = 0

    def draw(self, surface, camera_x, camera_y):
        draw_x = self.world_x - camera_x
        draw_y = self.y - camera_y

        player_surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(player_surf, PLAYER_COLOR, (0, 0, self.size, self.size), border_radius=6)
        pygame.draw.rect(player_surf, OUTLINE_COLOR, (0, 0, self.size, self.size), 2, border_radius=6)

        if self.is_spiced:
            pulse = abs(pygame.time.get_ticks() % 500 - 250) / 250.0
            glow_color = (255, int(180 + 50 * pulse), 50)
            pygame.draw.rect(player_surf, glow_color, (0, 0, self.size, self.size), 3, border_radius=6)

        if self.is_mushroomed:
            pulse = abs(pygame.time.get_ticks() % 500 - 250) / 250.0
            glow_color = (220, 100 + int(50 * pulse), 255)
            pygame.draw.rect(player_surf, glow_color, (2, 2, self.size - 4, self.size - 4), 3, border_radius=6)

        if self.is_floating:
            pulse = abs(pygame.time.get_ticks() % 500 - 250) / 250.0
            glow_color = (200 + int(55 * pulse), 255, 255)
            pygame.draw.rect(player_surf, glow_color, (0, 0, self.size, self.size), 4, border_radius=10)

        rotated_surf = pygame.transform.rotate(player_surf, self.angle)
        rad = math.radians(self.angle)
        cos_val = max(0.1, math.cos(rad))
        y_offset = (self.size / 2.0) / cos_val - (self.size / 2.0)

        center_x = draw_x + self.size / 2.0
        center_y = draw_y + self.size / 2.0 - y_offset
        rot_rect = rotated_surf.get_rect(center=(center_x, center_y))
        surface.blit(rotated_surf, rot_rect.topleft)


class Block(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, block_type="solid", moving="none", speed=6, spike_type="normal"):
        super().__init__()
        self._init_data(grid_x, grid_y, block_type, moving, speed, spike_type)

    def _init_data(self, grid_x, grid_y, block_type, moving, speed, spike_type):
        self.world_x = grid_x * BLOCK_SIZE
        self.world_y = grid_y * BLOCK_SIZE
        self.rect = pygame.Rect(self.world_x, self.world_y, BLOCK_SIZE, BLOCK_SIZE)
        self.block_type = block_type
        self.moving = moving
        self.spike_type = spike_type
        self.start_x = self.world_x
        self.start_y = self.world_y

        move_speed = max(2, int(speed * 0.35))
        self.vx = move_speed if self.moving == "horizontal" else 0
        self.vy = move_speed if self.moving == "vertical" else 0
        self.left_h = BLOCK_SIZE
        self.right_h = BLOCK_SIZE

        self.crumble_frames = int(4.5 * FPS)
        self.is_crumbling = False
        self.is_broken = False
        self.is_visible = True
        self.activated = False
        self.cp_index = 0
        self.dodged = False

        if self.block_type == "phasing":
            self.phase_timer = 4 * FPS
            self.phase_hidden_frames = random.randint(1 * FPS, 2 * FPS)

        if self.block_type == "fade_platform":
            self.fade_timer = 3 * FPS
            self.is_faded = False

        if "mouth" in self.moving:
            self.mouth_state = "shutting"
            self.m_spd = 2.0 if "slow" in self.moving else 1.0
            self.mouth_timer = int(6 * FPS * self.m_spd)
            self.mouth_max_open = BLOCK_SIZE * 2.0

        if self.block_type == "pop_stone":
            self.pop_state = "waiting_down"
            self.pop_timer = 3 * FPS
            self.pop_offset = BLOCK_SIZE

        if self.block_type == "pop_spike":
            self.pop_state = "waiting_down"
            self.pop_timer = 3 * FPS
            self.pop_offset = 20

        if self.block_type == "ramp_up":
            self.right_h = 0
        elif self.block_type == "ramp_down":
            self.left_h = 0
        elif self.block_type == "gentle_up_1":
            self.right_h = BLOCK_SIZE // 2
        elif self.block_type == "gentle_up_2":
            self.left_h = BLOCK_SIZE // 2;
            self.right_h = 0
        elif self.block_type == "gentle_down_1":
            self.left_h = 0;
            self.right_h = BLOCK_SIZE // 2
        elif self.block_type == "gentle_down_2":
            self.left_h = BLOCK_SIZE // 2

        if self.block_type == "spike":
            if self.spike_type == "small":
                self.hitbox = pygame.Rect(self.rect.x + 16, self.rect.y + 32, 8, 8)
            elif self.spike_type == "tall":
                self.hitbox = pygame.Rect(self.rect.x + 18, self.rect.y + 16, 4, 24)
            else:
                self.hitbox = pygame.Rect(self.rect.x + 16, self.rect.y + 20, 8, 20)
        elif self.block_type == "pop_spike":
            self.hitbox = pygame.Rect(self.rect.x + 16, self.rect.y + 40, 8, 0)
        elif self.block_type == "slab":
            self.hitbox = pygame.Rect(self.rect.x, self.rect.y + BLOCK_SIZE // 2, BLOCK_SIZE, BLOCK_SIZE // 2)
        elif "mouth" in self.moving:
            if "mouth_top" in self.moving:
                self.hitbox = pygame.Rect(self.rect.x + 10, self.rect.y, BLOCK_SIZE - 20, BLOCK_SIZE - 16)
            elif "mouth_bottom" in self.moving:
                self.hitbox = pygame.Rect(self.rect.x + 10, self.rect.y + 16, BLOCK_SIZE - 20, BLOCK_SIZE - 16)
        elif self.block_type in ["spice", "mushroom", "float"]:
            self.hitbox = pygame.Rect(self.rect.x + 8, self.rect.y + 8, 24, 24)
        elif self.block_type == "pop_stone":
            self.hitbox = pygame.Rect(self.rect.x, self.rect.y + self.pop_offset, BLOCK_SIZE, 0)
        else:
            self.hitbox = self.rect

    def update(self):
        if self.moving == "vertical":
            self.world_y += self.vy
            if abs(self.world_y - self.start_y) > BLOCK_SIZE * 3.5: self.vy *= -1
            self.rect.y = self.world_y
            if self.block_type == "spike":
                if self.spike_type == "small":
                    self.hitbox.y = self.world_y + 32
                elif self.spike_type == "tall":
                    self.hitbox.y = self.world_y + 16
                else:
                    self.hitbox.y = self.world_y + 20
            elif self.block_type == "slab":
                self.hitbox.y = self.world_y + BLOCK_SIZE // 2
            else:
                self.hitbox.y = self.world_y

        elif self.moving == "horizontal":
            self.world_x += self.vx
            if abs(self.world_x - self.start_x) > BLOCK_SIZE * 2.5: self.vx *= -1
            self.rect.x = self.world_x
            if self.block_type == "spike":
                if self.spike_type == "small":
                    self.hitbox.x = self.world_x + 16
                elif self.spike_type == "tall":
                    self.hitbox.x = self.world_x + 18
                else:
                    self.hitbox.x = self.world_x + 16
            else:
                self.hitbox.x = self.world_x

        elif "mouth" in self.moving:
            if "drift" in self.moving:
                self.world_x -= 1.0
                self.rect.x = self.world_x

            if self.mouth_state == "shutting":
                self.mouth_timer -= 1
                progress = 1.0 - (self.mouth_timer / (6.0 * FPS * self.m_spd))
                if self.mouth_timer <= 0:
                    self.mouth_state = "opening"
                    self.mouth_timer = int(3 * FPS * self.m_spd)
            else:
                self.mouth_timer -= 1
                progress = self.mouth_timer / (3.0 * FPS * self.m_spd)
                if self.mouth_timer <= 0:
                    self.mouth_state = "shutting"
                    self.mouth_timer = int(6 * FPS * self.m_spd)

            offset = progress * self.mouth_max_open
            if "mouth_top" in self.moving:
                self.world_y = self.start_y + offset
                self.hitbox.y = self.world_y
                self.hitbox.x = self.world_x + 10
            elif "mouth_bottom" in self.moving:
                self.world_y = self.start_y - offset
                self.hitbox.y = self.world_y + 16
                self.hitbox.x = self.world_x + 10
            self.rect.y = self.world_y

        if self.block_type == "crumble" and self.is_crumbling and not self.is_broken:
            self.crumble_frames -= 1
            if self.crumble_frames <= 0:
                self.is_broken = True
                self.hitbox.y = -9999

        if self.block_type == "phasing":
            self.phase_timer -= 1
            if self.phase_timer <= 0:
                self.is_visible = not self.is_visible
                if self.is_visible:
                    self.phase_timer = 4 * FPS
                    self.hitbox.y = self.rect.y
                else:
                    self.phase_timer = self.phase_hidden_frames
                    self.hitbox.y = -9999

        if self.block_type == "fade_platform":
            self.fade_timer -= 1
            if self.fade_timer <= 0:
                self.is_faded = not self.is_faded
                self.fade_timer = 3 * FPS

        if self.block_type == "pop_stone":
            if self.pop_state == "waiting_down":
                self.pop_timer -= 1
                if self.pop_timer <= 0: self.pop_state = "popping_up"
            elif self.pop_state == "popping_up":
                self.pop_offset -= 4
                if self.pop_offset <= 0:
                    self.pop_offset = 0
                    self.pop_state = "waiting_up"
                    self.pop_timer = int(2.0 * FPS)
            elif self.pop_state == "waiting_up":
                self.pop_timer -= 1
                if self.pop_timer <= 0: self.pop_state = "going_down"
            elif self.pop_state == "going_down":
                self.pop_offset += 2
                if self.pop_offset >= BLOCK_SIZE:
                    self.pop_offset = BLOCK_SIZE
                    self.pop_state = "waiting_down"
                    self.pop_timer = 3 * FPS

            self.hitbox.y = self.world_y + self.pop_offset
            self.hitbox.height = max(0, BLOCK_SIZE - self.pop_offset)
            self.hitbox.x = self.world_x

        if self.block_type == "pop_spike":
            if self.pop_state == "waiting_down":
                self.pop_timer -= 1
                if self.pop_timer <= 0: self.pop_state = "popping_up"
            elif self.pop_state == "popping_up":
                self.pop_offset -= 1
                if self.pop_offset <= 0:
                    self.pop_offset = 0
                    self.pop_state = "waiting_up"
                    self.pop_timer = 1 * FPS
            elif self.pop_state == "waiting_up":
                self.pop_timer -= 1
                if self.pop_timer <= 0: self.pop_state = "going_down"
            elif self.pop_state == "going_down":
                self.pop_offset += 1
                if self.pop_offset >= 20:
                    self.pop_offset = 20
                    self.pop_state = "waiting_down"
                    self.pop_timer = 3 * FPS

            self.hitbox.y = self.world_y + 20 + self.pop_offset
            self.hitbox.height = max(0, 20 - self.pop_offset)
            self.hitbox.x = self.world_x + 16

    def draw(self, surface, camera_x, camera_y):
        draw_x = self.world_x - camera_x
        draw_y = self.world_y - camera_y

        if self.is_broken or not self.is_visible:
            if not self.is_visible and "phasing" in self.block_type:
                pygame.draw.rect(surface, (60, 60, 80) if getattr(score, "colour", True) else (40, 40, 50),
                                 (draw_x, draw_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=4)
            return

        if self.block_type == "fade_platform" and self.is_faded:
            faded_col = (35, 40, 55) if getattr(score, "colour", True) else (30, 30, 35)
            pygame.draw.rect(surface, faded_col, (draw_x, draw_y, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=4)
            return

        if self.block_type == "spice":
            surface.blit(SPICE_IMG, (draw_x + 8, draw_y + 8));
            return
        if self.block_type == "mushroom":
            surface.blit(MUSHROOM_IMG, (draw_x + 8, draw_y + 8));
            return
        if self.block_type == "float":
            surface.blit(FLOAT_IMG, (draw_x + 8, draw_y + 8));
            return

        if self.block_type == "crumble" and self.is_crumbling:
            draw_x += random.randint(-4, 4)
            draw_y += random.randint(-4, 4)

        float_rect = (draw_x, draw_y, BLOCK_SIZE, BLOCK_SIZE)
        outline = OUTLINE_COLOR
        if self.moving in ["horizontal", "vertical"]:
            outline = MOVING_OUTLINE
        elif self.block_type == "crumble":
            outline = CRUMBLE_COLOR
        elif self.block_type == "phasing":
            outline = PHASE_OUTLINE
        elif self.block_type == "checkpoint_base":
            outline = CHECKPOINT_OUTLINE

        fill_color = BLOCK_COLOR
        if self.block_type == "crumble" and self.is_crumbling and self.crumble_frames < 2 * FPS:
            if (self.crumble_frames // 4) % 2 == 0: fill_color = (255, 100, 100) if getattr(score, "colour",
                                                                                            True) else (255, 60, 60)

        if self.block_type == "phasing":
            pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0
            fill_color = (int(120 + 40 * pulse), 100, 180) if getattr(score, "colour", True) else (int(80 + 30 * pulse),
                                                                                                   80, 130)

        if self.block_type == "spike":
            if self.spike_type == "small":
                points = [(draw_x + 6, draw_y + BLOCK_SIZE), (draw_x + 34, draw_y + BLOCK_SIZE),
                          (draw_x + 20, draw_y + 15)]
            elif self.spike_type == "tall":
                points = [(draw_x + 6, draw_y + BLOCK_SIZE), (draw_x + 34, draw_y + BLOCK_SIZE),
                          (draw_x + 20, draw_y - 10)]
            else:
                points = [(draw_x + 2, draw_y + BLOCK_SIZE), (draw_x + 38, draw_y + BLOCK_SIZE),
                          (draw_x + 20, draw_y - 5)]
            pygame.draw.polygon(surface, SPIKE_COLOR, points)
            pygame.draw.polygon(surface, outline, points, 2)

        elif self.block_type == "pop_spike":
            if self.pop_offset < 20:
                tip_y = draw_y - 5 + (self.pop_offset * 2.25)
                points = [(draw_x + 2, draw_y + BLOCK_SIZE), (draw_x + 38, draw_y + BLOCK_SIZE), (draw_x + 20, tip_y)]
                pygame.draw.polygon(surface, SPIKE_COLOR, points)
                pygame.draw.polygon(surface, (255, 255, 50), points, 2)

        elif self.block_type == "slab":
            slab_rect = (draw_x, draw_y + BLOCK_SIZE // 2, BLOCK_SIZE, BLOCK_SIZE // 2)
            pygame.draw.rect(surface, SLAB_COLOR, slab_rect, border_radius=4)
            pygame.draw.rect(surface, outline, slab_rect, 2, border_radius=4)

        elif self.block_type == "pop_stone":
            if self.pop_offset < BLOCK_SIZE:
                stone_rect = (draw_x, draw_y + self.pop_offset, BLOCK_SIZE, BLOCK_SIZE - self.pop_offset)
                pygame.draw.rect(surface, (80, 230, 120) if getattr(score, "colour", True) else (50, 200, 80),
                                 stone_rect, border_radius=4)
                pygame.draw.rect(surface, OUTLINE_COLOR, stone_rect, 2, border_radius=4)

        elif "ramp" in self.block_type or "gentle" in self.block_type:
            bl_y = draw_y + self.left_h
            br_y = draw_y + self.right_h
            points = [(draw_x, draw_y + BLOCK_SIZE), (draw_x + BLOCK_SIZE, draw_y + BLOCK_SIZE),
                      (draw_x + BLOCK_SIZE, br_y), (draw_x, bl_y)]
            pygame.draw.polygon(surface, fill_color, points)
            pygame.draw.polygon(surface, outline, points, 2)

        elif "mouth" in self.moving:
            pygame.draw.rect(surface, (180, 70, 90) if getattr(score, "colour", True) else (140, 50, 60), float_rect,
                             border_radius=4)
            pygame.draw.rect(surface, (230, 80, 100) if getattr(score, "colour", True) else (200, 60, 70), float_rect,
                             2, border_radius=4)
            teeth_color = (255, 255, 240) if getattr(score, "colour", True) else (240, 240, 230)
            if "mouth_top" in self.moving:
                for i in range(4):
                    tx = draw_x + (i * 10)
                    pygame.draw.polygon(surface, teeth_color,
                                        [(tx, draw_y + BLOCK_SIZE), (tx + 10, draw_y + BLOCK_SIZE),
                                         (tx + 5, draw_y + BLOCK_SIZE + 12)])
            elif "mouth_bottom" in self.moving:
                for i in range(4):
                    tx = draw_x + (i * 10)
                    pygame.draw.polygon(surface, teeth_color, [(tx, draw_y), (tx + 10, draw_y), (tx + 5, draw_y - 12)])

        elif self.block_type == "ladder":
            pygame.draw.rect(surface, (150, 110, 60) if getattr(score, "colour", True) else (120, 90, 50), float_rect,
                             border_radius=4)
            for i in range(4):
                ry = draw_y + (i * 10) + 5
                pygame.draw.line(surface, (100, 70, 30) if getattr(score, "colour", True) else (80, 50, 20),
                                 (draw_x, ry), (draw_x + BLOCK_SIZE, ry), 3)
            pygame.draw.rect(surface, outline, float_rect, 2, border_radius=4)

        elif self.block_type == "flag":
            pygame.draw.rect(surface, (200, 200, 220) if getattr(score, "colour", True) else (180, 180, 190),
                             (draw_x + 16, draw_y, 6, BLOCK_SIZE))
            f_color = (80, 255, 80) if self.activated else (255, 80, 80)
            pygame.draw.polygon(surface, f_color, [(draw_x + 22, draw_y), (draw_x + 22, draw_y + 20),
                                                   (draw_x + BLOCK_SIZE + 10, draw_y + 10)])
            pygame.draw.polygon(surface, OUTLINE_COLOR, [(draw_x + 22, draw_y), (draw_x + 22, draw_y + 20),
                                                         (draw_x + BLOCK_SIZE + 10, draw_y + 10)], 2)

        elif self.block_type == "checkpoint_base" or self.block_type == "stairs":
            pygame.draw.rect(surface, (60, 80, 120) if self.block_type == "checkpoint_base" else fill_color, float_rect,
                             border_radius=4)
            pygame.draw.rect(surface, outline, float_rect, 2, border_radius=4)

        else:
            pygame.draw.rect(surface, fill_color, float_rect, border_radius=4)
            pygame.draw.rect(surface, outline, float_rect, 2, border_radius=4)
            if self.moving in ["horizontal", "vertical"]:
                pygame.draw.line(surface, outline, (draw_x, draw_y), (draw_x + BLOCK_SIZE, draw_y + BLOCK_SIZE), 2)


class BlockPool:
    def __init__(self):
        self._pool = []

    def get(self, grid_x, grid_y, block_type="solid", moving="none", speed=6, spike_type="normal"):
        if self._pool:
            b = self._pool.pop()
            b._init_data(grid_x, grid_y, block_type, moving, speed, spike_type)
            return b
        return Block(grid_x, grid_y, block_type, moving, speed, spike_type)

    def release(self, block):
        block.kill()
        self._pool.append(block)


# --- MAIN ENGINE APP ---
class GameApp:
    def __init__(self):
        pygame.display.set_caption("Boxel Pure 2D - Colorful Run")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_fullscreen = False

        self.font = pygame.font.SysFont("Courier New", 24, bold=True)
        self.title_font = pygame.font.SysFont("Courier New", 48, bold=True)
        self.caption_font = pygame.font.SysFont("Courier New", 18, bold=True)
        self.count_font = pygame.font.SysFont("Courier New", 14, bold=True)

        self.menu_hs_font = pygame.font.SysFont("Courier New", 14)
        self.menu_btn_font = pygame.font.SysFont("Courier New", 20, bold=True)

        self.state = "SPLASH"
        self.splash_timer = int(4.5 * FPS)

        self.active_diff = None

        self.player = Player()
        self.block_pool = BlockPool()

        self.blocks = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.phantom_meteors = pygame.sprite.Group()
        self.bg_sparkles = [ParallaxSparkle() for _ in range(30)]

        self.camera_x = 0
        self.camera_y = 0
        self.next_grid_x = 25
        self.current_y = 8
        self.freeze_frames = 0

        self.is_pausing_camera = False

        self.stop_energy = MAX_STOP_FRAMES
        self.cooldown_timer = 0

        self.last_gap_size = 0
        self.last_chunk_type = "flat"
        self.generated_cps = 0
        self.fast_forward_target = 0
        self.was_riding_moving = False

        self.caption_text = ""
        self.caption_timer = 0
        self.caption_color = (255, 255, 150)
        self.menu_scroll_y = 0

        self.death_message = ""

        self.inv_spice = 0
        self.inv_mushroom = 0
        self.inv_float = 0

        self.running = True

        self.achievements = {
            100: "Novice Runner - Passed 100m!",
            250: "Warming Up - Passed 250m!",
            500: "Getting the Hang of It - 500m!",
            1000: "Kilometer Crusher - 1000m!",
            2000: "Unstoppable Force - 2000m!",
            3500: "Are you a machine?! - 3500m!",
            5000: "Boxel Grandmaster - 5000m!"
        }
        self.achieved_milestones = set()

    def set_caption(self, text, duration=150, color=(255, 255, 150)):
        self.caption_text = text
        self.caption_timer = duration
        self.caption_color = color

    def spawn_particles(self, x, y, color, count, vy_range=(-4, 0)):
        for _ in range(count):
            self.particles.add(Particle(x, y, color, vy_range=vy_range))

    def get_block(self, grid_x, grid_y, **kwargs):
        speed = self.active_diff["speed"] if "speed" not in kwargs else kwargs["speed"]
        return self.block_pool.get(grid_x, grid_y, speed=speed, **kwargs)

    def start_run(self, diff):
        self.active_diff = diff
        random.seed(getattr(score, self.active_diff["seed_var"]))
        self.player.reset()

        for b in self.blocks: self.block_pool.release(b)
        self.blocks.empty()
        self.phantom_meteors.empty()
        self.particles.empty()

        self.caption_timer = 0
        self.was_riding_moving = False
        self.is_pausing_camera = False
        self.death_message = ""

        for j in range(25):
            self.blocks.add(self.get_block(j, 8))

        self.camera_x = 0
        self.camera_y = 0
        self.current_y = 8
        self.freeze_frames = 0
        self.stop_energy = MAX_STOP_FRAMES
        self.cooldown_timer = 0
        self.last_gap_size = 0
        self.last_chunk_type = "flat"
        self.next_grid_x = 25

        self.generated_cps = 0
        self.fast_forward_target = getattr(score, self.active_diff["cp_var"], 0)
        self.player.cp_index = self.fast_forward_target

        self.state = "PLAYING"

    def _build_flat_segment(self, start_x, start_y, length):
        for i in range(length):
            self.blocks.add(self.get_block(start_x + i, start_y))
            for j in range(start_y + 1, start_y + 15):
                self.blocks.add(self.get_block(start_x + i, j))
        return start_x + length

    def generate_level_chunks(self):
        while self.next_grid_x * BLOCK_SIZE < self.camera_x + WIDTH + (BLOCK_SIZE * 5) or self.fast_forward_target > 0:
            options = ["flat", "hill_up", "hill_down", "gentle_hill_up", "gentle_hill_down", "stairs_up",
                       "stairs_down", "moving_platform", "crumble_platform", "phasing_platform",
                       "mouth_gate", "ladder_climb", "stepping_stones", "phantom_mouth", "fade_platforms"]
            weights = list(self.active_diff["weights"])

            if self.next_grid_x // 80 > self.generated_cps:
                choice = "checkpoint_station"
            else:
                if self.last_gap_size == 3: weights[1] = 0; weights[3] = 0; weights[5] = 0
                if self.last_chunk_type in ["hill_up", "hill_down"]: weights[1] = 0; weights[2] = 0
                choice = random.choices(options, weights=weights)[0]

            self.last_chunk_type = choice

            if choice == "checkpoint_station":
                self.generated_cps += 1
                length = 8
                for i in range(length):
                    self.blocks.add(
                        self.get_block(self.next_grid_x + i, self.current_y, block_type="checkpoint_base"))
                    for j in range(self.current_y + 1, self.current_y + 15):
                        self.blocks.add(self.get_block(self.next_grid_x + i, j))

                flag_block = self.get_block(self.next_grid_x + 2, self.current_y - 1, block_type="flag")
                flag_block.cp_index = self.generated_cps
                self.blocks.add(flag_block)

                if self.generated_cps == self.fast_forward_target:
                    self.camera_x = (self.next_grid_x + 2) * BLOCK_SIZE - 150
                    self.camera_y = self.current_y * BLOCK_SIZE - HEIGHT // 2
                    self.player.world_x = (self.next_grid_x + 2) * BLOCK_SIZE
                    self.player.y = (self.current_y - 1) * BLOCK_SIZE + BLOCK_SIZE - self.player.size
                    self.player.rect.x = self.player.world_x
                    self.player.rect.y = self.player.y
                    self.player.last_safe_y = self.player.y
                    self.fast_forward_target = 0

                self.next_grid_x += length

            elif choice in ["flat", "crumble_platform", "phasing_platform"]:
                length = random.randint(8, 13) if choice == "flat" else random.randint(3, 5)
                for i in range(length):
                    if choice == "crumble_platform":
                        self.blocks.add(self.get_block(self.next_grid_x + i, self.current_y, block_type="crumble"))
                    elif choice == "phasing_platform":
                        self.blocks.add(self.get_block(self.next_grid_x + i, self.current_y, block_type="phasing"))
                    else:
                        self.blocks.add(self.get_block(self.next_grid_x + i, self.current_y))
                        for j in range(self.current_y + 1, self.current_y + 15):
                            self.blocks.add(self.get_block(self.next_grid_x + i, j))

                if choice == "flat" and length >= 8:
                    boosted_spike_chance = min(1.0, self.active_diff["spike_chance"] + 0.60)

                    if random.random() < boosted_spike_chance:
                        num_obs = random.randint(1, min(self.active_diff["max_spikes"] + 3, length - 6))
                        obs_positions = random.sample(range(2, length - 4), num_obs)

                        for pos in obs_positions:
                            rand_val = random.random()
                            if rand_val < 0.15:
                                self.blocks.add(
                                    self.get_block(self.next_grid_x + pos, self.current_y - 1, block_type="pop_stone"))
                            elif rand_val < 0.30:
                                self.blocks.add(
                                    self.get_block(self.next_grid_x + pos, self.current_y - 1, block_type="slab"))
                            elif rand_val < 0.55:
                                self.blocks.add(
                                    self.get_block(self.next_grid_x + pos, self.current_y - 1, block_type="pop_spike"))
                            else:
                                s_type = random.choice(["normal", "normal", "small", "tall"])
                                move_type = random.choice(["none", "none", "horizontal"])

                                self.blocks.add(
                                    self.get_block(self.next_grid_x + pos, self.current_y - 1, block_type="spike",
                                                   spike_type=s_type, moving=move_type))

                    if random.random() < 0.45:
                        item_pos = random.randint(2, length - 2)
                        i_type = random.choices(["spice", "mushroom", "float"], weights=[40, 40, 20])[0]
                        self.blocks.add(
                            self.get_block(self.next_grid_x + item_pos, self.current_y - 2, block_type=i_type))

                self.next_grid_x += length

            elif choice == "fade_platforms":
                num_steps = random.randint(3, 5)
                for step in range(num_steps):
                    step_len = random.randint(2, 4)
                    for i in range(step_len):
                        self.blocks.add(
                            self.get_block(self.next_grid_x + i, self.current_y, block_type="fade_platform"))
                    self.next_grid_x += step_len
                    if step < num_steps - 1:
                        self.next_grid_x += random.randint(2, 3)
                        self.current_y += random.randint(-1, 1)

            elif choice == "hill_up":
                self.next_grid_x = self._build_flat_segment(self.next_grid_x, self.current_y, random.randint(1, 3))
                length = random.randint(2, 4)
                for i in range(length):
                    self.current_y -= 1
                    self.blocks.add(self.get_block(self.next_grid_x + i, self.current_y, block_type="ramp_up"))
                    for j in range(self.current_y + 1, self.current_y + 15):
                        self.blocks.add(self.get_block(self.next_grid_x + i, j))
                self.next_grid_x += length
                self.next_grid_x = self._build_flat_segment(self.next_grid_x, self.current_y, random.randint(2, 4))

            elif choice == "hill_down":
                self.next_grid_x = self._build_flat_segment(self.next_grid_x, self.current_y, random.randint(1, 3))
                length = random.randint(2, 4)
                for i in range(length):
                    self.blocks.add(self.get_block(self.next_grid_x + i, self.current_y, block_type="ramp_down"))
                    for j in range(self.current_y + 1, self.current_y + 15):
                        self.blocks.add(self.get_block(self.next_grid_x + i, j))
                    self.current_y += 1
                self.next_grid_x += length
                self.next_grid_x = self._build_flat_segment(self.next_grid_x, self.current_y, random.randint(2, 4))

            elif choice == "gentle_hill_up":
                self.next_grid_x = self._build_flat_segment(self.next_grid_x, self.current_y, random.randint(1, 3))
                length = random.randint(1, 2) * 2
                for i in range(0, length, 2):
                    self.current_y -= 1
                    self.blocks.add(self.get_block(self.next_grid_x + i, self.current_y, block_type="gentle_up_1"))
                    for j in range(self.current_y + 1, self.current_y + 15): self.blocks.add(
                        self.get_block(self.next_grid_x + i, j))
                    self.blocks.add(
                        self.get_block(self.next_grid_x + i + 1, self.current_y, block_type="gentle_up_2"))
                    for j in range(self.current_y + 1, self.current_y + 15): self.blocks.add(
                        self.get_block(self.next_grid_x + i + 1, j))
                self.next_grid_x += length
                self.next_grid_x = self._build_flat_segment(self.next_grid_x, self.current_y, random.randint(2, 4))

            elif choice == "gentle_hill_down":
                self.next_grid_x = self._build_flat_segment(self.next_grid_x, self.current_y, random.randint(1, 3))
                length = random.randint(1, 2) * 2
                for i in range(0, length, 2):
                    self.blocks.add(self.get_block(self.next_grid_x + i, self.current_y, block_type="gentle_down_1"))
                    for j in range(self.current_y + 1, self.current_y + 15): self.blocks.add(
                        self.get_block(self.next_grid_x + i, j))
                    self.blocks.add(
                        self.get_block(self.next_grid_x + i + 1, self.current_y, block_type="gentle_down_2"))
                    for j in range(self.current_y + 1, self.current_y + 15): self.blocks.add(
                        self.get_block(self.next_grid_x + i + 1, j))
                    self.current_y += 1
                self.next_grid_x += length
                self.next_grid_x = self._build_flat_segment(self.next_grid_x, self.current_y, random.randint(2, 4))

            elif choice in ["stairs_up", "stairs_down"]:
                self.next_grid_x = self._build_flat_segment(self.next_grid_x, self.current_y, random.randint(1, 3))
                length = random.randint(3, 5)
                for i in range(length):
                    if choice == "stairs_up": self.current_y -= 1
                    self.blocks.add(self.get_block(self.next_grid_x + i, self.current_y, block_type="stairs"))
                    for j in range(self.current_y + 1, self.current_y + 15): self.blocks.add(
                        self.get_block(self.next_grid_x + i, j))
                    if choice == "stairs_down": self.current_y += 1
                self.next_grid_x += length
                self.next_grid_x = self._build_flat_segment(self.next_grid_x, self.current_y, random.randint(2, 4))

            elif choice == "stepping_stones":
                num_steps = random.randint(2, 4)
                for step in range(num_steps):
                    step_len = random.randint(1, 2)
                    self.next_grid_x = self._build_flat_segment(self.next_grid_x, self.current_y, step_len)
                    if random.random() < 0.40:
                        i_type = random.choices(["spice", "mushroom", "float"], weights=[40, 40, 20])[0]
                        self.blocks.add(self.get_block(self.next_grid_x - 1, self.current_y - 2, block_type=i_type))
                    if step < num_steps - 1: self.next_grid_x += random.randint(1, 2)

            elif choice == "moving_platform":
                move_dir = random.choice(["vertical", "horizontal"])
                plat_y = self.current_y + random.randint(0,
                                                         1) if self.last_gap_size == 3 else self.current_y + random.randint(
                    -1, 1)
                for i in range(3): self.blocks.add(self.get_block(self.next_grid_x + i, plat_y, moving=move_dir))
                self.next_grid_x += 3
                self.current_y = plat_y

            elif choice == "mouth_gate":
                gap_before = random.randint(2, 3)
                self.next_grid_x += gap_before
                top_y = self.current_y - 4
                bot_y = self.current_y
                mouth_len = 2 if self.active_diff["name"] in ["Impossible", "Professional"] else random.randint(4, 6)
                for i in range(mouth_len):
                    self.blocks.add(self.get_block(self.next_grid_x + i, top_y, moving="mouth_top"))
                    self.blocks.add(self.get_block(self.next_grid_x + i, bot_y, moving="mouth_bottom"))
                    for j in range(bot_y + 1, bot_y + 15): self.blocks.add(self.get_block(self.next_grid_x + i, j))
                self.next_grid_x += mouth_len

            elif choice == "phantom_mouth":
                gap_before = random.randint(3, 4)
                self.next_grid_x += gap_before
                top_y = self.current_y - 4
                bot_y = self.current_y
                for i in range(3):
                    self.blocks.add(self.get_block(self.next_grid_x + i, top_y, block_type="phasing",
                                                   moving="mouth_top_slow_drift"))
                    self.blocks.add(self.get_block(self.next_grid_x + i, bot_y, block_type="phasing",
                                                   moving="mouth_bottom_slow_drift"))
                    for j in range(bot_y + 1, bot_y + 15): self.blocks.add(self.get_block(self.next_grid_x + i, j))
                self.next_grid_x += 3

            elif choice == "ladder_climb":
                gap_before = random.randint(2, 4)
                self.next_grid_x += gap_before
                ladder_h = random.randint(5, 7)
                for i in range(ladder_h):
                    self.blocks.add(self.get_block(self.next_grid_x, self.current_y - i, block_type="ladder"))
                self.next_grid_x += 1
                self.current_y -= (ladder_h - 1)

            gap_min, gap_max = self.active_diff["gap_range"]
            gap_size = random.randint(gap_min, gap_max)
            self.next_grid_x += gap_size
            self.last_gap_size = gap_size

    def handle_input(self, keys):
        if (keys[pygame.K_w] or getattr(score, "auto_spice_activation",
                                        True)) and self.inv_spice > 0 and not self.player.is_spiced:
            self.inv_spice -= 1
            self.player.is_spiced = True
            self.player.spice_timer = 12 * FPS
            self.set_caption("Skill Activated: 12s High Speed & Jump!", color=(255, 180, 50))

        if (keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT] or getattr(score, "auto_mushroom_activation",
                                                                      True)) and self.inv_mushroom > 0 and not self.player.is_mushroomed:
            self.inv_mushroom -= 1
            self.player.is_mushroomed = True
            self.player.mushroom_timer = 12 * FPS
            self.set_caption("Skill Activated: 12s Invincible Shield!", color=(220, 100, 255))

        if (keys[pygame.K_e] or getattr(score, "auto_float_activation",
                                        True)) and self.inv_float > 0 and not self.player.is_floating:
            self.inv_float -= 1
            self.player.is_floating = True
            self.player.float_timer = 8 * FPS
            self.set_caption("Skill Activated: 8s Anti-Gravity Float!", color=(180, 250, 255))

        if keys[pygame.K_t] and self.player.is_floating:
            self.player.is_floating = False
            self.player.float_timer = 0
            self.set_caption("Floating ended early!", color=(180, 250, 255))

        self.is_pausing_camera = False
        if keys[pygame.K_LEFT] and self.cooldown_timer == 0 and self.stop_energy > 0:
            self.is_pausing_camera = True
            self.stop_energy -= 1
            if self.stop_energy <= 0: self.cooldown_timer = COOLDOWN_FRAMES
        else:
            if self.cooldown_timer > 0:
                self.cooldown_timer -= 1
                if self.cooldown_timer == 0: self.stop_energy = MAX_STOP_FRAMES
            elif self.stop_energy < MAX_STOP_FRAMES:
                self.stop_energy = min(MAX_STOP_FRAMES, self.stop_energy + 1)

    def update_physics(self, keys):
        if self.player.spice_timer > 0:
            self.player.spice_timer -= 1
            if self.player.spice_timer <= 0: self.player.is_spiced = False

        if self.player.mushroom_timer > 0:
            self.player.mushroom_timer -= 1
            if self.player.mushroom_timer <= 0: self.player.is_mushroomed = False

        if self.player.float_timer > 0:
            self.player.float_timer -= 1
            if self.player.float_timer <= 0: self.player.is_floating = False

        if self.active_diff["name"] in ["Very Easy", "Easy", "Medium"]:
            coyote_max = 12;
            inflate_px = 10;
            pity_px = 10;
            corner_leniency = 14;
            allow_ghost_saves = True
        elif self.active_diff["name"] in ["Hard", "Nightmare", "Impossible"]:
            coyote_max = 6;
            inflate_px = 4;
            pity_px = 5;
            corner_leniency = 8;
            allow_ghost_saves = True
        else:
            coyote_max = 1;
            inflate_px = 0;
            pity_px = 0;
            corner_leniency = 2;
            allow_ghost_saves = False

        speed_mod = 1.35 if self.player.is_spiced else 1.0
        if self.player.on_ground and self.player.standing_on and self.player.standing_on.block_type == "stairs":
            speed_mod *= 0.60

        current_speed = self.active_diff["speed"] * speed_mod
        current_jump_strength = JUMP_STRENGTH - 2.5 if self.player.is_spiced else JUMP_STRENGTH

        in_phantom = False
        for b in self.blocks:
            if "drift" in b.moving:
                if b.rect.left - (BLOCK_SIZE * 2) <= self.player.world_x <= b.rect.right + (BLOCK_SIZE * 2):
                    in_phantom = True
                    break

        if self.freeze_frames > 0:
            self.freeze_frames -= 1
        else:
            if not self.is_pausing_camera and self.fast_forward_target == 0:
                if self.player.on_ladder:
                    self.camera_y -= current_speed * 0.60
                    if self.player.rect.bottom < self.camera_y + 50: self.camera_y = self.player.rect.bottom - 50
                else:
                    self.camera_x += current_speed
                    target_camera_y = self.player.rect.centery - HEIGHT // 2
                    self.camera_y += (target_camera_y - self.camera_y) * 0.1

            if self.active_diff["name"] in ["Hard", "Nightmare", "Impossible",
                                            "Professional"] and self.fast_forward_target == 0:
                if random.random() < 0.01:
                    self.phantom_meteors.add(PhantomMeteor(
                        self.camera_x + WIDTH + random.randint(100, 600),
                        self.camera_y - random.randint(100, 300),
                        random.uniform(-18, -12), random.uniform(8, 15), random.randint(4, 8)
                    ))

            self.blocks.update()

            for b in self.blocks:
                if b.block_type == "crumble" and b.is_crumbling and not b.is_broken:
                    if b.crumble_frames == 1:
                        self.spawn_particles(b.world_x + BLOCK_SIZE / 2, b.world_y + BLOCK_SIZE / 2, CRUMBLE_COLOR, 3)

                if b.block_type in ["pop_stone", "pop_spike"] and getattr(b, "pop_state", "") == "waiting_down":
                    if random.random() < 0.05:
                        p_color = (80, 230, 120) if b.block_type == "pop_stone" else SPIKE_COLOR
                        self.spawn_particles(b.world_x + random.randint(5, BLOCK_SIZE - 5), b.world_y + 35, p_color, 1,
                                             vy_range=(-2.5, -0.5))

            self.generate_level_chunks()

            self.player.on_ladder = False
            active_ladder = None

            nearby_blocks = pygame.sprite.spritecollide(self.player, self.blocks, False)

            for b in nearby_blocks:
                if b.block_type in ["spike", "pop_spike"] or "mouth" in b.moving:
                    if not b.dodged and not self.player.rect.colliderect(b.hitbox):
                        self.set_caption("That was close! Smooth moves.", color=(100, 255, 100))
                        b.dodged = True

            for b in nearby_blocks:
                if b.is_broken: continue
                if b.block_type in ["spice", "mushroom", "float"] and self.player.rect.colliderect(b.hitbox):
                    b.is_broken = True
                    if b.block_type == "spice":
                        self.inv_spice += 1
                        self.set_caption("+1 Spice Collected!", color=(255, 180, 50))
                    elif b.block_type == "mushroom":
                        self.inv_mushroom += 1
                        self.set_caption("+1 Mushroom Shield Collected!", color=(220, 100, 255))
                    elif b.block_type == "float":
                        self.inv_float += 1
                        self.set_caption("+1 Float Orb Collected!", color=(180, 250, 255))

                if b.block_type == "flag" and self.player.rect.colliderect(b.hitbox) and not b.activated:
                    b.activated = True
                    if b.cp_index > self.player.cp_index:
                        self.player.cp_index = b.cp_index
                        setattr(score, self.active_diff["cp_var"], self.player.cp_index)
                        save_scores()

                    blocks_to_remove = [old_b for old_b in self.blocks if old_b.world_x < b.world_x - BLOCK_SIZE]
                    for old_b in blocks_to_remove:
                        self.block_pool.release(old_b)

                if b.block_type == "ladder" and self.player.rect.colliderect(b.hitbox):
                    self.player.on_ladder = True
                    active_ladder = b

            self.player.prev_right = self.player.rect.right
            self.player.prev_bottom = self.player.rect.bottom
            was_on_ground = self.player.on_ground

            if self.player.on_ground and self.player.standing_on:
                self.player.world_x += self.player.standing_on.vx
                self.player.y += self.player.standing_on.vy

            is_riding_moving = self.player.on_ground and self.player.standing_on and self.player.standing_on.moving != "none"
            if is_riding_moving and not self.was_riding_moving:
                self.set_caption("You have caught the express!", color=(255, 255, 100))
            self.was_riding_moving = is_riding_moving

            if self.player.on_ladder and active_ladder:
                self.player.world_x = active_ladder.world_x
            elif is_riding_moving:
                target_world_x = self.camera_x + 30
                if self.player.world_x < target_world_x: self.player.world_x += min(current_speed,
                                                                                    target_world_x - self.player.world_x)
            else:
                target_world_x = self.camera_x + (250 if self.player.is_spiced else 150)
                if self.player.world_x < target_world_x: self.player.world_x += min(current_speed,
                                                                                    target_world_x - self.player.world_x)

            self.player.rect.x = self.player.world_x

            for b in self.blocks:
                if b.block_type not in ["solid", "stairs", "crumble", "phasing", "checkpoint_base", "slab",
                                        "pop_stone",
                                        "fade_platform"] or b.rect.right < self.player.world_x or b.rect.x > self.player.world_x + BLOCK_SIZE: continue
                if self.player.rect.colliderect(b.hitbox):
                    if self.player.prev_right <= b.hitbox.x:
                        if self.player.rect.bottom > b.hitbox.top + corner_leniency:
                            self.player.rect.right = b.hitbox.x
                            self.player.world_x = self.player.rect.x
                        else:
                            self.player.y = b.hitbox.top - self.player.size
                            self.player.rect.y = self.player.y
                    if b.block_type == "crumble": b.is_crumbling = True

            if self.player.is_floating:
                if self.player.float_timer > 3 * FPS:
                    self.player.vy = -3.0  # Goes up for 5 seconds
                else:
                    self.player.vy = 3.0  # Goes down for final 3 seconds
            else:
                if self.player.on_ladder:
                    self.player.vy += 0.2
                    if self.player.vy > 3.0: self.player.vy = 3.0
                else:
                    if abs(self.player.vy) < 2.0 and not keys[pygame.K_DOWN]:
                        self.player.vy += GRAVITY * 0.4
                    else:
                        self.player.vy += GRAVITY

            self.player.y += self.player.vy
            self.player.rect.y = self.player.y
            self.player.on_ground = False
            self.player.standing_on = None

            for b in self.blocks:
                if b.block_type in ["spike", "pop_spike", "ladder", "flag", "spice", "mushroom",
                                    "float"] or b.rect.right < self.player.world_x or b.rect.x > self.player.world_x + self.player.size: continue
                if b.block_type in ["solid", "stairs", "crumble", "phasing", "checkpoint_base", "slab", "pop_stone",
                                    "fade_platform"]:
                    landing_box = b.hitbox.inflate(inflate_px * 2, 0)
                    if self.player.rect.colliderect(landing_box):
                        tolerance = max(2, abs(self.player.vy) + 2)
                        if self.player.vy >= 0 and self.player.prev_bottom <= landing_box.top + self.player.vy + tolerance:
                            if allow_ghost_saves and not self.player.rect.colliderect(b.hitbox):
                                if self.player.rect.centerx < b.hitbox.centerx:
                                    self.set_caption("Edge instinct save!", color=(100, 255, 150))
                                else:
                                    self.set_caption("Close jump at the last minute.", color=(100, 255, 150))
                            self.player.y = landing_box.top - self.player.size
                            self.player.rect.y = self.player.y
                            self.player.rect.bottom = landing_box.top
                            self.player.vy = 0
                            self.player.on_ground = True
                            if not self.player.is_floating:
                                self.player.last_safe_y = self.player.y
                            self.player.standing_on = b
                            if b.block_type == "crumble": b.is_crumbling = True
                        elif self.player.vy < 0 and self.player.rect.top < b.hitbox.bottom and self.player.prev_bottom > b.hitbox.bottom:
                            self.player.rect.top = b.hitbox.bottom
                            self.player.vy = 0
                            if b.block_type == "crumble": b.is_crumbling = True

                elif "ramp" in b.block_type or "gentle" in b.block_type:
                    if self.player.rect.right > b.rect.left - 8 and self.player.rect.left < b.rect.right + 8:
                        rel_x = self.player.rect.right - b.rect.left if b.left_h > b.right_h else self.player.rect.left - b.rect.left
                        rel_x = max(0, min(BLOCK_SIZE, rel_x))
                        t = rel_x / BLOCK_SIZE
                        surf_y = b.world_y + b.left_h + t * (b.right_h - b.left_h)
                        if self.player.vy >= 0 and self.player.rect.bottom >= surf_y - 10:
                            self.player.y = surf_y - self.player.size
                            self.player.rect.y = self.player.y
                            self.player.vy = 0
                            self.player.on_ground = True
                            if not self.player.is_floating:
                                self.player.last_safe_y = self.player.y

            if not was_on_ground and self.player.on_ground:
                valid_particle_blocks = ["solid", "crumble", "slab", "ramp_up", "ramp_down", "gentle_up_1",
                                         "gentle_up_2", "gentle_down_1", "gentle_down_2", "stairs", "checkpoint_base",
                                         "fade_platform"]
                if self.player.standing_on and self.player.standing_on.block_type in valid_particle_blocks:
                    if not keys[pygame.K_LEFT]:
                        b_type = self.player.standing_on.block_type
                        if b_type == "crumble":
                            base_color = CRUMBLE_COLOR
                        elif b_type == "checkpoint_base":
                            base_color = (60, 80, 120) if getattr(score, "colour", True) else (40, 50, 70)
                        else:
                            base_color = BLOCK_COLOR

                        for _ in range(3):
                            p_color = (
                                max(0, min(255, base_color[0] + random.randint(-20, 20))),
                                max(0, min(255, base_color[1] + random.randint(-20, 20))),
                                max(0, min(255, base_color[2] + random.randint(-20, 20)))
                            )
                            self.spawn_particles(self.player.world_x + self.player.size / 2,
                                                 self.player.y + self.player.size, p_color, 1, vy_range=(-1.5, 0))

            target_angle = 0.0
            if self.player.on_ground and self.player.standing_on:
                b = self.player.standing_on
                if "ramp" in b.block_type or "gentle" in b.block_type:
                    dy = b.right_h - b.left_h
                    target_angle = math.degrees(math.atan2(-dy, BLOCK_SIZE))
            self.player.angle += (target_angle - self.player.angle) * 0.4

            if self.player.on_ground:
                self.player.coyote_frames = coyote_max
            else:
                self.player.coyote_frames -= 1

            if self.player.jump_buffer > 0:
                if self.player.on_ground or self.player.coyote_frames > 0:
                    self.player.vy = current_jump_strength
                    self.player.on_ground = False
                    self.player.coyote_frames = 0
                    self.player.standing_on = None
                    self.freeze_frames = 2
                    self.player.jump_buffer = 0
                else:
                    self.player.jump_buffer -= 1

            # --- DEATH CHECK & LOGIC ---
            death_cause = None

            for b in nearby_blocks:
                if b.block_type in ["spike", "pop_spike"] and self.player.rect.colliderect(b.hitbox):
                    if self.player.is_mushroomed:
                        pass
                    elif pity_px > 0 and self.player.vy > 0 and self.player.rect.bottom - b.hitbox.top <= pity_px:
                        if random.random() < 0.33:
                            self.player.y -= (pity_px + 2)
                            self.player.vy = -4.5
                            self.player.rect.y = self.player.y
                            self.set_caption("Ohhh, that hurt! Be careful.", color=(255, 100, 100))
                        else:
                            death_cause = "spike"
                    else:
                        death_cause = "spike"

            if self.active_diff["name"] == "Professional" and self.fast_forward_target == 0:
                for m in self.phantom_meteors:
                    dist = math.hypot(m.x - (self.player.world_x + self.player.size / 2),
                                      m.y - (self.player.y + self.player.size / 2))
                    if dist < m.size + self.player.size / 2:
                        if not self.player.is_mushroomed:
                            death_cause = "meteor"
                            break

            if self.player.y > max(self.player.last_safe_y + 800, self.camera_y + HEIGHT + 200):
                death_cause = "void"
            elif self.player.on_ladder and self.player.rect.top > self.camera_y + HEIGHT:
                death_cause = "void"
            elif self.player.rect.right < self.camera_x and not self.is_pausing_camera:
                if in_phantom:
                    death_cause = "phantom_mouth"
                else:
                    death_cause = "screen_scrolling"

            if death_cause:
                self.state = "GAME_OVER"

                if death_cause == "spike":
                    self.death_message = "You are spiked!"
                elif death_cause == "meteor":
                    self.death_message = "You are ambushed from the sky"
                elif death_cause == "void":
                    self.death_message = "You fell into the void"
                elif death_cause == "phantom_mouth":
                    self.death_message = "You are crushed by a merciless mouth!"
                elif death_cause == "screen_scrolling":
                    self.death_message = "You are too behind progress!"
                else:
                    self.death_message = "You died!"

                current_score = int(self.camera_x // 10)
                hi_var_name = self.active_diff["var"]
                current_hi = getattr(score, hi_var_name)
                if current_score > current_hi:
                    setattr(score, hi_var_name, current_score)
                    save_scores()

    def update_playing_state(self):
        current_score = int(self.camera_x // 10)

        # Check Achievements (Now Persistent & Optional via Settings)
        if getattr(score, "achievement", True):
            for milestone, msg in self.achievements.items():
                if current_score >= milestone and milestone not in self.achieved_milestones:
                    self.set_caption(f"ACHIEVEMENT: {msg}", duration=240, color=(255, 220, 50))
                    self.spawn_particles(self.player.world_x + self.player.size / 2, self.player.y, (255, 215, 0), 20,
                                         vy_range=(-6, -2))
                    self.achieved_milestones.add(milestone)

        if current_score >= WIN_SCORE:
            self.state = "VICTORY"
            setattr(score, self.active_diff["comp_var"], True)
            hi_var_name = self.active_diff["var"]
            if current_score > getattr(score, hi_var_name):
                setattr(score, hi_var_name, current_score)
            save_scores()

        keys = pygame.key.get_pressed()
        self.handle_input(keys)
        self.update_physics(keys)

        self.phantom_meteors.update()
        for m in self.phantom_meteors:
            if m.y - self.camera_y > HEIGHT or m.x - self.camera_x < -100: m.kill()

        self.particles.update()

    def draw_splash(self):
        self.screen.fill((15, 15, 20))
        splash_text1 = self.caption_font.render("A wonderful parkour game made by an independent game developer.", True,
                                                (255, 255, 0))
        splash_text2 = self.caption_font.render("Please help me improve the code.", True, (255, 255, 0))

        self.screen.blit(splash_text1, (WIDTH // 2 - splash_text1.get_width() // 2, HEIGHT // 2 - 20))
        self.screen.blit(splash_text2, (WIDTH // 2 - splash_text2.get_width() // 2, HEIGHT // 2 + 10))

        self.splash_timer -= 1
        if self.splash_timer <= 0:
            self.state = "MENU"

    def draw_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        if getattr(score, "colour", True):
            for sparkle in self.bg_sparkles:
                sparkle.draw(self.screen, self.camera_x, self.camera_y)

        title = self.title_font.render("BOXEL 2D", True, PLAYER_COLOR)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
        sub = self.font.render("Scroll down for settings and more levels.", True, (255, 255, 255))
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 90))

        btn_w, btn_h = 200, 60
        spacing_x, spacing_y = 40, 20
        start_x = WIDTH // 2 - btn_w - (spacing_x // 2)
        start_y = 150

        for i, diff in enumerate(DIFFICULTIES):
            if diff["name"] == "Professional":
                bx = WIDTH // 2 - btn_w // 2
                by = start_y + 4.5 * (btn_h + spacing_y) + self.menu_scroll_y
            else:
                bx = start_x + (i % 2) * (btn_w + spacing_x)
                by = start_y + (i // 2) * (btn_h + spacing_y) + self.menu_scroll_y

            btn_rect = pygame.Rect(bx, by, btn_w, btn_h)
            color = diff["color"] if not btn_rect.collidepoint(mouse_pos) else (255, 255, 255)

            pygame.draw.rect(self.screen, (20, 25, 35), btn_rect, border_radius=8)
            pygame.draw.rect(self.screen, color, btn_rect, 3, border_radius=8)
            text = self.font.render(diff["name"], True, color)
            self.screen.blit(text, (bx + btn_w // 2 - text.get_width() // 2, by + btn_h // 2 - text.get_height() // 2))

            hs_val = getattr(score, diff["var"])
            hs_text = self.menu_hs_font.render(f"Best: {hs_val:08d}", True, (200, 200, 220))
            self.screen.blit(hs_text, (bx + btn_w // 2 - hs_text.get_width() // 2, by + btn_h - 18))

            rr_rect = pygame.Rect(bx + btn_w + 10, by + 10, 40, 40)
            rr_color = diff["color"] if not rr_rect.collidepoint(mouse_pos) else (255, 255, 255)
            pygame.draw.rect(self.screen, (20, 25, 35), rr_rect, border_radius=8)
            pygame.draw.rect(self.screen, rr_color, rr_rect, 2, border_radius=8)
            rr_text = self.menu_btn_font.render("R", True, rr_color)
            self.screen.blit(rr_text,
                             (rr_rect.centerx - rr_text.get_width() // 2, rr_rect.centery - rr_text.get_height() // 2))

            if mouse_clicked and getattr(self, "click_handled", False) == False:
                if rr_rect.collidepoint(mouse_pos):
                    current_cp = getattr(score, diff["cp_var"], 0)
                    new_cp = max(0, current_cp - 1)
                    new_seed = diff["name"] + str(random.randint(1000, 99999))
                    setattr(score, diff["seed_var"], new_seed)
                    setattr(score, diff["cp_var"], new_cp)
                    save_scores()

                    self.inv_spice = 0;
                    self.inv_mushroom = 0;
                    self.inv_float = 0
                    self.start_run(diff)
                    self.click_handled = True
                elif btn_rect.collidepoint(mouse_pos):
                    self.inv_spice = 0;
                    self.inv_mushroom = 0;
                    self.inv_float = 0
                    self.start_run(diff)
                    self.click_handled = True

        toggle_y = start_y + 4.5 * (btn_h + spacing_y) + btn_h + 30 + self.menu_scroll_y
        toggles = [
            ("Auto-Spice Activation", "auto_spice_activation", (255, 150, 0)),
            ("Auto-Mushroom Activation", "auto_mushroom_activation", (200, 50, 255)),
            ("Auto-Float Activation", "auto_float_activation", (150, 240, 255)),
            ("Achievements", "achievement", (255, 215, 0)),
            ("Colour Mode", "colour", (120, 255, 120))
        ]

        for label, var_name, color in toggles:
            val = getattr(score, var_name, True)
            lbl = self.font.render(label, True, (255, 255, 255))
            self.screen.blit(lbl, (WIDTH // 2 - 180, toggle_y))

            sw_rect = pygame.Rect(WIDTH // 2 + 130, toggle_y, 50, 24)
            pygame.draw.rect(self.screen, color if val else (100, 100, 100), sw_rect, border_radius=12)
            pygame.draw.circle(self.screen, (255, 255, 255),
                               (sw_rect.right - 12 if val else sw_rect.left + 12, sw_rect.centery), 10)

            click_area = pygame.Rect(WIDTH // 2 - 180, toggle_y, 360, 24)
            if mouse_clicked and not getattr(self, "click_handled", False) and click_area.collidepoint(mouse_pos):
                setattr(score, var_name, not val)
                save_scores()

                # Immediately apply palette update if Colour Mode was clicked
                if var_name == "colour":
                    update_palette()

                self.click_handled = True

            toggle_y += 40

    def draw_playing(self):
        if getattr(score, "colour", True):
            for sparkle in self.bg_sparkles:
                sparkle.draw(self.screen, self.camera_x, self.camera_y)

        for m in self.phantom_meteors:
            m_draw_x, m_draw_y = m.x - self.camera_x, m.y - self.camera_y
            m_color = (255, 50, 50) if self.active_diff["name"] == "Professional" else (255, 100, 50)
            pygame.draw.circle(self.screen, m_color, (int(m_draw_x), int(m_draw_y)), m.size)
            pygame.draw.line(self.screen, (255, 200, 50), (m_draw_x, m_draw_y),
                             (m_draw_x - m.vx * 3, m_draw_y - m.vy * 3), m.size)

        visible_blocks = [b for b in self.blocks if b.rect.right > self.camera_x and b.rect.x < self.camera_x + WIDTH
                          and b.rect.bottom > self.camera_y and b.rect.top < self.camera_y + HEIGHT]
        for b in visible_blocks: b.draw(self.screen, self.camera_x, self.camera_y)

        for p in self.particles: p.draw(self.screen, self.camera_x, self.camera_y)
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        pygame.draw.rect(self.screen, BG_COLOR, (10, 10, 220, 65), border_radius=5)
        pygame.draw.rect(self.screen, self.active_diff["color"], (10, 10, 220, 65), 2, border_radius=5)
        score_text = self.font.render(f"CUR: {int(self.camera_x // 10):08d}", True, (255, 255, 255))
        hi_text = self.font.render(f"MAX: {getattr(score, self.active_diff['var']):08d}", True,
                                   self.active_diff["color"])
        self.screen.blit(score_text, (20, 15));
        self.screen.blit(hi_text, (20, 42))

        if getattr(score, self.active_diff["comp_var"]):
            comp_text = self.caption_font.render("Level Already Conquered!", True, (255, 215, 0))
            self.screen.blit(comp_text, (WIDTH // 2 - comp_text.get_width() // 2, 15))

        pygame.draw.rect(self.screen, BG_COLOR, (10, 85, 220, 16), border_radius=4)
        pygame.draw.rect(self.screen, OUTLINE_COLOR, (10, 85, 220, 16), 2, border_radius=4)
        if self.cooldown_timer > 0:
            fill_w = max(0, int((self.cooldown_timer / COOLDOWN_FRAMES) * 216))
            pygame.draw.rect(self.screen, SPIKE_COLOR, (12, 87, fill_w, 12), border_radius=3)
        else:
            fill_w = max(0, int((self.stop_energy / MAX_STOP_FRAMES) * 216))
            pygame.draw.rect(self.screen, STAMINA_COLOR, (12, 87, fill_w, 12), border_radius=3)

        inv_w = 130
        inv_x = WIDTH - inv_w - 10
        inv_y = 10
        pygame.draw.rect(self.screen, (30, 30, 35, 180), (inv_x, inv_y, inv_w, 40), border_radius=5)
        pygame.draw.rect(self.screen, OUTLINE_COLOR, (inv_x, inv_y, inv_w, 40), 2, border_radius=5)

        def draw_inv_slot(img, count, x_offset):
            self.screen.blit(img, (inv_x + x_offset, inv_y + 8))
            if count > 0:
                cnt_txt = self.count_font.render(str(count), True, (255, 255, 255))
                shd_txt = self.count_font.render(str(count), True, (0, 0, 0))
                cx = inv_x + x_offset + 24 - cnt_txt.get_width()
                cy = inv_y + 8 + 24 - cnt_txt.get_height()
                self.screen.blit(shd_txt, (cx + 1, cy + 1))
                self.screen.blit(cnt_txt, (cx, cy))

        draw_inv_slot(SPICE_IMG, self.inv_spice, 10)
        draw_inv_slot(MUSHROOM_IMG, self.inv_mushroom, 50)
        draw_inv_slot(FLOAT_IMG, self.inv_float, 90)

        cd_y = 55
        if self.player.spice_timer > 0 and self.player.spice_timer <= 3 * FPS:
            cd_text = self.font.render(f"Spice: {math.ceil(self.player.spice_timer / FPS)}s", True, (255, 180, 50))
            self.screen.blit(cd_text, (WIDTH - cd_text.get_width() - 10, cd_y))
            cd_y += 25
        if self.player.mushroom_timer > 0 and self.player.mushroom_timer <= 3 * FPS:
            cd_text = self.font.render(f"Shroom: {math.ceil(self.player.mushroom_timer / FPS)}s", True, (220, 100, 255))
            self.screen.blit(cd_text, (WIDTH - cd_text.get_width() - 10, cd_y))
            cd_y += 25
        if self.player.float_timer > 0 and self.player.float_timer <= 3 * FPS:
            cd_text = self.font.render(f"Float: {math.ceil(self.player.float_timer / FPS)}s", True, (180, 250, 255))
            self.screen.blit(cd_text, (WIDTH - cd_text.get_width() - 10, cd_y))
            cd_y += 25

        if self.caption_timer > 0:
            self.caption_timer -= 1
            alpha = min(255, self.caption_timer * 5)
            cap_surf = self.caption_font.render(self.caption_text, True, self.caption_color)
            cap_surf.set_alpha(alpha)
            cap_bg = pygame.Surface((cap_surf.get_width() + 20, cap_surf.get_height() + 10), pygame.SRCALPHA)
            pygame.draw.rect(cap_bg, (0, 0, 0, min(150, alpha)), (0, 0, cap_bg.get_width(), cap_bg.get_height()),
                             border_radius=8)
            self.screen.blit(cap_bg, (WIDTH // 2 - cap_bg.get_width() // 2, HEIGHT - 60))
            self.screen.blit(cap_surf, (WIDTH // 2 - cap_surf.get_width() // 2, HEIGHT - 55))

        if self.state == "GAME_OVER":
            overlay = pygame.Surface((WIDTH, HEIGHT));
            overlay.set_alpha(180);
            overlay.fill((40, 0, 10))
            self.screen.blit(overlay, (0, 0))
            go_text = self.title_font.render("SHATTERED!", True, SPIKE_COLOR)
            self.screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 60))

            # Draw specific death message
            death_txt = self.font.render(getattr(self, "death_message", "You died!"), True, (255, 180, 180))
            self.screen.blit(death_txt, (WIDTH // 2 - death_txt.get_width() // 2, HEIGHT // 2 - 10))

            sub_text = self.font.render(
                "SPACE = Checkpoint | ESC = Menu" if self.player.cp_index > 0 else "SPACE = Retry | ESC = Menu", True,
                (100, 255, 100) if self.player.cp_index > 0 else (255, 255, 255))
            self.screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 30))

        elif self.state == "VICTORY":
            overlay = pygame.Surface((WIDTH, HEIGHT));
            overlay.set_alpha(200);
            overlay.fill((255, 200, 50))
            self.screen.blit(overlay, (0, 0))
            go_text = self.title_font.render("YOU HAVE BEATEN THIS LEVEL!", True, (255, 255, 255))
            self.screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 40))
            sub_text = self.font.render("SPACE = Retry | ESC = Menu", True, (0, 0, 0))
            self.screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 20))

    def run(self):
        while self.running:
            # Determine if we draw grid lines or just the solid dark background for the splash
            if self.state != "SPLASH":
                self.screen.fill(BG_COLOR)
                offset_x = -(self.camera_x % BLOCK_SIZE) if self.state != "MENU" else 0
                offset_y = -(self.camera_y % BLOCK_SIZE) if self.state != "MENU" else 0

                for x in range(0, int(WIDTH + BLOCK_SIZE), BLOCK_SIZE): pygame.draw.line(self.screen, GRID_COLOR,
                                                                                         (x + offset_x, 0),
                                                                                         (x + offset_x, HEIGHT))
                for y in range(0, int(HEIGHT + BLOCK_SIZE), BLOCK_SIZE): pygame.draw.line(self.screen, GRID_COLOR,
                                                                                          (0, y + offset_y),
                                                                                          (WIDTH, y + offset_y))

            self.click_handled = False if not pygame.mouse.get_pressed()[0] else getattr(self, "click_handled", False)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()
                if event.type == pygame.MOUSEWHEEL and self.state == "MENU":
                    # Increased scroll limit so all settings are visible
                    self.menu_scroll_y = min(0, max(-450, self.menu_scroll_y + event.y * 30))
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_F11, pygame.K_f]:
                        self.is_fullscreen = not self.is_fullscreen
                        self.screen = pygame.display.set_mode((WIDTH, HEIGHT),
                                                              pygame.FULLSCREEN if self.is_fullscreen else 0)

                    if self.state in ["GAME_OVER", "VICTORY"]:
                        if event.key in [pygame.K_SPACE, pygame.K_UP]:
                            self.start_run(self.active_diff)
                        elif event.key == pygame.K_ESCAPE:
                            random.seed()
                            self.state = "MENU"
                            self.inv_spice = 0;
                            self.inv_mushroom = 0;
                            self.inv_float = 0

                    elif self.state == "PLAYING":
                        if event.key in [pygame.K_SPACE, pygame.K_UP]:
                            if self.player.on_ladder:
                                self.player.vy = -6.0
                            else:
                                self.player.jump_buffer = 10

            if self.state == "SPLASH":
                self.draw_splash()
            elif self.state == "MENU":
                self.draw_menu()
            else:
                if self.state == "PLAYING": self.update_playing_state()
                self.draw_playing()

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    app = GameApp()
    app.run()