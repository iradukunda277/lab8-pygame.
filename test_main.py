import math
from types import SimpleNamespace

import main


class ForcedJitterRandom:
    def random(self) -> float:
        return 0.0

    def uniform(self, minimum: float, maximum: float) -> float:
        return maximum


def test_create_default_state_builds_expected_number_of_squares() -> None:
    state = main.create_default_state(seed=7)
    assert len(state.squares) == main.SQUARE_COUNT
    assert main.SQUARE_COUNT == 100


def test_compute_square_max_speed_makes_bigger_squares_slower() -> None:
    small_square_speed = main.compute_square_max_speed(main.MIN_SIZE)
    big_square_speed = main.compute_square_max_speed(main.MAX_SIZE)

    assert small_square_speed > big_square_speed
    assert math.isclose(small_square_speed, main.MAX_SPEED, rel_tol=1e-9)
    assert math.isclose(big_square_speed, main.MIN_SPEED, rel_tol=1e-9)


def test_clamp_velocity_to_max_speed_limits_speed() -> None:
    square = main.Square(
        x=0,
        y=0,
        size=20,
        color=(255, 0, 0),
        vx=6.0,
        vy=8.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=5.0,
    )

    main.clamp_velocity_to_max_speed(square)

    assert math.isclose(math.hypot(square.vx, square.vy), 5.0, rel_tol=1e-6)


def test_apply_random_direction_jitter_changes_direction_without_breaking_speed_limit() -> None:
    square = main.Square(
        x=10,
        y=10,
        size=24,
        color=(255, 255, 0),
        vx=2.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=3.0,
    )

    before_speed = math.hypot(square.vx, square.vy)
    main.apply_random_direction_jitter(square, dt_seconds=1.0, rng=ForcedJitterRandom())
    after_speed = math.hypot(square.vx, square.vy)

    assert not math.isclose(square.vy, 0.0, abs_tol=1e-6)
    assert after_speed <= square.max_speed
    assert math.isclose(before_speed, after_speed, rel_tol=1e-6)


def test_update_square_bounces_when_it_hits_a_wall() -> None:
    square = main.Square(
        x=0,
        y=50,
        size=40,
        color=(255, 0, 0),
        vx=-2.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=3.0,
    )

    main.update_square(square, global_speed=1.0, dt_seconds=1 / main.FPS, rng=ForcedJitterRandom())

    assert square.x == 0
    assert square.vx > 0


def test_handle_input_can_pause_animation() -> None:
    state = main.create_default_state(seed=1)
    event = SimpleNamespace(type=main.pygame.KEYDOWN, key=main.pygame.K_SPACE)

    main.handle_input(state, [event])

    assert state.paused is True
