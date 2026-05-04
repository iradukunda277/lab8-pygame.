# lab8-pygame

## What this project does
This project contains two Pygame simulations: moving squares in `main.py` and boids flocking in `boids_exam.py`.

## How to run
```powershell
python main.py
python boids_exam.py
```

## How to test
```powershell
python -m py_compile main.py boids_exam.py
pytest
```

## Main features
- 45 starting squares with different sizes
- Screen wrapping
- Collision detection
- Eating and animated growth
- Trails
- Simple speed test
- Boids wrapping, random steering, separation, alignment, and cohesion
