import pygame
import os
import random
from get_image import get_images_from_pexels 
import math
import pygame.gfxdraw
# Constants for screen dimensions
WIDTH, HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 140, 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_NAME = pygame.font.match_font('arial')
GREY = (119,136,153)
IMAGE = 'splice\\background\\player_music_display_114988_800x600.jpg'
def main_input():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mood Input")

    input_box = pygame.Rect(WIDTH // 4 + 3, HEIGHT // 2, BUTTON_WIDTH * 2, BUTTON_HEIGHT)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    done = False
    # Load the image
    background_image = pygame.image.load(IMAGE)
    # Instruction Font
    instruction_font = pygame.font.Font(None, 40)  # Change the size as needed

    while not done:
        # screen.fill(WHITE)
        # Blit the image onto the screen
        screen.blit(background_image, (0, 0))

        # Render and display the instruction text
        instruction_text = instruction_font.render("What do you want to tell me", True, WHITE)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 100))

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

        txt_surface = font.render(text, True, GREY)  


        # width = max(BUTTON_WIDTH * 2, txt_surface.get_width() + 10)
        # input_box.w = width
        # input_box.h = txt_surface.get_height() + 10 + BUTTON_HEIGHT  # Update the height of the input box
        # screen.blit(txt_surface, (input_box.x + 6 , input_box.y + 5 + BUTTON_HEIGHT))


        lines = [text[i:i + 30] for i in range(0, len(text), 30)] # Break the text into lines of 30 characters
        y_offset = 0
        input_box_width = 395 # Set the initial width to BUTTON_WIDTH * 2

        for i, line in enumerate(lines):
            txt_surface = font.render(line, True, GREY)
            screen.blit(txt_surface, (input_box.x + 6, input_box.y + 5 + BUTTON_HEIGHT + y_offset))

            # If the first line is full, set the width of the input box
            if i == 0 and len(line) == 30:
                input_box_width = 395

            y_offset += txt_surface.get_height() + 5 # Adjust the vertical spacing for the next line

        # Set the dimensions of the input box
        input_box.w = input_box_width
        input_box.h = y_offset + BUTTON_HEIGHT + 5 # Set the height based on the total height of the text
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
    # Load the image
    background_image = pygame.image.load(IMAGE)
    ICON_SIZE = (240, 180)
    BUTTON_WIDTH, BUTTON_HEIGHT = ICON_SIZE
    BUTTON_MARGIN = 70

    # Determine the folder to choose the images from
    folder = 'icons\\POS\\' if sentiment_score >= 0 else 'icons\\NEG\\'

    # Randomly select images that haven't been selected before
    available_images = [img for img in os.listdir(folder) if img not in selected_icons]
    chosen_images = random.sample(available_images, 4)

    # Fetch images from Pexels
    chosen_images = get_images_from_pexels(word)
    if len(chosen_images) < 4:
        # Fallback to local images
        folder = 'icons\\POS\\' if sentiment_score >= 0 else 'icons\\NEG\\'
        available_images = [img for img in os.listdir(folder) if img not in selected_icons]
        temp_images = random.sample(available_images, 4-len(chosen_images))
        chosen_images = chosen_images.append(temp_images)
        selected_icons.append(temp_images)
        chosen_images = [img for img in chosen_images if img is not None]
        images = [pygame.image.load(os.path.join(folder, img)) for img in chosen_images]
    else:
        images = chosen_images#[pygame.image.load(requests.get(img["src"]["medium"]).content) for img in chosen_images]
        images = [pygame.image.load(img_path) for img_path in images]

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
    CONFIRM_BUTTON_WIDTH = 200
    CONFIRM_BUTTON_HEIGHT = 50
    confirm_button_y = START_Y + (2 * BUTTON_HEIGHT) + BUTTON_MARGIN + 15 # 15 pixels below the custom images
    confirm_button = pygame.Rect((WIDTH - CONFIRM_BUTTON_WIDTH) // 2, confirm_button_y, CONFIRM_BUTTON_WIDTH, CONFIRM_BUTTON_HEIGHT)

    
    selected_audio_file = None

    running = True
    while running:
        screen.blit(background_image, (0, 0))
        draw_text(screen, f"Please select music for '{word}':", 32, WIDTH // 2, 20, (0, 0, 0))

        # Draw buttons and images
        for i, button in enumerate(buttons):
            pygame.draw.rect(screen, (0, 0, 0), button, 2)
            screen.blit(images[i], (button.x, button.y))

        # Draw confirm button
        # pygame.draw.rect(screen, (0, 0, 0), confirm_button, 2)
        draw_rounded_rect(screen, confirm_button, (0, 0, 0), 10)
        draw_text(screen, "Confirm", 30, confirm_button.x + CONFIRM_BUTTON_WIDTH // 2, confirm_button.y + CONFIRM_BUTTON_HEIGHT // 2 - 17, (0, 0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
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
                    return selected_audio_file

        pygame.display.flip()

    pygame.quit()


def draw_rounded_rect(surface, rect, color, corner_radius):
    """Draw the outline of a rounded rectangle."""
    pygame.draw.line(surface, color, (rect.left + corner_radius, rect.top), (rect.right - corner_radius, rect.top), 1)
    pygame.draw.line(surface, color, (rect.left + corner_radius, rect.bottom), (rect.right - corner_radius, rect.bottom), 1)
    pygame.draw.line(surface, color, (rect.left, rect.top + corner_radius), (rect.left, rect.bottom - corner_radius), 1)
    pygame.draw.line(surface, color, (rect.right, rect.top + corner_radius), (rect.right, rect.bottom - corner_radius), 1)

    pygame.gfxdraw.arc(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, 180, 270, color)
    pygame.gfxdraw.arc(surface, rect.right - corner_radius, rect.top + corner_radius, corner_radius, 270, 360, color)
    pygame.gfxdraw.arc(surface, rect.left + corner_radius, rect.bottom - corner_radius, corner_radius, 90, 180, color)
    pygame.gfxdraw.arc(surface, rect.right - corner_radius, rect.bottom - corner_radius, corner_radius, 0, 90, color)

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


# def magic_starts_page():
#     pygame.init()
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     background_image = pygame.image.load(IMAGE)
#     pygame.display.set_caption("Magic Starts!")
    
#     progress = 0
#     running = True
    
#     while running:
#         screen.blit(background_image, (0, 0))
#         draw_text(screen, "Magic Starts!", 32, WIDTH // 2, 100, WHITE)
        
#         # Draw the progress bar
#         pygame.draw.rect(screen, GREY, (WIDTH // 4 + 3, HEIGHT // 2, (WIDTH // 2) * progress / 100 -3, BUTTON_HEIGHT), 2)
        
#         # Increment progress
#         progress += 1
#         if progress > 100:
#             running = False
            
#         pygame.display.flip()
#         pygame.time.delay(50)  # Adjust the delay for the desired speed of the progress bar

def magic_starts_page(num_files):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background_image = pygame.image.load(IMAGE)
    pygame.display.set_caption("Magic Starts!")

    progress = 0
    running = True
    delay = (3000 * num_files) // 100  # Calculate the delay based on the number of files, 3 seconds per file

    while running:
        screen.blit(background_image, (0, 0))
        draw_text(screen, "Magic Starts!", 32, WIDTH // 2, 100, WHITE)

        # Draw the progress bar
        pygame.draw.rect(screen, GREY, (WIDTH // 4 + 3, HEIGHT // 2, (WIDTH // 2) * progress / 100 - 3, BUTTON_HEIGHT), 2)

        # Increment progress
        progress += 1
        if progress > 100:
            running = False

        pygame.display.flip()
        pygame.time.delay(delay)  # Adjust the delay for the desired speed of the progress bar based on the number of files


# def music_ready_page(music_file):
#     pygame.init()
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption("Here's Your Music!")
#     background_image = pygame.image.load(IMAGE)
    
#     play_button_center = (485, 325)
#     triangle_base = 40
#     triangle_height = 40



#     running = True
#     music_played = False
#     while running:
#         screen.blit(background_image, (0, 0))
#         draw_text(screen, "Here's your music!", 32, WIDTH // 2, 100, WHITE)

#         triangle_points = [
#             (play_button_center[0] - triangle_base // 2, play_button_center[1] - triangle_height // 2),
#             (play_button_center[0] - triangle_base // 2, play_button_center[1] + triangle_height // 2),
#             (play_button_center[0] + triangle_base // 2, play_button_center[1]),
#         ]

#         play_button_rect = pygame.draw.polygon(screen, BLACK, triangle_points)

#         if music_played:
#             draw_text(screen, "Hope you enjoy the process and the music!", 30, WIDTH // 2, HEIGHT - 135, BLACK)

#         pygame.display.flip()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if play_button_rect.collidepoint(event.pos):
#                     pygame.mixer.init()
#                     pygame.mixer.music.load(music_file)
#                     pygame.mixer.music.play()
#                     music_played = True

#         while pygame.mixer.music.get_busy():  # Wait for the music to finish playing
#             pygame.time.Clock().tick(10)  # You can adjust the tick rate as needed

#     pygame.quit()

def music_ready_page(music_file):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Here's Your Music!")
    background_image = pygame.image.load(IMAGE)
    
    play_button_center = (485, 325)
    triangle_base = 40
    triangle_height = 40

    running = True
    music_played = False
    music_finished = False
    while running:
        screen.blit(background_image, (0, 0))
        draw_text(screen, "Here's your music!", 32, WIDTH // 2, 100, WHITE)

        triangle_points = [
            (play_button_center[0] - triangle_base // 2, play_button_center[1] - triangle_height // 2),
            (play_button_center[0] - triangle_base // 2, play_button_center[1] + triangle_height // 2),
            (play_button_center[0] + triangle_base // 2, play_button_center[1]),
        ]

        play_button_rect = pygame.draw.polygon(screen, BLACK, triangle_points)

        if music_finished:
            draw_text(screen, "Hope you enjoy the process and the music!", 30, WIDTH // 2, HEIGHT - 135, BLACK)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos) and not pygame.mixer.music.get_busy():
                    pygame.mixer.init()
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.play()
                    music_played = True

        if music_played and not pygame.mixer.music.get_busy():
            music_finished = True

        pygame.time.Clock().tick(3)  # You can adjust the tick rate as needed

    pygame.quit()



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
# music_ready_page("output.wav")