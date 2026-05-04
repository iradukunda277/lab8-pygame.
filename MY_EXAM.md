# MY_EXAM

## Q7 - Trails
I added trails by saving the last positions of each square and drawing lines between them.
The main issue was a long line after screen wrapping, so I reset the trail when a square crosses the edge.

## Q8 - Speed test
I tested speed with one square starting from a known position and moving with a known velocity.
The test checks if the final position matches the expected movement after a fixed time.

## Q15 - S.A.C. test analysis
For S.A.C., I would check separation, alignment, and cohesion with simple measurements.
The idea is to see if boids avoid being too close, move in similar directions, and stay near the group.

## Q16 - S.A.C. test implementation
I implemented a simple test mode that runs boids without drawing and measures flocking behavior.
It prints PASS or FAIL based on basic separation, alignment, and cohesion checks.
