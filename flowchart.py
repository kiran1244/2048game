import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Node class
class Node(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

# Arrow class
class Arrow(pygame.sprite.Sprite):
    def __init__(self, start, end):
        super().__init__()
        self.image = pygame.Surface((2, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center=start)
        self.start = start
        self.end = end
        self.vector = pygame.math.Vector2(end[0] - start[0], end[1] - start[1])
        self.length = self.vector.length()
        self.angle = self.vector.angle_to(pygame.math.Vector2(0, -1))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=start)

    def update(self):
        self.rect.move_ip(self.vector.normalize() * 5)

# Create Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flow Chart Animation")
clock = pygame.time.Clock()

# Create sprite groups
all_sprites = pygame.sprite.Group()

# Create nodes
node1 = Node(100, 100, (255, 0, 0))
node2 = Node(300, 100, (0, 255, 0))
node3 = Node(500, 100, (0, 0, 255))

# Create arrows
arrow1 = Arrow(node1.rect.center, node2.rect.center)
arrow2 = Arrow(node2.rect.center, node3.rect.center)

# Add sprites to groups
all_sprites.add(node1, node2, node3, arrow1, arrow2)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update()

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
