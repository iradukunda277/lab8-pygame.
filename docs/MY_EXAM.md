## Q7 Trails analysis

When trails were added, visual artifacts can happen because the square wraps from one side of the screen to the other side. The trail may draw one long line between the old edge position and the new opposite-side position. To fix this, the code resets the trail when wrapping happens, or avoids drawing a trail segment when the distance between two points is too large.

## Q8 Speed test analysis

To test speed, I create a square with a known starting position and a known velocity. For example, if the square starts at x = 100 and moves at 50 pixels per second for one second, I expect the final x position to be 150. The test should disable randomness and avoid wall wrapping so that only the movement formula is tested. The code can print PASS if the actual position is close to the expected position, otherwise FAIL.

## Q15 S.A.C. test analysis

S.A.C. means separation, alignment, and cohesion. To test that boids are flocking, I would run the simulation in a test mode for a few seconds and compare measurements from the start and the end.

For separation, boids should not be too close together. I would measure the minimum distance from each boid to its nearest neighbor, then calculate the average minimum distance. If separation is working, this value should stay reasonable or increase because boids are avoiding crowding.

For alignment, boids should move in similar directions. I would compare each boid's velocity angle with nearby boids' velocity angles, then calculate the average angle difference. If alignment is working, the average angle difference should get smaller because boids are turning toward the same direction.

For cohesion, boids should remain grouped. I would calculate the group center by averaging all boid positions, then measure each boid's distance from that center. If cohesion is working, the average distance from the center should stay reasonable or decrease because boids are moving toward the group.

The test idea is to create a fixed set of boids, turn on separation, alignment, and cohesion, and run the update loop for a few seconds without drawing. The code would collect the separation, alignment, and cohesion measurements before and after the simulation. It would print PASS if the final values show better flocking behavior, otherwise it would print FAIL.
