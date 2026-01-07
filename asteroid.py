import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            (int(self.position.x), int(self.position.y)),
            int(self.radius),
            LINE_WIDTH,
        )

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        # This asteroid is always destroyed
        self.kill()

        # If it's already small, stop here
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Otherwise, split into two smaller asteroids
        log_event("asteroid_split")

        angle = random.uniform(20, 50)

        velocity1 = self.velocity.rotate(angle)
        velocity2 = self.velocity.rotate(-angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        asteroid1.velocity = velocity1 * 1.2
        asteroid2.velocity = velocity2 * 1.2
