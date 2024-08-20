import pygame
import sys

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((900, 760))
pygame.display.set_caption("Unpacking Off Brand")

# Load images
background = pygame.image.load('assets/room.png')
box_image = pygame.image.load('assets/box.png')
openBox_image = pygame.image.load('assets/openBox.png')
counter_image = pygame.image.load('assets/counter.png')

# Load object images and create a queue
object_images = ['assets/object1.png', 'assets/object1.png', 'assets/object1.png']  # List of object images
object_queue = [pygame.image.load(obj) for obj in object_images]

# Initial positions
box_rect = box_image.get_rect(topleft=(600, 450))
counter_rect = counter_image.get_rect(topleft=(360, 320))
placed_objects = []  # List to store placed objects as (surface, rect) tuples
current_object = None
dragging = False

# Track box state
box_clicked = False
box_empty = False

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
            if current_object is None and box_rect.collidepoint(event.pos):
                if not box_clicked:
                    box_clicked = True
                    if object_queue:
                        box_image = openBox_image

                # Take the next object from the box and place it directly under the mouse
                if len(object_queue) > 0:
                    current_object = object_queue.pop(0)
                    current_rect = current_object.get_rect(center=event.pos)
                    dragging = True
                else:
                    box_empty = True

            elif current_object is None:
                # Check if the user clicked on any placed object
                for surface, rect in placed_objects:
                    if rect.collidepoint(event.pos):
                        current_object = surface
                        current_rect = rect
                        placed_objects.remove((surface, rect))
                        dragging = True
                        break

            else:
                placed_objects.append((current_object, current_rect))
                current_object = None
                dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging and current_object:
                mouse_x, mouse_y = event.pos
                # Center the object around the mouse
                current_rect.center = (mouse_x, mouse_y)

    # Draw everything
    screen.blit(background, (0, 0))
    screen.blit(counter_image, counter_rect.topleft)
    if not box_empty:
        screen.blit(box_image, box_rect.topleft)

    for surface, rect in placed_objects:
        screen.blit(surface, rect.topleft)
    if current_object:
        screen.blit(current_object, current_rect.topleft)
    pygame.display.flip()
