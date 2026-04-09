from __future__ import annotations

from dataclasses import dataclass, field
import math
import random

import pygame

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
FPS = 60

SQUARE_COUNT = 100
MIN_SIZE = 16
MAX_SIZE = 64
MIN_SPEED = 0.8
MAX_SPEED = 3.2
MIN_ROTATION_SPEED = 0.5
MAX_ROTATION_SPEED = 4.0
DIRECTION_JITTER_CHANCE_PER_SECOND = 1.0
MAX_DIRECTION_JITTER_DEGREES = 6.0

BACKGROUND_COLOR = (0, 0, 0)
MIN_GLOBAL_SPEED = 0.25
MAX_GLOBAL_SPEED = 3.0
GLOBAL_SPEED_STEP = 0.25


@dataclass
class Square:
    # Top-left position of the square on the screen.
    x: float
    y: float
    # Visual properties.
    size: int
    color: tuple[int, int, int]
    # Velocity on each axis.
    vx: float
    vy: float
    # Rotation state for drawing.
    angle: float
    rotation_speed: float
    # The bigger the square, the lower this value should be.
    max_speed: float


@dataclass
class GameState:
    squares: list[Square]
    rng: random.Random = field(default_factory=random.Random)
    running: bool = True
    paused: bool = False
    global_speed: float = 1.0
    square_count: int = SQUARE_COUNT


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Keep a number inside a valid range."""
    return max(minimum, min(value, maximum))


def random_color(rng: random.Random) -> tuple[int, int, int]:
    """Create a bright color so the squares stand out on a black background."""
    return (
        rng.randint(90, 255),
        rng.randint(90, 255),
        rng.randint(90, 255),
    )


def compute_square_max_speed(size: int) -> float:
    """Map size to speed so smaller squares can move faster than bigger ones."""
    if MAX_SIZE == MIN_SIZE:
        return MAX_SPEED

    size_ratio = (size - MIN_SIZE) / (MAX_SIZE - MIN_SIZE)
    return MAX_SPEED - size_ratio * (MAX_SPEED - MIN_SPEED)


def create_velocity_vector(rng: random.Random, max_speed: float) -> tuple[float, float]:
    """Create a velocity whose magnitude does not exceed the square's max speed."""
    speed = rng.uniform(max_speed * 0.4, max_speed)
    angle = rng.uniform(0, 2 * math.pi)
    return math.cos(angle) * speed, math.sin(angle) * speed


def clamp_velocity_to_max_speed(square: Square) -> None:
    """Clamp the velocity magnitude if it ever drifts above the square's max speed."""
    speed = math.hypot(square.vx, square.vy)
    if speed <= square.max_speed or speed == 0:
        return

    scale = square.max_speed / speed
    square.vx *= scale
    square.vy *= scale


def create_random_square(rng: random.Random) -> Square:
    """Create one square with a random position, speed, and rotation."""
    size = rng.randint(MIN_SIZE, MAX_SIZE)
    max_speed = compute_square_max_speed(size)
    vx, vy = create_velocity_vector(rng, max_speed)

    return Square(
        x=rng.uniform(0, WINDOW_WIDTH - size),
        y=rng.uniform(0, WINDOW_HEIGHT - size),
        size=size,
        color=random_color(rng),
        vx=vx,
        vy=vy,
        angle=rng.uniform(0, 360),
        rotation_speed=rng.uniform(MIN_ROTATION_SPEED, MAX_ROTATION_SPEED)
        * rng.choice([-1, 1]),
        max_speed=max_speed,
    )


def create_squares(count: int, rng: random.Random) -> list[Square]:
    """Create the list of moving squares."""
    return [create_random_square(rng) for _ in range(count)]


def create_default_state(square_count: int = SQUARE_COUNT, seed: int | None = None) -> GameState:
    """Create the full game state."""
    rng = random.Random(seed)
    return GameState(
        squares=create_squares(square_count, rng),
        rng=rng,
        square_count=square_count,
    )


def change_global_speed(current_speed: float, delta: float) -> float:
    """Speed up or slow down all squares together."""
    return clamp(current_speed + delta, MIN_GLOBAL_SPEED, MAX_GLOBAL_SPEED)


def handle_input(state: GameState, events: list[pygame.event.Event]) -> None:
    """Handle one-time actions such as quit, reset, pause, and speed changes."""
    for event in events:
        if event.type == pygame.QUIT:
            state.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                state.running = False
            elif event.key == pygame.K_r:
                state.squares = create_squares(state.square_count, state.rng)
            elif event.key == pygame.K_SPACE:
                state.paused = not state.paused
            elif event.key == pygame.K_1:
                state.global_speed = change_global_speed(
                    state.global_speed,
                    -GLOBAL_SPEED_STEP,
                )
            elif event.key == pygame.K_2:
                state.global_speed = change_global_speed(
                    state.global_speed,
                    GLOBAL_SPEED_STEP,
                )


def apply_random_direction_jitter(
    square: Square,
    dt_seconds: float,
    rng: random.Random,
) -> None:
    """Rotate the velocity vector a little bit while preserving the speed magnitude."""
    jitter_probability = min(1.0, DIRECTION_JITTER_CHANCE_PER_SECOND * dt_seconds)
    if rng.random() >= jitter_probability:
        return

    speed = math.hypot(square.vx, square.vy)
    if speed <= 0:
        return

    angle = math.atan2(square.vy, square.vx)
    jitter_degrees = rng.uniform(
        -MAX_DIRECTION_JITTER_DEGREES,
        MAX_DIRECTION_JITTER_DEGREES,
    )
    new_angle = angle + math.radians(jitter_degrees)
    square.vx = math.cos(new_angle) * speed
    square.vy = math.sin(new_angle) * speed

    # Rotation of a vector should preserve speed, but we keep this guard so the
    # square never breaks its own max_speed rule.
    clamp_velocity_to_max_speed(square)


def update_square(square: Square, global_speed: float, dt_seconds: float, rng: random.Random) -> None:
    """Move one square, add jitter, bounce it off walls, and rotate it."""
    apply_random_direction_jitter(square, dt_seconds, rng)

    frame_scale = dt_seconds * FPS
    square.x += square.vx * global_speed * frame_scale
    square.y += square.vy * global_speed * frame_scale
    square.angle = (square.angle + square.rotation_speed * global_speed * frame_scale) % 360

    if square.x <= 0:
        square.x = 0
        square.vx *= -1
    elif square.x + square.size >= WINDOW_WIDTH:
        square.x = WINDOW_WIDTH - square.size
        square.vx *= -1

    if square.y <= 0:
        square.y = 0
        square.vy *= -1
    elif square.y + square.size >= WINDOW_HEIGHT:
        square.y = WINDOW_HEIGHT - square.size
        square.vy *= -1


def update_game_state(state: GameState, dt_seconds: float) -> None:
    """Update every square unless the animation is paused."""
    if state.paused:
        return

    for square in state.squares:
        update_square(square, state.global_speed, dt_seconds, state.rng)


def draw_square(screen: pygame.Surface, square: Square) -> None:
    """Draw one rotated square."""
    base_square = pygame.Surface((square.size, square.size), pygame.SRCALPHA)
    pygame.draw.rect(
        base_square,
        square.color,
        (0, 0, square.size, square.size),
    )

    rotated_square = pygame.transform.rotate(base_square, square.angle)
    rotated_rect = rotated_square.get_rect(
        center=(square.x + square.size / 2, square.y + square.size / 2)
    )
    screen.blit(rotated_square, rotated_rect)


def draw_scene(screen: pygame.Surface, state: GameState) -> None:
    """Draw the black background and all moving squares."""
    screen.fill(BACKGROUND_COLOR)

    for square in state.squares:
        draw_square(screen, square)


def main() -> None:
    """Run the moving squares animation."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Lab8 - Moving Squares")
    clock = pygame.time.Clock()
    state = create_default_state()

    while state.running:
        events = pygame.event.get()
        handle_input(state, events)

        dt_seconds = clock.tick(FPS) / 1000.0
        update_game_state(state, dt_seconds)
        draw_scene(screen, state)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
