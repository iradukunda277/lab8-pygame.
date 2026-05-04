## Q7 Trails analysis

When trails were added, visual artifacts can happen because the square wraps from one side of the screen to the other side. The trail may draw one long line between the old edge position and the new opposite-side position. To fix this, the code resets the trail when wrapping happens, or avoids drawing a trail segment when the distance between two points is too large.
