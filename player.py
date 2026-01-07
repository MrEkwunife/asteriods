import pygame

from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0

    def triangle(self):
        """Return points of the triangle representing the player ship."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        # Prevent shooting if cooldown is active
        if self.shot_cooldown > 0:
            return

        shot = Shot(self.position.x, self.position.y)
        velocity = pygame.Vector2(0, -1).rotate(self.rotation)
        shot.velocity = velocity * PLAYER_SHOOT_SPEED

        # Reset cooldown
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

    def update(self, dt):
        # Decrease cooldown timer
        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt

        keys = pygame.key.get_pressed()

        # Rotation
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        # Movement
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

        # Shooting
        if keys[pygame.K_SPACE]:
            self.shoot()
