import pygame
import sys
import os

pygame.init()

screen_width, screen_height = 1200, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Watering Quinnie's Tree")

# background frames
frame_folder = "./assets/bg"
frame_files = sorted([f for f in os.listdir(frame_folder) if f.startswith("frame_") and f.endswith(".png")])
frames = [
    pygame.transform.scale(
        pygame.image.load(os.path.join(frame_folder, f)).convert(),
        (screen_width, screen_height)
    )
    for f in frame_files
]
frame_index = 0
frame_timer = 0
frame_delay = 100

# plant frames
plant_frame_path = "./assets/plant"
plant_frame_files = sorted([f for f in os.listdir(plant_frame_path) if f.startswith("frame_") and f.endswith(".png")])
plant_frames = [
    pygame.transform.scale(
        pygame.image.load(os.path.join(plant_frame_path, f)).convert_alpha(),
        (200, 200)
    )
    for f in plant_frame_files
]
plant_frame_index = 0

# water drop frame
water_frame_path = "./assets/water_drop.png"
water_frame = pygame.transform.scale(pygame.image.load(water_frame_path).convert_alpha(), (50, 50))

# Set up the clock (for FPS)
clock = pygame.time.Clock()
fps = 95

water_visible = False
click_time = None

# Main game loop
running = True
while running:
    dt = clock.tick(fps)  # time since last tick in ms
    frame_timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            click_time = pygame.time.get_ticks()

    # Update animation frame
    if frame_timer >= frame_delay:
        frame_index = (frame_index + 1) % len(frames)
        frame_timer = 0
        plant_frame_index = (plant_frame_index + 1) % len(plant_frames)
        plant_frame_timer = 0

    # Draw current frame as background
    screen.blit(frames[frame_index], (0, 0))
    screen.blit(plant_frames[plant_frame_index], (540, 320))
    
    if click_time is not None:
        current_time = pygame.time.get_ticks()
        if current_time - click_time <= 1000:
            water_visible = True
            mouse_y += 0.3
        else:
            water_visible = False
    if water_visible:
        screen.blit(water_frame, (mouse_x, mouse_y))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
