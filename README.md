# lab8-pygame

## What this project does

This project shows 20 colorful squares moving around a black window. Each
square has its own size, color, movement speed, direction, rotation speed, and
size-based maximum speed. Bigger squares move more slowly than smaller ones.

The app also applies a small random direction jitter over time, so the movement
feels more alive instead of perfectly straight forever. In Part B, smaller
squares also try to flee away from bigger nearby squares.

## Installation

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## How to run

```powershell
python main.py
```

## How to test

```powershell
pytest
```

## Controls

- `SPACE`: pause or resume the animation
- `1`: slow all squares down
- `2`: speed all squares up
- `R`: generate a new set of random squares
- `Q` or `ESC`: quit

## Features

- 20 moving squares
- Random sizes and colors
- Rotation for every square
- Size-based max speed
- Random direction jitter
- Flee behavior for smaller squares
- Bounce behavior on window edges
- Pause, reset, and speed controls
