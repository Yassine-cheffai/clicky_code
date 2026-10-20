import math
import random
import arcade

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Industrial Futurist Space Shooter"

SHIP_SPEED = 5.0
MAX_TILT_ANGLE = 30.0  # Max roll angle when turning
TILT_SMOOTHING = 0.15  # Speed of roll interpolation


class StarStreak:
  """Represents a scrolling background star line to create forward motion illusion."""

  def __init__(self):
    self.reset(random_y=True)

  def reset(self, random_y=False):
    self.x = random.randint(0, SCREEN_WIDTH)
    self.y = (
        random.randint(0, SCREEN_HEIGHT) if random_y else SCREEN_HEIGHT + 10
    )
    self.length = random.randint(15, 35)
    self.speed = random.uniform(8.0, 16.0)
    self.brightness = random.randint(150, 255)

  def update(self):
    self.y -= self.speed
    if self.y < -self.length:
      self.reset()

  def draw(self):
    arcade.draw_line(
        self.x,
        self.y,
        self.x,
        self.y - self.length,
        (self.brightness, self.brightness, 255, self.brightness),
        1.5,
    )


class Particle:
  """Engine plasma and lightning spark particle effect."""

  def __init__(self, x, y, dx, dy, color, size, lifetime):
    self.x = x
    self.y = y
    self.dx = dx
    self.dy = dy
    self.color = color
    self.size = size
    self.lifetime = lifetime
    self.age = 0

  def update(self):
    self.x += self.dx
    self.y += self.dy
    self.age += 1

  def is_dead(self):
    return self.age >= self.lifetime

  def draw(self):
    alpha = int(255 * (1 - (self.age / self.lifetime)))
    r, g, b = self.color[:3]
    arcade.draw_circle_filled(self.x, self.y, self.size, (r, g, b, alpha))

class SpaceShip(arcade.Sprite):
  """Procedurally rendered spaceship sprite supporting roll tilt & dynamic flame effects."""

  def __init__(self, x, y):
    super().__init__()
    self.center_x = x
    self.center_y = y

    self.target_angle = 0.0
    self.current_angle = 0.0

    # Controls tracking
    self.move_left = False
    self.move_right = False
    self.move_up = False
    self.move_down = False

    self.particles = []

  def update_movement(self):
    dx = 0
    dy = 0

    if self.move_left:
      dx -= SHIP_SPEED
    if self.move_right:
      dx += SHIP_SPEED
    if self.move_up:
      dy += SHIP_SPEED
    if self.move_down:
      dy -= SHIP_SPEED

    self.center_x = max(40, min(SCREEN_WIDTH - 40, self.center_x + dx))
    self.center_y = max(40, min(SCREEN_HEIGHT - 40, self.center_y + dy))

    # Calculate smooth 30-degree roll angle based on horizontal direction
    if dx < 0:
      self.target_angle = MAX_TILT_ANGLE  # Roll left
    elif dx > 0:
      self.target_angle = -MAX_TILT_ANGLE  # Roll right
    else:
      self.target_angle = 0.0  # Level out

    # Interpolate current angle toward target angle smoothly
    self.current_angle += (
        self.target_angle - self.current_angle
    ) * TILT_SMOOTHING
    self.angle = self.current_angle

  def generate_thruster_particles(self):
    # Calculate engine exit coordinates relative to rotation angle
    rad = math.radians(self.angle)
    back_x = self.center_x - math.sin(rad) * 25
    back_y = self.center_y - math.cos(rad) * 25

    # Orange/Yellow engine thrust flames
    for _ in range(3):
      px = back_x + random.uniform(-10, 10)
      py = back_y + random.uniform(-5, 0)
      dx = -math.sin(rad) * random.uniform(2, 5) + random.uniform(-0.5, 0.5)
      dy = -math.cos(rad) * random.uniform(6, 12) + random.uniform(-0.5, 0.5)
      color = random.choice([
          (255, 120, 20),
          (255, 200, 40),
          (255, 80, 10),
      ])
      self.particles.append(
          Particle(
              px, py, dx, dy, color, random.uniform(2, 4), random.randint(10, 20)
          )
      )

    # Cyan/Purple central electric ion beam sparks
    for _ in range(2):
      px = back_x + random.uniform(-3, 3)
      py = back_y
      dx = random.uniform(-1, 1)
      dy = -random.uniform(10, 18)
      color = random.choice([(80, 220, 255), (180, 100, 255)])
      self.particles.append(
          Particle(
              px, py, dx, dy, color, random.uniform(1, 3), random.randint(8, 15)
          )
      )

  def update(self):
    self.update_movement()
    self.generate_thruster_particles()

    # Update particle physics
    for p in self.particles[:]:
      p.update()
      if p.is_dead():
        self.particles.remove(p)

  def draw(self):
    # Render particles in world space underneath the ship
    for p in self.particles:
      p.draw()

    # Anchor point rendering fix (using direct arcade function)
    arcade.draw_point(self.center_x, self.center_y, arcade.color.WHITE, 1)

    # Custom vector design render with angle rotation matrix
    rad = math.radians(self.angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    def to_screen(lx, ly):
      rx = lx * cos_a - ly * sin_a
      ry = lx * sin_a + ly * cos_a
      return (self.center_x + rx, self.center_y + ry)

    # Draw Wing Outlines / Hull Elements rotated dynamically
    wings = [
        to_screen(-35, -20),
        to_screen(-12, 10),
        to_screen(0, 28),
        to_screen(12, 10),
        to_screen(35, -20),
    ]
    arcade.draw_polygon_filled(wings, (45, 85, 115))

    body = [
        to_screen(-12, -25),
        to_screen(-12, 10),
        to_screen(0, 35),
        to_screen(12, 10),
        to_screen(12, -25),
    ]
    arcade.draw_polygon_filled(body, (30, 55, 80))

    cockpit = [
        to_screen(-6, 0),
        to_screen(-6, 18),
        to_screen(0, 25),
        to_screen(6, 18),
        to_screen(6, 0),
    ]
    arcade.draw_polygon_filled(cockpit, (185, 125, 60))

    # Cannons
    arcade.draw_line(*to_screen(-18, 5), *to_screen(-18, 30), (30, 35, 45), 3)
    arcade.draw_line(*to_screen(18, 5), *to_screen(18, 30), (30, 35, 45), 3)

class Laser(arcade.Sprite):
  """Player projectile."""

  def __init__(self, x, y):
    super().__init__()
    self.center_x = x
    self.center_y = y
    self.speed = 18.0

  def update(self):
    self.center_y += self.speed

  def draw(self):
    arcade.draw_line(
        self.center_x,
        self.center_y - 10,
        self.center_x,
        self.center_y + 10,
        (100, 230, 255),
        3,
    )
    arcade.draw_circle_filled(
        self.center_x, self.center_y + 10, 3, (200, 245, 255)
    )


class GameWindow(arcade.Window):
  """Main Arcade Game Window."""

  def __init__(self):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color((8, 12, 22))

    self.stars = [StarStreak() for _ in range(60)]
    self.player = SpaceShip(SCREEN_WIDTH // 2, 100)
    self.lasers = []
    self.score = 0

  def on_draw(self):
    self.clear()

    # Draw scrolling starfield
    for star in self.stars:
      star.draw()

    # Draw player ship and engine thrusters
    self.player.draw()

    # Draw active projectiles
    for laser in self.lasers:
      laser.draw()

    # Display HUD UI
    arcade.draw_text(
        f"SCORE: {self.score:05d}",
        20,
        SCREEN_HEIGHT - 35,
        (120, 220, 255),
        14,
        font_name="DejaVu Sans",
        bold=True,
    )
    arcade.draw_text(
        "CONTROLS: WASD / ARROWS to Move | SPACE to Shoot",
        20,
        20,
        (100, 130, 160),
        10,
    )

  def on_update(self, delta_time: float):
    # Update stars
    for star in self.stars:
      star.update()

    # Update player position & animations
    self.player.update()

    # Update lasers
    for laser in self.lasers[:]:
      laser.update()
      if laser.center_y > SCREEN_HEIGHT + 20:
        self.lasers.remove(laser)

  def on_key_press(self, symbol: int, modifiers: int):
    if symbol in (arcade.key.A, arcade.key.LEFT):
      self.player.move_left = True
    elif symbol in (arcade.key.D, arcade.key.RIGHT):
      self.player.move_right = True
    elif symbol in (arcade.key.W, arcade.key.UP):
      self.player.move_up = True
    elif symbol in (arcade.key.S, arcade.key.DOWN):
      self.player.move_down = True
    elif symbol == arcade.key.SPACE:
      # Fire twin cannons
      rad = math.radians(self.player.angle)
      cos_a = math.cos(rad)
      sin_a = math.sin(rad)

      offset_x = 18
      lx1 = self.player.center_x - offset_x * cos_a
      ly1 = self.player.center_y - offset_x * sin_a
      lx2 = self.player.center_x + offset_x * cos_a
      ly2 = self.player.center_y + offset_x * sin_a

      self.lasers.append(Laser(lx1, ly1 + 20))
      self.lasers.append(Laser(lx2, ly2 + 20))
      self.score += 10

  def on_key_release(self, symbol: int, modifiers: int):
    if symbol in (arcade.key.A, arcade.key.LEFT):
      self.player.move_left = False
    elif symbol in (arcade.key.D, arcade.key.RIGHT):
      self.player.move_right = False
    elif symbol in (arcade.key.W, arcade.key.UP):
      self.player.move_up = False
    elif symbol in (arcade.key.S, arcade.key.DOWN):
      self.player.move_down = False


if __name__ == "__main__":
  app = GameWindow()
  arcade.run()