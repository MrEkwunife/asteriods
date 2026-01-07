import pygame

from circleshape import CircleShape
from constants import LINE_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, SHOT_RADIUS


class Shot(CircleShape):
    # Containers will be set in main.py
    containers = ()

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = pygame.Vector2(0, 0)

        # Add self to all containers
        for container in self.containers:
            container.add(self)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            (int(self.position.x), int(self.position.y)),
            self.radius,
            LINE_WIDTH,
        )

    def update(self, dt):
        self.position += self.velocity * dt

        # Remove shot if it leaves screen bounds
        if (
            self.position.x < 0
            or self.position.x > SCREEN_WIDTH
            or self.position.y < 0
            or self.position.y > SCREEN_HEIGHT
        ):
            self.kill()
