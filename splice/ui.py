import pygame
import os
import random

# Constants for screen dimensions
WIDTH, HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 140, 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_NAME = pygame.font.match_font('arial')

def main_input():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mood Input")

    input_box = pygame.Rect(WIDTH // 4, HEIGHT // 2, BUTTON_WIDTH * 2, BUTTON_HEIGHT)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    done = False

    # Instruction Font
    instruction_font = pygame.font.Font(None, 40)  # Change the size as needed

    while not done:
        screen.fill(WHITE)

        # Render and display the instruction text
        instruction_text = instruction_font.render("Please type several words to describe your mood", True, BLACK)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        txt_surface = font.render(text, True, BLACK)  # Change color to BLACK for better visibility
        width = max(BUTTON_WIDTH * 2, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return text

def select_files(word, audio_files, sentiment_score, selected_icons):
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Select music for {word}")

    ICON_SIZE = (240, 180)
    BUTTON_WIDTH, BUTTON_HEIGHT = ICON_SIZE
    BUTTON_MARGIN = 60

    # Determine the folder to choose the images from
    folder = 'icons\\POS\\' if sentiment_score >= 0 else 'icons\\NEG\\'

    # Randomly select images that haven't been selected before
    available_images = [img for img in os.listdir(folder) if img not in selected_icons]
    chosen_images = random.sample(available_images, 4)

    # Load images and resize them
    images = [pygame.image.load(os.path.join(folder, img)) for img in chosen_images]
    images = [pygame.transform.scale(img, ICON_SIZE) for img in images]

    # Define the starting position for the buttons
    START_X = (WIDTH - (2 * BUTTON_WIDTH + BUTTON_MARGIN)) // 2
    START_Y = (HEIGHT - (2 * BUTTON_HEIGHT + BUTTON_MARGIN)) // 2

    # Define buttons for each audio file
    buttons = [pygame.Rect(START_X + (i % 2) * (BUTTON_WIDTH + BUTTON_MARGIN), START_Y + (i // 2) * (BUTTON_HEIGHT + BUTTON_MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT) for i in range(4)]
    sounds = [pygame.mixer.Sound(file) for file in audio_files]
    current_sound = None
    
    # Confirm button as a rectangle at the bottom
    # Confirm button as a rectangle at the bottom
    CONFIRM_BUTTON_WIDTH = 350
    CONFIRM_BUTTON_HEIGHT = 50
    confirm_button_y = START_Y + (2 * BUTTON_HEIGHT) + BUTTON_MARGIN + 15 # 15 pixels below the custom images
    confirm_button = pygame.Rect((WIDTH - CONFIRM_BUTTON_WIDTH) // 2, confirm_button_y, CONFIRM_BUTTON_WIDTH, CONFIRM_BUTTON_HEIGHT)

    
    selected_audio_file = None

    running = True
    while running:
        screen.fill((255, 255, 255))
        draw_text(screen, f"Please select music for '{word}':", 32, WIDTH // 2, 20, (0, 0, 0))

        draw_buttons_and_images(screen, buttons, images)
        draw_confirm_button(screen, confirm_button, CONFIRM_BUTTON_WIDTH, CONFIRM_BUTTON_HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                current_sound, selected_audio_file = handle_button_click(event.pos, buttons, sounds, confirm_button, current_sound, selected_audio_file, audio_files)
                if selected_audio_file:
                    return selected_audio_file

        pygame.display.flip()

    pygame.quit()

def draw_buttons_and_images(screen, buttons, images):
    for i, button in enumerate(buttons):
        pygame.draw.rect(screen, (0, 0, 0), button, 2)
        screen.blit(images[i], (button.x, button.y))

def draw_confirm_button(screen, confirm_button, confirm_button_width, confirm_button_height):
    pygame.draw.rect(screen, (0, 0, 0), confirm_button, 2)
    draw_text(screen, "Confirm", 20, confirm_button.x + confirm_button_width // 2, confirm_button.y + confirm_button_height // 2 - 10, (0, 0, 0))

def handle_button_click(mouse_pos, buttons, sounds, confirm_button, current_sound, selected_audio_file, audio_files):
    for i, button in enumerate(buttons):
        if button.collidepoint(mouse_pos):
            if current_sound:
                current_sound.stop()
            current_sound = sounds[i]
            current_sound.play()
            selected_audio_file = audio_files[i]
            break

    if confirm_button.collidepoint(mouse_pos) and selected_audio_file:
        if current_sound:
            current_sound.stop()
        return current_sound, selected_audio_file

    return current_sound, None

# def select_files(word, audio_files, sentiment_score, selected_icons):
#     pygame.init()
#     pygame.mixer.init()
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption(f"Select music for {word}")

#     ICON_SIZE = (200, 200)
#     BUTTON_WIDTH, BUTTON_HEIGHT = ICON_SIZE
#     BUTTON_MARGIN = 60

#     # Determine the folder to choose the images from
#     folder = 'icons\\POS\\' if sentiment_score >= 0 else 'icons\\NEG\\'

#     # Randomly select images that haven't been selected before
#     available_images = [img for img in os.listdir(folder) if img not in selected_icons]
#     chosen_images = random.sample(available_images, 4)

#     # Load images and resize them
#     images = [pygame.image.load(os.path.join(folder, img)) for img in chosen_images]
#     images = [pygame.transform.scale(img, ICON_SIZE) for img in images]

#     # Define the starting position for the buttons
#     START_X = (WIDTH - (2 * BUTTON_WIDTH + BUTTON_MARGIN)) // 2
#     START_Y = (HEIGHT - (2 * BUTTON_HEIGHT + BUTTON_MARGIN)) // 2

#     # Define buttons for each audio file
#     buttons = [pygame.Rect(START_X + (i % 2) * (BUTTON_WIDTH + BUTTON_MARGIN), START_Y + (i // 2) * (BUTTON_HEIGHT + BUTTON_MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT) for i in range(4)]
#     sounds = [pygame.mixer.Sound(file) for file in audio_files]
#     current_sound = None
    
#     # Confirm button as a rectangle at the bottom
#     # Confirm button as a rectangle at the bottom
#     CONFIRM_BUTTON_WIDTH = 350
#     CONFIRM_BUTTON_HEIGHT = 50
#     confirm_button_y = START_Y + (2 * BUTTON_HEIGHT) + BUTTON_MARGIN + 15 # 15 pixels below the custom images
#     confirm_button = pygame.Rect((WIDTH - CONFIRM_BUTTON_WIDTH) // 2, confirm_button_y, CONFIRM_BUTTON_WIDTH, CONFIRM_BUTTON_HEIGHT)

    
#     selected_audio_file = None

#     running = True
#     while running:
#         screen.fill((255, 255, 255))
#         draw_text(screen, f"Please select music for '{word}':", 32, WIDTH // 2, 20, (0, 0, 0))

#         # Draw buttons and images
#         for i, button in enumerate(buttons):
#             pygame.draw.rect(screen, (0, 0, 0), button, 2)
#             screen.blit(images[i], (button.x, button.y))

#         # Draw confirm button
#         pygame.draw.rect(screen, (0, 0, 0), confirm_button, 2)
#         draw_text(screen, "Confirm", 20, confirm_button.x + CONFIRM_BUTTON_WIDTH // 2, confirm_button.y + CONFIRM_BUTTON_HEIGHT // 2 - 10, (0, 0, 0))

#         # Event handling
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#             # Handle button clicks
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_pos = event.pos
#                 for i, button in enumerate(buttons):
#                     if button.collidepoint(mouse_pos):
#                         if current_sound:
#                             current_sound.stop()
#                         current_sound = sounds[i]
#                         current_sound.play()
#                         selected_audio_file = audio_files[i]
#                         break

#                 if confirm_button.collidepoint(mouse_pos) and selected_audio_file:
#                     if current_sound:
#                         current_sound.stop()
#                     return selected_audio_file

#         pygame.display.flip()

#     pygame.quit()



# def select_files(word, audio_files):
#     pygame.init()
#     pygame.mixer.init()  # Initialize the mixer module
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption(f"Select music for {word}")

#     # Define buttons for each audio file
#     buttons = [pygame.Rect(300, 100 + i*60, BUTTON_WIDTH, BUTTON_HEIGHT) for i in range(len(audio_files))]
#     button_colors = [random_color() for _ in range(len(audio_files))] # Random colors for buttons
#     sounds = [pygame.mixer.Sound(file) for file in audio_files]  # Load the audio files
#     current_sound = None
#     confirm_button = pygame.Rect(300, 100 + len(audio_files)*60, BUTTON_WIDTH, BUTTON_HEIGHT)  # Confirm button
#     selected_audio_file = None

#     running = True
#     while running:
#         screen.fill(WHITE)
#         draw_text(screen, f"Please select music for '{word}':", 32, WIDTH // 2, 20, BLACK)

#         # Draw buttons
#         for i, button in enumerate(buttons):
#             pygame.draw.rect(screen, button_colors[i], button) # Fill with random color
#             pygame.draw.rect(screen, BLACK, button, 2)

#         # Draw confirm button
#         pygame.draw.rect(screen, BLACK, confirm_button, 2)
#         draw_text(screen, "Confirm", 20, confirm_button.x + BUTTON_WIDTH // 2, confirm_button.y + BUTTON_HEIGHT // 2 - 10, BLACK)

#         # Event handling
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#             # Handle button clicks
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_pos = event.pos
#                 for i, button in enumerate(buttons):
#                     if button.collidepoint(mouse_pos):
#                         # Stop current sound if playing
#                         if current_sound:
#                             current_sound.stop()
#                         # Play the selected sound
#                         current_sound = sounds[i]
#                         current_sound.play()
#                         selected_audio_file = audio_files[i]
#                         break

#                 # Confirm button handling
#                 if confirm_button.collidepoint(mouse_pos) and selected_audio_file:
#                     if current_sound:
#                         current_sound.stop()  # Stop the sound when confirmed
#                     return selected_audio_file

#         pygame.display.flip()

#     pygame.quit()

def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


# def play_music(name):
#     pygame.mixer.init()
#     pygame.mixer.music.load(name)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():  # Wait for the music to finish playing
#         pygame.time.Clock().tick(10)  # You can adjust the tick rate as needed


def magic_starts_page():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Magic Starts!")
    
    progress = 0
    running = True
    
    while running:
        screen.fill(WHITE)
        draw_text(screen, "Magic Starts!", 32, WIDTH // 2, 20, BLACK)
        
        # Draw the progress bar
        pygame.draw.rect(screen, BLACK, (WIDTH // 4, HEIGHT // 2, (WIDTH // 2) * progress / 100, BUTTON_HEIGHT), 2)
        
        # Increment progress
        progress += 1
        if progress > 100:
            running = False
            
        pygame.display.flip()
        pygame.time.delay(50)  # Adjust the delay for the desired speed of the progress bar

def music_ready_page(music_file):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Here's Your Music!")
    
    screen.fill(WHITE)
    draw_text(screen, "Here's your music!", 32, WIDTH // 2, 20, BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    pygame.time.delay(2000)  # Delay for 2 seconds before starting music
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for the music to finish playing
        pygame.time.Clock().tick(10)  # You can adjust the tick rate as needed


# def select_files(word, audio_files):
#     pygame.init()
#     pygame.mixer.init()  # Initialize the mixer module
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption(f"Select music for {word}")

#     # Define buttons for each audio file
#     buttons = [pygame.Rect(300, 100 + i*60, BUTTON_WIDTH, BUTTON_HEIGHT) for i in range(len(audio_files))]
#     sounds = [pygame.mixer.Sound(file) for file in audio_files]  # Load the audio files
#     current_sound = None
#     confirm_button = pygame.Rect(300, 100 + len(audio_files)*60, BUTTON_WIDTH, BUTTON_HEIGHT)  # Confirm button
#     selected_audio_file = None

#     running = True
#     while running:
#         screen.fill(WHITE)
#         draw_text(screen, f"Please select music for '{word}':", 32, WIDTH // 2, 20, BLACK)

#         # Draw buttons
#         for i, button in enumerate(buttons):
#             pygame.draw.rect(screen, BLACK, button, 2)
#             draw_text(screen, os.path.basename(audio_files[i]), 20, button.x + BUTTON_WIDTH // 2, button.y + BUTTON_HEIGHT // 2 - 10, BLACK)

#         # Draw confirm button
#         pygame.draw.rect(screen, BLACK, confirm_button, 2)
#         draw_text(screen, "Confirm", 20, confirm_button.x + BUTTON_WIDTH // 2, confirm_button.y + BUTTON_HEIGHT // 2 - 10, BLACK)

#         # Event handling
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#             # Handle button clicks
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_pos = event.pos
#                 for i, button in enumerate(buttons):
#                     if button.collidepoint(mouse_pos):
#                         # Stop current sound if playing
#                         if current_sound:
#                             current_sound.stop()
#                         # Play the selected sound
#                         current_sound = sounds[i]
#                         current_sound.play()
#                         selected_audio_file = audio_files[i]
#                         break

#                 # Confirm button handling
#                 if confirm_button.collidepoint(mouse_pos) and selected_audio_file:
#                     return selected_audio_file

#         pygame.display.flip()

#     pygame.quit()

# def draw_text(surf, text, size, x, y, color):
#     font = pygame.font.Font(FONT_NAME, size)
#     text_surface = font.render(text, True, color)
#     text_rect = text_surface.get_rect()
#     text_rect.midtop = (x, y)
#     surf.blit(text_surface, text_rect)
