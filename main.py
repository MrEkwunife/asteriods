import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import ASTEROID_MIN_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # --- Sprite groups ---
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # --- Containers setup ---
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    # --- Game objects ---
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    running = True
    while running:
        log_state()

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Delta time ---
        dt = clock.tick(60) / 1000  # seconds

        # --- Update all updatable sprites ---
        for sprite in updatable:
            sprite.update(dt)

        # --- Check collisions between shots and asteroids ---
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()

        # --- Check collisions between player and asteroids ---
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                pygame.quit()
                sys.exit()

        # --- Draw everything ---
        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
