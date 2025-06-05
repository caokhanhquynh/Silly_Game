import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 700, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Watering Quinnie's Tree")

# background music
bg_sound = pygame.mixer.Sound("./assets/sound.mp3")
bg_sound.set_volume(0.1)
bg_sound.play(loops=-1)

# water sound
water_plant_sound = pygame.mixer.Sound("./assets/water_plant_sound.mp3")
water_plant_sound.set_volume(1.0)

# cat sound
cat_sound = pygame.mixer.Sound("./assets/cat.mp3")
cat_sound.set_volume(1.0)

# background frames
frame_folder = "./assets/cafebg.png"
frame = pygame.transform.scale(pygame.image.load(frame_folder).convert_alpha(), (700, 700))
frame_index = 0
frame_timer = 0
frame_delay = 100

# plant frames
plant_frame_path = "./assets/plant"
plant_frame_files = sorted([f for f in os.listdir(plant_frame_path) if f.startswith("frame_") and f.endswith(".png")])
plant_frames = [
    pygame.transform.scale(
        pygame.image.load(os.path.join(plant_frame_path, f)).convert_alpha(),
        (230, 230)
    )
    for f in plant_frame_files
]
plant_frame_index = 0
plant_x, plant_y = 78, 335
plant_width, plant_height = plant_frames[0].get_size()
plant_center_x = plant_x + plant_width // 2
plant_center_y = plant_y + plant_height // 2
plant_horizontal_bound = 20
plant_vertical_bound = 50

# dog frames
dog_frame_path = "./assets/dog1.png"
dog_frame_path2 = "./assets/dog2.png"
dog_frames = [pygame.transform.scale(pygame.image.load(dog_frame_path).convert_alpha(), (250, 250)), pygame.transform.scale(pygame.image.load(dog_frame_path2).convert_alpha(), (250, 250))]
dog_frame_index = 0
dog_x, dog_y = 0, 325

#cat frames
cat_frame_index = 0
cat_frame_timer = 0
cat_frame_delay = 300
cat_frame_path = "./assets/cat_opened_eyes.png"
cat_frame_path_2 = "./assets/cat_opened_eyes2.png"
cat_frames = [pygame.transform.scale(pygame.image.load(cat_frame_path).convert_alpha(), (180, 180)), pygame.transform.scale(pygame.image.load(cat_frame_path_2).convert_alpha(), (180, 180))]
cat_closed_eye = "./assets/cat_closed_eyes.png"
cat_closed_eye_frame = pygame.transform.scale(pygame.image.load(cat_closed_eye).convert_alpha(), (180, 180))
cat_x, cat_y = 520, 360
cat_width, cat_height = cat_frames[0].get_size()
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
water_sound_played = False
cat_sound_played = False
while running:
    dt = clock.tick(fps)  # time since last tick in ms
    frame_timer += dt
    cat_frame_timer += dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            click_time = pygame.time.get_ticks()

    # Animation frame
    if frame_timer >= frame_delay:
        frame_timer = 0
        plant_frame_index = (plant_frame_index + 1) % len(plant_frames)
        plant_frame_timer = 0
    
    # Cat animation frame
    if cat_frame_timer >= cat_frame_delay:
        cat_frame_index = (cat_frame_index + 1) % len(cat_frames)
        cat_frame_timer = 0
        dog_frame_index = (plant_frame_index + 1) % len(dog_frames)
        dog_frame_timer = 0
        if dog_x < screen_width:
            dog_x += 10
        else:
            dog_x = 0

    # Draw current frame as background
    screen.blit(frame, (0, 0))
    screen.blit(plant_frames[plant_frame_index], (plant_x, plant_y))
    
    # Mouse click condition
    if click_time is not None:
        current_time = pygame.time.get_ticks()
        
        dy = mouse_y - cat_center_y
        dx = mouse_x - cat_center_x
        
        # Cat closed eyes condition
        if abs(dx) <= cat_horizontal_bound and abs(dy) <= cat_vertical_bound and current_time - click_time <= 500:
            cat_closed_eye_visible = True
            if not cat_sound_played:
                cat_sound.play()
                cat_sound_played = True
        else:
            cat_closed_eye_visible = False
            cat_sound_played = False
        
        # Water drop condition
        dy = mouse_y - plant_center_y
        dx = mouse_x - plant_center_x
        in_plant_range = abs(dx) <= plant_horizontal_bound and abs(dy) <= plant_vertical_bound
        if in_plant_range and current_time - click_time <= 1000:
            if not water_sound_played:
                water_plant_sound.play()
                water_sound_played = True
            water_visible = True
            mouse_y += 0.3 # move the drop slowly down
        else:
            water_visible = False
            water_sound_played = False 
    
    # Draw dog
    screen.blit(dog_frames[dog_frame_index], (dog_x, dog_y))
    
    # Draw water drop
    if water_visible:
        screen.blit(water_frame, (mouse_x - 20, mouse_y -20))
        
    # Draw cat
    if cat_closed_eye_visible:
        screen.blit(cat_closed_eye_frame, (cat_x, cat_y))
    else:
        screen.blit(cat_frames[cat_frame_index], (cat_x, cat_y))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
