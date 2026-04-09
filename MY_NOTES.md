# MY_NOTES

## Core Structure

- The program uses a `Square` dataclass to store each square's position, size,
  color, velocity, angle, rotation speed, and max speed.
- The `GameState` dataclass stores the list of squares plus global animation
  settings such as pause state and global speed.
- The main loop follows the usual PyGame order:
  - handle input
  - update state
  - draw frame

## Size-Based Max Speed

- I added a `max_speed` attribute to every square.
- `compute_square_max_speed(size)` makes smaller squares faster and bigger
  squares slower.
- I used a linear mapping from `MIN_SIZE..MAX_SIZE` to `MAX_SPEED..MIN_SPEED`.

## Jitter

- Jitter slightly rotates the square's velocity vector over time.
- The idea is to change direction a little without changing the speed
  magnitude.
- I still keep a safety clamp so the velocity never exceeds the square's
  `max_speed`.

## Current Controls

- `SPACE` pauses and resumes the animation
- `1` slows the global animation speed
- `2` speeds the global animation speed up
- `R` regenerates the set of squares
- `Q` or `ESC` quits

## Things I Should Still Be Ready To Explain

- Why the square count is now 100
- Why bigger squares should move more slowly
- Why jitter rotates the velocity vector instead of replacing it randomly
- Why `main()` is the entry point and how the game loop works
