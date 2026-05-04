import pygame
import random
import math
from typing import List, Tuple


class Config:
    WIDTH: int = 800
    HEIGHT: int = 600

    NUM_BOIDS: int = 200
    BOID_SIZE: int = 5
    BOID_SPEED_MIN: int = 200  # Pixels per second
    BOID_SPEED_MAX: int = 300  # Pixels per second

    # TODO: Use the following parameters to implement the three main boid behaviors: separation, alignment, and cohesion
    # Use the *_DISTANCE parameters in the _separation, _alignment, and _cohesion methods to determine which nearby boids to consider for each behavior.
    # Use the *_STEER_STRENGTH parameters when applying the steering forces in the update() method.
    # You may have to adjust these parameters to get good results, but they should be a good starting point for tuning the behaviors.

    # Separation is the behavior where boids steer away from nearby boids to avoid crowding
    SEPARATION_ON: bool = False  # Toggle separation behavior on/off
    SEPARATION_DISTANCE: int = BOID_SIZE * 15  # Minimum distance to maintain from other boids
    SEPARATION_STEER_STRENGTH: float = 5 # How strongly boids steer away from neighbors (vector-based)

    # Alignment is the behavior where boids steer toward the average direction of nearby boids
    ALIGNMENT_ON: bool = False  # Toggle alignment behavior on/off
    ALIGNMENT_DISTANCE: int = BOID_SIZE * 100  # Distance within which to consider neighbors for alignment
    ALIGNMENT_STEER_STRENGTH: float = .8  # How strongly boids steer toward average direction of neighbors (vector-based)

    # Cohesion is the behavior where boids steer toward the average position of nearby boids
    COHESION_ON: bool = False  # Toggle cohesion behavior on/off
    COHESION_DISTANCE: int = BOID_SIZE * 50  # Distance within which to consider neighbors for cohesion
    COHESION_STEER_STRENGTH: float = 5  # How strongly boids steer toward center of mass of neighbors (vector-based)

    # Wall behavior
    WALL_BEHAVIOR: str = "wrap"

    RANDOM_STEER_ON: bool = True


TEST_MODE_ON: bool = False
SAC_TEST_FRAMES: int = 120
SAC_TEST_DT: int = 16



config = Config()

# Main Boid class representing each boid in the simulation
class Boid:
    def __init__(self) -> None:
        self.x: float = random.randint(0, config.WIDTH)
        self.y: float = random.randint(0, config.HEIGHT)
        self.speed: float = random.uniform(config.BOID_SPEED_MIN, config.BOID_SPEED_MAX)
        angle: float = random.uniform(0, 2 * math.pi)
        self.vx: float = self.speed * math.cos(angle)
        self.vy: float = self.speed * math.sin(angle)


    # TODO: Implement speed clamping to ensure boids don't exceed max speed
    def _clampSpeed(self) -> None:
        speed: float = math.hypot(self.vx, self.vy)

        if speed > config.BOID_SPEED_MAX:
            scale: float = config.BOID_SPEED_MAX / speed
            self.vx *= scale
            self.vy *= scale

    # TODO: Implement Screen Wrapping
    # Screen wrapping: if a boid goes off one edge of the screen, 
    # it should reappear on the opposite edge
    def _screen_wrap(self) -> None:
        if self.x > config.WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = config.WIDTH

        if self.y > config.HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = config.HEIGHT
    
    # Default wall behavior is bounce: if a boid hits the edge of the screen, 
    # it should bounce back in the opposite direction
    def _screen_bounce(self) -> None:
        if self.x < config.BOID_SIZE or self.x > config.WIDTH - config.BOID_SIZE:
            self.vx = -self.vx
            self.x = max(config.BOID_SIZE, min(self.x, config.WIDTH - config.BOID_SIZE))
        if self.y < config.BOID_SIZE or self.y > config.HEIGHT - config.BOID_SIZE:
            self.vy = -self.vy
            self.y = max(config.BOID_SIZE, min(self.y, config.HEIGHT - config.BOID_SIZE))

    # TODO: Implement Random Steering of the velocity vector to create more natural movement
    def _random_steer(self, spread: float = 0.2) -> None:
        speed: float = math.hypot(self.vx, self.vy)

        if speed == 0:
            return

        # Turn the velocity by a small random angle while keeping the same speed.
        current_angle: float = math.atan2(self.vy, self.vx)
        new_angle: float = current_angle + random.uniform(-spread, spread)
        self.vx = speed * math.cos(new_angle)
        self.vy = speed * math.sin(new_angle)


    # TODO: Implement the three main boid behaviors: separation, alignment, and cohesion

    # Separation: steer away from nearby boids to avoid crowding: 
    # _separation returns a vector pointing away from nearby boids
    # Explanation: For each nearby boid, calculate a vector pointing away from it, 
    # inversely proportional to the distance. 
    # Then sum these vectors to get the overall separation steering force.
    def _separation(self, boids: List['Boid']) -> pygame.Vector2:
        steer : pygame.Vector2 = pygame.Vector2(0, 0)

        for other in boids:
            if other is self:
                continue

            difference: pygame.Vector2 = pygame.Vector2(
                self.x - other.x,
                self.y - other.y,
            )
            distance: float = difference.length()

            if 0 < distance < config.SEPARATION_DISTANCE:
                steer += difference.normalize() / distance

        return steer

    # Alignment: steer toward the average direction of nearby boids: 
    # _alignment returns a vector pointing in the average direction of nearby boids
    # Explanation: For each nearby boid, get its velocity vector and sum them up. 
    # Then divide by the number of nearby boids to get the average velocity, 
    # and subtract the current boid's velocity to get the alignment steering force.
    def _alignment(self, boids: List['Boid']) -> pygame.Vector2:
        steer : pygame.Vector2 = pygame.Vector2(0, 0)

        nearby_count: int = 0

        for other in boids:
            if other is self:
                continue

            distance: float = math.hypot(self.x - other.x, self.y - other.y)

            if 0 < distance < config.ALIGNMENT_DISTANCE:
                steer += pygame.Vector2(other.vx, other.vy)
                nearby_count += 1

        if nearby_count > 0:
            average_velocity: pygame.Vector2 = steer / nearby_count
            steer = average_velocity - pygame.Vector2(self.vx, self.vy)

        return steer
    
    # Cohesion: steer toward the average position of nearby boids: 
    # _cohesion returns a vector pointing toward the average position of nearby boids
    # Explanation: For each nearby boid, get its position and sum them up. 
    # Then divide by the number of nearby boids to get the average position, 
    # and subtract the current boid's position to get the cohesion steering force.
    def _cohesion(self, boids: List['Boid']) -> pygame.Vector2:
        steer : pygame.Vector2 = pygame.Vector2(0, 0)

        nearby_count: int = 0

        for other in boids:
            if other is self:
                continue

            distance: float = math.hypot(self.x - other.x, self.y - other.y)

            if 0 < distance < config.COHESION_DISTANCE:
                steer += pygame.Vector2(other.x, other.y)
                nearby_count += 1

        if nearby_count > 0:
            group_center: pygame.Vector2 = steer / nearby_count
            steer = group_center - pygame.Vector2(self.x, self.y)

        return steer
        

    # TODO: Use _random_steer, _separation, _alignment and _cohesion in update()
    def update(self, boids: List['Boid'], dt: int) -> None:
        # dt is in milliseconds, convert to seconds for physics calculations, when applying steering forces
        # and the speed which are in pixels per second
        dt_seconds: float = dt / 1000.0

        # TODO: Use _random_steer, _separation, _alignment and _cohesion in update()
        # Explanation: 
        # Use the _separation, _alignment, and _cohesion methods to calculate the steering forces based on nearby boids.
        # Use the flags in the Config class to determine which behaviors are active 
        # and apply the corresponding steering forces to the boid's velocity 
        # using the defined strengths (*_STEER_STRENGTH) for each behavior.

        if config.RANDOM_STEER_ON:
            self._random_steer()

        if config.SEPARATION_ON:
            separation: pygame.Vector2 = self._separation(boids)
            self.vx += separation.x * config.SEPARATION_STEER_STRENGTH * dt_seconds
            self.vy += separation.y * config.SEPARATION_STEER_STRENGTH * dt_seconds

        if config.ALIGNMENT_ON:
            alignment: pygame.Vector2 = self._alignment(boids)
            self.vx += alignment.x * config.ALIGNMENT_STEER_STRENGTH * dt_seconds
            self.vy += alignment.y * config.ALIGNMENT_STEER_STRENGTH * dt_seconds

        if config.COHESION_ON:
            cohesion: pygame.Vector2 = self._cohesion(boids)
            self.vx += cohesion.x * config.COHESION_STEER_STRENGTH * dt_seconds
            self.vy += cohesion.y * config.COHESION_STEER_STRENGTH * dt_seconds

        self._clampSpeed()

        # Update the boid's position based on its velocity.
        self.x += self.vx * dt_seconds
        self.y += self.vy * dt_seconds

        # Last, wrap around the screen edges without changing velocity.
        self._screen_wrap()


    # Draw boid as a triangle pointing in the direction of velocity
    def draw(self, screen: pygame.Surface) -> None:
        arrow_spread_angle: float = 2.5  # Radians between the two back points of the triangle
        angle: float = math.atan2(self.vy, self.vx)
        points: List[Tuple[float, float]] = [
            (self.x + math.cos(angle) * config.BOID_SIZE, self.y + math.sin(angle) * config.BOID_SIZE),
            (self.x + math.cos(angle + arrow_spread_angle) * config.BOID_SIZE, self.y + math.sin(angle + arrow_spread_angle) * config.BOID_SIZE),
            (self.x + math.cos(angle - arrow_spread_angle) * config.BOID_SIZE, self.y + math.sin(angle - arrow_spread_angle) * config.BOID_SIZE),
        ]
        pygame.draw.polygon(screen, (255, 255, 255), points)

# Draw HUD (Heads Up Display) with FPS and behavior statuses
def draw_hud(screen: pygame.Surface, font: pygame.font.Font, config: Config, fps: float) -> None:
    # Draw separation status and alignment and FPS on the screen
    text: str = f"FPS: {fps:.2f}   (Press 'ESC' or 'Q' to quit)"
    img: pygame.Surface = font.render(text, True, (255, 255, 255))
    screen.blit(img, (10, 10))
    text: str = f"Separation: {'ON' if config.SEPARATION_ON else 'OFF'} - Press 'S' to toggle"
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (10, 25))
    text: str = f"Alignment: {'ON' if config.ALIGNMENT_ON else 'OFF'} - Press 'A' to toggle"
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (10, 40))
    text: str = f"Cohesion: {'ON' if config.COHESION_ON else 'OFF'} - Press 'C' to toggle"
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (10, 55))
    text: str = f"Wall Behavior: {config.WALL_BEHAVIOR.capitalize()}"
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (10, 70))


def average_minimum_distance(boids: List[Boid]) -> float:
    minimum_distances: List[float] = []

    for boid in boids:
        closest_distance: float | None = None

        for other in boids:
            if other is boid:
                continue

            distance: float = math.hypot(boid.x - other.x, boid.y - other.y)

            if closest_distance is None or distance < closest_distance:
                closest_distance = distance

        if closest_distance is not None:
            minimum_distances.append(closest_distance)

    if not minimum_distances:
        return 0.0

    return sum(minimum_distances) / len(minimum_distances)


def average_angle_difference(boids: List[Boid]) -> float:
    angle_differences: List[float] = []

    for first_index in range(len(boids)):
        first_angle: float = math.atan2(boids[first_index].vy, boids[first_index].vx)

        for second_index in range(first_index + 1, len(boids)):
            second_angle: float = math.atan2(boids[second_index].vy, boids[second_index].vx)
            difference: float = abs(first_angle - second_angle)

            if difference > math.pi:
                difference = 2 * math.pi - difference

            angle_differences.append(difference)

    if not angle_differences:
        return 0.0

    return sum(angle_differences) / len(angle_differences)


def average_distance_to_group_center(boids: List[Boid]) -> float:
    if not boids:
        return 0.0

    center_x: float = sum(boid.x for boid in boids) / len(boids)
    center_y: float = sum(boid.y for boid in boids) / len(boids)
    distances: List[float] = []

    for boid in boids:
        distances.append(math.hypot(boid.x - center_x, boid.y - center_y))

    return sum(distances) / len(distances)


def measure_sac(boids: List[Boid]) -> Tuple[float, float, float]:
    return (
        average_minimum_distance(boids),
        average_angle_difference(boids),
        average_distance_to_group_center(boids),
    )


def create_sac_test_boids() -> List[Boid]:
    test_data: List[Tuple[float, float, float, float]] = [
        (300, 300, 220, 0),
        (500, 300, -220, 0),
        (400, 220, 0, 220),
        (400, 380, 0, -220),
        (420, 310, 220, 0),
    ]
    boids: List[Boid] = []

    for x, y, vx, vy in test_data:
        boid = Boid()
        boid.x = x
        boid.y = y
        boid.vx = vx
        boid.vy = vy
        boids.append(boid)

    return boids


def run_sac_test() -> bool:
    old_separation: bool = config.SEPARATION_ON
    old_alignment: bool = config.ALIGNMENT_ON
    old_cohesion: bool = config.COHESION_ON
    old_random_steer: bool = config.RANDOM_STEER_ON

    config.SEPARATION_ON = True
    config.ALIGNMENT_ON = True
    config.COHESION_ON = True
    config.RANDOM_STEER_ON = False

    boids: List[Boid] = create_sac_test_boids()
    before_separation, before_alignment, before_cohesion = measure_sac(boids)

    for _ in range(SAC_TEST_FRAMES):
        for boid in boids:
            boid.update(boids, SAC_TEST_DT)

    after_separation, after_alignment, after_cohesion = measure_sac(boids)

    config.SEPARATION_ON = old_separation
    config.ALIGNMENT_ON = old_alignment
    config.COHESION_ON = old_cohesion
    config.RANDOM_STEER_ON = old_random_steer

    separation_passed: bool = after_separation >= config.BOID_SIZE * 2
    alignment_passed: bool = after_alignment < before_alignment
    cohesion_passed: bool = after_cohesion <= before_cohesion * 1.5
    test_passed: bool = separation_passed and alignment_passed and cohesion_passed

    print("S.A.C. measurements:")
    print(f"Separation average minimum distance: {before_separation:.2f} -> {after_separation:.2f}")
    print(
        "Alignment average angle difference: "
        f"{math.degrees(before_alignment):.2f} deg -> {math.degrees(after_alignment):.2f} deg"
    )
    print(f"Cohesion average distance to center: {before_cohesion:.2f} -> {after_cohesion:.2f}")

    if test_passed:
        print("SAC TEST PASS")
    else:
        print("SAC TEST FAIL")

    return test_passed


# Main function to run the simulation
def run_simulation() -> None:

    # Initialize Pygame and create screen, clock, and font
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
    clock: pygame.time.Clock = pygame.time.Clock()
    font: pygame.font.Font = pygame.font.SysFont(None, 18)

    # Create boids
    boids: List[Boid] = [Boid() for _ in range(Config.NUM_BOIDS)]
    
    # Main loop
    running: bool = True
    while running:
        dt: int = clock.tick(60)  # Elapsed time in milliseconds since last frame
        fps: float = clock.get_fps() # Current frames per second

        # Screen clearing
        screen.fill((0, 0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_s:
                    config.SEPARATION_ON = not config.SEPARATION_ON
                if event.key == pygame.K_a:
                    config.ALIGNMENT_ON = not config.ALIGNMENT_ON
                if event.key == pygame.K_c:
                    config.COHESION_ON = not config.COHESION_ON

        # Update and draw boids in one loop
        for boid in boids:
            boid.update(boids, dt)
            boid.draw(screen)

        # Draw HUD (Heads Up Display) with FPS and behavior statuses
        draw_hud(screen, font, config, fps)
        pygame.display.flip()

    pygame.quit()

# Main entry point to run the simulation
if __name__ == "__main__":
    if TEST_MODE_ON:
        run_sac_test()
    else:
        run_simulation()
