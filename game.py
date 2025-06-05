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
plant_x, plant_y = 540, 320
plant_width, plant_height = plant_frames[0].get_size()
plant_center_x = plant_x + plant_width // 2
plant_center_y = plant_y + plant_height // 2
plant_horizontal_bound = 20
plant_vertical_bound = 50

#cat frames
cat_frame_path = "./assets/cat_opened_eyes.png"
cat_frame = pygame.transform.scale(pygame.image.load(cat_frame_path).convert_alpha(), (150, 150))
cat_closed_eye = "./assets/cat_closed_eyes.png"
cat_closed_eye_frame = pygame.transform.scale(pygame.image.load(cat_closed_eye).convert_alpha(), (150, 150))
cat_x, cat_y = 800, 400
cat_width, cat_height = cat_frame.get_size()
cat_center_x = cat_x + cat_width // 2
cat_center_y = cat_y + cat_height // 2
cat_horizontal_bound = 50
cat_vertical_bound = 20


# water drop frame
water_frame_path = "./assets/water_drop.png"
water_frame = pygame.transform.scale(pygame.image.load(water_frame_path).convert_alpha(), (50, 50))

# Set up the clock (for FPS)
clock = pygame.time.Clock()
fps = 95

water_visible = False
cat_closed_eye_visible = False
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
    screen.blit(plant_frames[plant_frame_index], (plant_x, plant_y))
    
    # Draw cat
    screen.blit(cat_frame, (cat_x, cat_y))
    

    if click_time is not None:
        current_time = pygame.time.get_ticks()
        
        dy = mouse_y - cat_center_y
        dx = mouse_x - cat_center_x
        # Cat closed eyes condition
        if abs(dx) <= cat_horizontal_bound and abs(dy) <= cat_vertical_bound and current_time - click_time <= 500:
            cat_closed_eye_visible = True
        else:
            cat_closed_eye_visible = False
        
        # Water drop condition
        dy = mouse_y - plant_center_y
        dx = mouse_x - plant_center_x
        if abs(dx) <= plant_horizontal_bound and abs(dy) <= plant_vertical_bound and current_time - click_time <= 1000:
            water_visible = True
            mouse_y += 0.3 # move the drop slowly down
        else:
            water_visible = False
            
    # Draw water drop
    if water_visible:
        screen.blit(water_frame, (mouse_x - 20, mouse_y -20))
        
    # Draw cat closed eyes
    if cat_closed_eye_visible:
        screen.blit(cat_closed_eye_frame, (cat_x, cat_y))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
