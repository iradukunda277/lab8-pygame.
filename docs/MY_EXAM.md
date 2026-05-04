## Q7 Trails analysis

When trails were added, visual artifacts can happen because the square wraps from one side of the screen to the other side. The trail may draw one long line between the old edge position and the new opposite-side position. To fix this, the code resets the trail when wrapping happens, or avoids drawing a trail segment when the distance between two points is too large.

## Q8 Speed test analysis

To test speed, I create a square with a known starting position and a known velocity. For example, if the square starts at x = 100 and moves at 50 pixels per second for one second, I expect the final x position to be 150. The test should disable randomness and avoid wall wrapping so that only the movement formula is tested. The code can print PASS if the actual position is close to the expected position, otherwise FAIL.
