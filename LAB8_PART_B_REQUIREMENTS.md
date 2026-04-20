# Lab 8 Part B Requirements

Source analyzed:
- `C:\Users\sjean\Downloads\epita course\AI for software dvelopement\OneDrive_2_4-10-2026.zip`
- `AI For Software Development_Labs - 9 - 0 - PyGame - Moving Squares - Part II.pdf`
- `AI For Software Development_Course - 9 - 0 - Agenda - Lab 8 Pygame Part II - Share.pdf`

## What Part B asks you to do

These are the real task and requirement signals from the Part II lab PDF.

### Core feature for Part B

- Add a **flee behavior**:
  - **smaller squares should flee away from bigger squares**
  - the movement should still keep **some randomness**

### Preparation before adding the new feature

- **Reduce the total number of squares to 20**
  - this is specifically recommended to make the behavior easier to see and debug

- If not already done:
  - make **smaller squares move faster than bigger ones**

### Technical guidance from the PDF

- Use **time-based animation**
  - update with `x += vx * delta_time`
  - update with `y += vy * delta_time`
  - do not rely only on frame-based movement

- You may use `clock.tick(FPS)` to compute `delta_time`

- A small FPS HUD is suggested, for example:
  - show the current FPS on screen

### Process / workflow expectations

- Go as far as possible **without AI**
- If you use AI:
  - prefer **Ask** and **Socratic** approaches
  - ask for progressive help, not full solutions
- Use **stubs and TODOs**
- Do regular **git rituals**
- Keep your **README** updated
- Think through the behavior first
  - strategies
  - generic cases
  - edge cases
  - vectors
  - lists
  - distances

### Notes / documentation expectations

- Write your thinking and analysis in `MY_NOTES.md`
- `JOURNAL.md` should exist and be working
- `prompt_history.md` should also exist
- The latest `.github` folder from `lab1-hello-world` is still expected

### Commit / submission reminder

- Suggested commit message for the new feature:
  - `feat: Chasing / Fleeing behavior`

- Send the repo link to Denis again at the end of class

## What your current project already satisfies

- `.github` folder exists
- `JOURNAL.md` exists
- `MY_NOTES.md` exists
- `README.md` exists
- Time-based animation already exists in `main.py`
- Smaller squares already move faster than bigger ones via size-based `max_speed`
- Jitter / random directional change already exists

## What is still missing for Part B

- Change the square count from `100` to `20` while working on Part B
- Implement the **flee behavior**
- Make sure the flee behavior still leaves a bit of randomness
- Add `prompt_history.md` if the logger is supposed to generate it and it is missing
- Optionally add an FPS HUD, since the PDF suggests it

## Practical implementation checklist

1. Change `SQUARE_COUNT` to `20`
2. Keep time-based movement
3. For each small square, find nearby bigger squares
4. Compute a direction away from the bigger square(s)
5. Blend that flee direction with the current random movement
6. Keep the final speed under the square's `max_speed`
7. Test edge cases:
   - no bigger square nearby
   - multiple bigger squares nearby
   - overlapping squares
   - behavior near screen borders
8. Update `MY_NOTES.md`
9. Update `README.md`
10. Commit with `feat: Chasing / Fleeing behavior`

## Important note

The Part II PDF is not asking you to start over from scratch.
It expects you to build on the Part I work you already have:
- moving squares
- size-based max speed
- jitter
- documentation
- git history

The main new lab feature is the **flee behavior**.
