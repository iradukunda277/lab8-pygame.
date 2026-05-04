from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Protocol

import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
HUD_COLOR = (240, 240, 240)

SQUARE_MIX = (
    (25, 5),
    (10, 10),
    (4, 30),
)
SQUARE_COUNT = 45
NUM_SQUARES = SQUARE_COUNT
MIN_SIZE = 10
MAX_SIZE = 40
MAX_SPEED = 6.0
MIN_SPEED = 1.5
GLOBAL_MAX_SPEED = MAX_SPEED

ANGLE_JITTER = 9.0
FLEE_DISTANCE = 100
FLEE_FORCE = 2.0

MIN_LIFE = 3
MAX_LIFE = 9
MIN_ROTATION_SPEED = -180.0
MAX_ROTATION_SPEED = 180.0


class RandomLike(Protocol):
    def uniform(self, minimum: float, maximum: float) -> float: ...


@dataclass
class Square:
    x: float
    y: float
    size: int
    color: tuple[int, int, int]
    vx: float
    vy: float
    angle: float
    rotation_speed: float
    max_speed: float
    life_span: float = 6.0
    age: float = 0.0
    original_size: int | None = None
    rect: pygame.Rect = field(init=False)

    def __post_init__(self) -> None:
        if self.original_size is None:
            self.original_size = self.size
        self.update_rect()

    def update_rect(self) -> None:
        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    @property
    def dx(self) -> float:
        return self.vx

    @dx.setter
    def dx(self, value: float) -> None:
        self.vx = value

    @property
    def dy(self) -> float:
        return self.vy

    @dy.setter
    def dy(self, value: float) -> None:
        self.vy = value

    def center_x(self) -> float:
        return self.x + self.size / 2

    def center_y(self) -> float:
        return self.y + self.size / 2


@dataclass
class GameState:
    squares: list[Square]
    rng: random.Random = field(default_factory=random.Random)
    paused: bool = False
    running: bool = True
    global_speed: float = 1.0


def compute_square_max_speed(size: int) -> float:
    if size <= MIN_SIZE:
        return MAX_SPEED
    if size >= MAX_SIZE:
        return MIN_SPEED

    size_ratio = (size - MIN_SIZE) / (MAX_SIZE - MIN_SIZE)
    return MAX_SPEED + (MIN_SPEED - MAX_SPEED) * size_ratio


def create_random_square(rng: random.Random, size: int | None = None) -> Square:
    if size is None:
        size = rng.randint(MIN_SIZE, MAX_SIZE)

    max_speed = compute_square_max_speed(size)
    speed = rng.uniform(MIN_SPEED, max_speed)
    direction = rng.uniform(0, 2 * math.pi)

    return Square(
        x=rng.uniform(0, WIDTH - size),
        y=rng.uniform(0, HEIGHT - size),
        size=size,
        color=(
            rng.randint(50, 255),
            rng.randint(50, 255),
            rng.randint(50, 255),
        ),
        vx=math.cos(direction) * speed,
        vy=math.sin(direction) * speed,
        angle=rng.uniform(0, 360),
        rotation_speed=rng.uniform(MIN_ROTATION_SPEED, MAX_ROTATION_SPEED),
        max_speed=max_speed,
        life_span=rng.uniform(MIN_LIFE, MAX_LIFE),
        original_size=size,
    )


def create_default_state(seed: int | None = None) -> GameState:
    rng = random.Random(seed)
    squares: list[Square] = []

    for size, count in SQUARE_MIX:
        for _ in range(count):
            squares.append(create_random_square(rng, size))

    return GameState(squares=squares, rng=rng)


def clamp_velocity_to_max_speed(square: Square) -> None:
    speed = math.hypot(square.vx, square.vy)
    if speed == 0 or speed <= square.max_speed:
        return

    scale = square.max_speed / speed
    square.vx *= scale
    square.vy *= scale


def apply_random_direction_jitter(
    square: Square,
    dt_seconds: float,
    rng: RandomLike = random,
) -> None:
    speed = math.hypot(square.vx, square.vy)
    if speed == 0:
        return

    direction = math.atan2(square.vy, square.vx)
    direction += rng.uniform(-ANGLE_JITTER, ANGLE_JITTER) * dt_seconds
    square.vx = math.cos(direction) * speed
    square.vy = math.sin(direction) * speed
    clamp_velocity_to_max_speed(square)


def apply_flee_behavior(
    square: Square,
    squares: list[Square],
    dt_seconds: float,
) -> None:
    for other in squares:
        if other is square or square.size >= other.size:
            continue

        away_x = square.center_x() - other.center_x()
        away_y = square.center_y() - other.center_y()
        distance = math.hypot(away_x, away_y)

        if 0 < distance < FLEE_DISTANCE:
            square.vx += (away_x / distance) * FLEE_FORCE * dt_seconds
            square.vy += (away_y / distance) * FLEE_FORCE * dt_seconds

    clamp_velocity_to_max_speed(square)


def update_square(
    square: Square,
    squares: list[Square],
    global_speed: float,
    dt_seconds: float,
    rng: RandomLike = random,
) -> None:
    apply_random_direction_jitter(square, dt_seconds, rng)
    apply_flee_behavior(square, squares, dt_seconds)
    clamp_velocity_to_max_speed(square)

    square.x += square.vx * global_speed * dt_seconds * FPS
    square.y += square.vy * global_speed * dt_seconds * FPS
    square.angle = (
        square.angle + square.rotation_speed * global_speed * dt_seconds
    ) % 360

    if square.x + square.size >= WIDTH:
        square.x = 0
    elif square.x <= 0:
        square.x = WIDTH - square.size

    if square.y + square.size >= HEIGHT:
        square.y = 0
    elif square.y <= 0:
        square.y = HEIGHT - square.size

    square.update_rect()


def check_collision(first_square: Square, second_square: Square) -> bool:
    first_square.update_rect()
    second_square.update_rect()
    return first_square.rect.colliderect(second_square.rect)


def respawn_square(state: GameState, square_index: int) -> None:
    old_square = state.squares[square_index]
    state.squares[square_index] = create_random_square(
        state.rng,
        old_square.original_size,
    )


def handle_collisions(state: GameState) -> None:
    eaten_indexes: set[int] = set()

    for first_index in range(len(state.squares)):
        if first_index in eaten_indexes:
            continue

        for second_index in range(first_index + 1, len(state.squares)):
            if second_index in eaten_indexes:
                continue

            first_square = state.squares[first_index]
            second_square = state.squares[second_index]

            if first_square.size == second_square.size:
                continue

            if not check_collision(first_square, second_square):
                continue

            if first_square.size > second_square.size:
                eaten_index = second_index
            else:
                eaten_index = first_index

            respawn_square(state, eaten_index)
            eaten_indexes.add(eaten_index)

            if eaten_index == first_index:
                break


def update_state(state: GameState, dt_seconds: float) -> None:
    if state.paused:
        return

    for index, square in enumerate(list(state.squares)):
        square.age += dt_seconds * state.global_speed

        if square.age >= square.life_span:
            respawn_square(state, index)
            square = state.squares[index]

        update_square(
            square,
            state.squares,
            global_speed=state.global_speed,
            dt_seconds=dt_seconds,
            rng=state.rng,
        )

    handle_collisions(state)


def handle_input(state: GameState, events: list[pygame.event.Event]) -> None:
    for event in events:
        if event.type == pygame.QUIT:
            state.running = False
            continue

        if event.type != pygame.KEYDOWN:
            continue

        if event.key == pygame.K_SPACE:
            state.paused = not state.paused
        elif event.key in (pygame.K_ESCAPE, pygame.K_q):
            state.running = False
        elif event.key == pygame.K_1:
            state.global_speed = max(0.25, state.global_speed * 0.8)
        elif event.key == pygame.K_2:
            state.global_speed = min(3.0, state.global_speed * 1.25)
        elif event.key == pygame.K_r:
            state.squares = []

            for size, count in SQUARE_MIX:
                for _ in range(count):
                    state.squares.append(create_random_square(state.rng, size))


def draw_square(screen: pygame.Surface, square: Square) -> None:
    square_surface = pygame.Surface((square.size, square.size), pygame.SRCALPHA)
    square_surface.fill(square.color)
    rotated_square = pygame.transform.rotate(square_surface, square.angle)
    rotated_rect = rotated_square.get_rect(
        center=(square.center_x(), square.center_y())
    )
    screen.blit(rotated_square, rotated_rect)


def draw_scene(
    screen: pygame.Surface,
    font: pygame.font.Font,
    clock: pygame.time.Clock,
    state: GameState,
) -> None:
    screen.fill(BACKGROUND_COLOR)

    for square in state.squares:
        draw_square(screen, square)

    status = "Paused" if state.paused else f"FPS: {int(clock.get_fps())}"
    hud_text = font.render(status, True, HUD_COLOR)
    speed_text = font.render(f"Speed: {state.global_speed:.2f}x", True, HUD_COLOR)
    screen.blit(hud_text, (10, 10))
    screen.blit(speed_text, (10, 36))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Squares")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    state = create_default_state()

    while state.running:
        dt_seconds = clock.tick(FPS) / 1000.0
        handle_input(state, pygame.event.get())
        update_state(state, dt_seconds)
        draw_scene(screen, font, clock, state)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
