import pygame
import sys

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Unpacking Off Brand")

# Load images
background = pygame.image.load('room.png')
box_image = pygame.image.load('box.png')

# Load object images and create a queue
object_images = ['object1.png', 'object2.png', 'object3.png']  # List of object images
object_queue = [pygame.image.load(obj) for obj in object_images]

# Initial positions
box_rect = box_image.get_rect(topleft=(100, 100))
placed_objects = []
current_object = None
dragging = False

def can_place_object(new_rect, placed_objects):
    for surface, rect in placed_objects:
        if new_rect.colliderect(rect):
            return False
    return True

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if box_rect.collidepoint(event.pos) and object_queue:
                current_object = object_queue.pop(0)
                current_rect = current_object.get_rect(topleft=event.pos)
                dragging = True
                mouse_x, mouse_y = event.pos
                offset_x = current_rect.x - mouse_x
                offset_y = current_rect.y - mouse_y

            elif current_object and current_rect.collidepoint(event.pos):
                dragging = True
                mouse_x, mouse_y = event.pos
                offset_x = current_rect.x - mouse_x
                offset_y = current_rect.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                if can_place_object(current_rect, placed_objects):
                    placed_objects.append((current_object, current_rect))
                    current_object = None
                dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging and current_object:
                mouse_x, mouse_y = event.pos
                current_rect.x = mouse_x + offset_x
                current_rect.y = mouse_y + offset_y

    # Draw everything
    screen.blit(background, (0, 0))
    screen.blit(box_image, box_rect.topleft)
    for surface, rect in placed_objects:
        screen.blit(surface, rect.topleft)
    if current_object:
        screen.blit(current_object, current_rect.topleft)
    pygame.display.flip()