from ursina import *
import math
import random
from PIL import Image, ImageFilter

app = Ursina()

# --- 1. Environment & Lighting ---
Sky(color=color.black)

# Dynamic PointLight inside the Sun to cast light onto orbiting bodies
sun_light = PointLight(position=(0, 0, 0), color=color.white)
AmbientLight(color=color.rgba(25, 25, 25, 0.4))

# --- 2. Procedural Solar Surface Texture Generator ---
def create_solar_texture(size=512):
    """Generates a turbulent plasma surface texture in memory (no external image files needed)."""
    img = Image.new('RGB', (size, size), color=(255, 140, 0))
    pixels = img.load()
    
    # Layer noise for granulation/flares
    for x in range(size):
        for y in range(size):
            noise = random.randint(-45, 45)
            r = min(255, max(210, 245 + noise))
            g = min(255, max(90, 160 + noise))
            b = min(255, max(0, 20 + noise // 2))
            pixels[x, y] = (r, g, b)
            
    # Gaussian blur converts raw noise into smooth plasma cells
    img = img.filter(ImageFilter.GaussianBlur(radius=6))
    return Texture(img)

# --- 3. Sun Architecture (Core + Atmosphere + Halo) ---

# A. Central Core with procedural plasma texture
sun_core = Entity(
    model='sphere',
    texture=create_solar_texture(),
    scale=2.5,
    position=(0, 0, 0),
    unlit=True
)

# B. Inner Corona Atmosphere (semi-transparent warm aura)
inner_glow = Entity(
    model='sphere',
    color=color.rgba(255, 180, 0, 0.35),
    scale=2.8,
    unlit=True,
    double_sided=True
)

# C. Outer Corona Haze (faded ambient boundary)
outer_glow = Entity(
    model='sphere',
    color=color.rgba(255, 80, 0, 0.15),
    scale=3.3,
    unlit=True,
    double_sided=True
)

# D. Soft Camera-Facing Halo (Radial Gradient Flare)
corona_halo = Entity(
    model='quad',
    texture='radial_gradient',
    color=color.rgba(255, 160, 20, 0.6),
    scale=9.0,
    billboard=True,  # Automatically rotates to face the active camera
    unlit=True
)

# --- 4. Planet & Orbit ---
planet_pivot = Entity(position=(0, 0, 0))
ORBIT_RADIUS = 8

planet = Entity(
    parent=planet_pivot,
    model='sphere',
    color=color.azure,
    scale=0.8,
    position=(ORBIT_RADIUS, 0, 0)
)

orbit_ring = Entity(
    model='circle',
    scale=(ORBIT_RADIUS * 2, ORBIT_RADIUS * 2),
    rotation_x=90,
    color=color.rgba(255, 255, 255, 0.15),
    mode='line',
    thickness=1.5
)

# --- 5. Main Loop (Pulsing & Rotation) ---
def update():
    # Slowly rotate the plasma surface on the core
    sun_core.rotation_y += 4 * time.dt
    
    # Orbit and rotate planet
    planet_pivot.rotation_y += 30 * time.dt
    planet.rotation_y += 100 * time.dt
    
    # Pulse atmosphere layers out-of-phase for dynamic living star effect
    t = time.time()
    inner_glow.scale = 2.8 + math.sin(t * 2.5) * 0.08
    outer_glow.scale = 3.3 + math.cos(t * 1.8) * 0.12
    
    # Fluctuate corona halo opacity subtly
    corona_halo.color = color.rgba(255, 160, 20, 0.55 + math.sin(t * 3.0) * 0.08)

EditorCamera(rotation=(25, -30, 0))
app.run()