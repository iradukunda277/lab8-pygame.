import math
from collections import Counter
from types import SimpleNamespace

import main


class ForcedJitterRandom:
    def random(self) -> float:
        return 0.0

    def uniform(self, minimum: float, maximum: float) -> float:
        return maximum


class NoJitterRandom:
    def uniform(self, minimum: float, maximum: float) -> float:
        return 0.0


def test_create_default_state_builds_expected_number_of_squares() -> None:
    state = main.create_default_state(seed=7)
    size_counts = Counter(square.size for square in state.squares)

    assert len(state.squares) == main.SQUARE_COUNT
    assert main.SQUARE_COUNT == 45
    assert size_counts[25] == 5
    assert size_counts[10] == 10
    assert size_counts[4] == 30


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


def test_check_collision_uses_updated_rects() -> None:
    first_square = main.Square(
        x=10,
        y=10,
        size=10,
        color=(255, 0, 0),
        vx=0.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=3.0,
    )
    second_square = main.Square(
        x=18,
        y=18,
        size=10,
        color=(0, 255, 0),
        vx=0.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=3.0,
    )

    assert main.check_collision(first_square, second_square) is True

    second_square.x = 50
    second_square.y = 50
    assert main.check_collision(first_square, second_square) is False

    first_square.size = 45
    assert main.check_collision(first_square, second_square) is True


def test_bigger_square_eats_smaller_square_on_collision() -> None:
    bigger_square = main.Square(
        x=10,
        y=10,
        size=25,
        color=(255, 0, 0),
        vx=0.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=3.0,
    )
    smaller_square = main.Square(
        x=20,
        y=20,
        size=4,
        color=(0, 255, 0),
        vx=0.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=3.0,
        original_size=10,
    )
    state = main.GameState(
        squares=[bigger_square, smaller_square],
        rng=main.random.Random(3),
    )

    main.handle_collisions(state)

    assert state.squares[0] is bigger_square
    assert state.squares[0].size == 26
    assert state.squares[0].original_size == 25
    assert state.squares[0].rect.size == (26, 26)
    assert state.squares[1] is not smaller_square
    assert state.squares[1].size == 10
    assert state.squares[1].original_size == 10


def test_predator_growth_is_limited_by_max_size() -> None:
    predator = main.Square(
        x=10,
        y=10,
        size=79,
        color=(255, 0, 0),
        vx=0.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=3.0,
        original_size=25,
    )
    prey = main.Square(
        x=20,
        y=20,
        size=25,
        color=(0, 255, 0),
        vx=0.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=3.0,
    )
    state = main.GameState(
        squares=[predator, prey],
        rng=main.random.Random(5),
    )

    main.handle_collisions(state)

    assert state.squares[0].size == main.MAX_SQUARE_SIZE
    assert state.squares[0].rect.size == (
        main.MAX_SQUARE_SIZE,
        main.MAX_SQUARE_SIZE,
    )
    assert state.squares[0].original_size == 25


def test_same_size_squares_do_not_eat_each_other() -> None:
    first_square = main.Square(
        x=10,
        y=10,
        size=10,
        color=(255, 0, 0),
        vx=0.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=3.0,
    )
    second_square = main.Square(
        x=15,
        y=15,
        size=10,
        color=(0, 255, 0),
        vx=0.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=3.0,
    )
    state = main.GameState(
        squares=[first_square, second_square],
        rng=main.random.Random(4),
    )

    main.handle_collisions(state)

    assert state.squares[0] is first_square
    assert state.squares[1] is second_square


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


def test_update_square_wraps_at_edges_without_changing_velocity() -> None:
    test_cases = [
        (main.WIDTH - 2, 50, 3.0, 1.0, 0, 51),
        (1, 50, -3.0, 1.0, main.WIDTH - 4, 51),
        (50, main.HEIGHT - 2, 1.0, 3.0, 51, 0),
        (50, 1, 1.0, -3.0, 51, main.HEIGHT - 4),
    ]

    for x, y, vx, vy, expected_x, expected_y in test_cases:
        square = main.Square(
            x=x,
            y=y,
            size=4,
            color=(255, 0, 0),
            vx=vx,
            vy=vy,
            angle=0.0,
            rotation_speed=1.0,
            max_speed=10.0,
        )
        square.trail = [(10, 10), (20, 20)]

        main.update_square(
            square,
            [square],
            global_speed=1.0,
            dt_seconds=1 / main.FPS,
            rng=NoJitterRandom(),
        )

        assert math.isclose(square.x, expected_x, abs_tol=1e-6)
        assert math.isclose(square.y, expected_y, abs_tol=1e-6)
        assert math.isclose(square.vx, vx, abs_tol=1e-6)
        assert math.isclose(square.vy, vy, abs_tol=1e-6)
        assert square.rect.topleft == (int(expected_x), int(expected_y))
        assert square.rect.size == (square.size, square.size)
        assert square.trail == []


def test_square_trail_keeps_last_positions() -> None:
    square = main.Square(
        x=100,
        y=100,
        size=4,
        color=(255, 0, 0),
        vx=1.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=10.0,
    )

    for _ in range(main.TRAILS_LENGTH + 5):
        main.update_square(
            square,
            [square],
            global_speed=1.0,
            dt_seconds=1 / main.FPS,
            rng=NoJitterRandom(),
        )

    assert len(square.trail) == main.TRAILS_LENGTH
    assert math.isclose(square.trail[-1][0], square.center_x(), abs_tol=1e-6)
    assert math.isclose(square.trail[-1][1], square.center_y(), abs_tol=1e-6)


def test_apply_flee_behavior_turns_small_square_away_from_bigger_one() -> None:
    small_square = main.Square(
        x=100,
        y=100,
        size=20,
        color=(255, 0, 0),
        vx=1.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=3.0,
    )
    big_square = main.Square(
        x=140,
        y=100,
        size=60,
        color=(0, 255, 0),
        vx=0.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=1.0,
    )

    main.apply_flee_behavior(small_square, [small_square, big_square], dt_seconds=1.0)

    assert small_square.vx < 0
    assert math.hypot(small_square.vx, small_square.vy) <= small_square.max_speed


def test_handle_input_can_pause_animation() -> None:
    state = main.create_default_state(seed=1)
    event = SimpleNamespace(type=main.pygame.KEYDOWN, key=main.pygame.K_SPACE)

    main.handle_input(state, [event])

    assert state.paused is True


def test_respawn_uses_original_size() -> None:
    square = main.Square(
        x=20,
        y=20,
        size=4,
        color=(255, 0, 0),
        vx=1.0,
        vy=0.0,
        angle=0.0,
        rotation_speed=1.0,
        max_speed=3.0,
        life_span=1.0,
        age=2.0,
        original_size=25,
    )
    state = main.GameState(squares=[square], rng=main.random.Random(2))

    main.update_state(state, dt_seconds=0.0)

    assert state.squares[0].size == 25
    assert state.squares[0].original_size == 25
