### Estimate the Distance of the Moon

To estimate the age of the universe using the CMB map, we can employ a methodology similar to determining the distance of the moon. Let's walk through how to do that now.

Let's suppose that we already know the physical size (diameter) of the moon to be 3,474 km, and we can easily measure the angular size (diameter) of the moon on the sky to be 0.52 degrees. How do we estimate the distance to the moon? Recall the formula for an arc-length:

![arclengh](media/arclength.png)

Therefore, we have
$$\text{distance to the moon} = \frac{\text{physical diameter of the moon}}{\text{angular size subtended by the moon}}$$

**Important**: To use this formula correctly, we need to convert the angular size from degrees to radians. You can use the formula below or `np.deg2rad` function.

$$\text{angular size (radians)} = \text{angular size (degrees)} \times \frac{\pi}{180}$$

Work out the distance to the moon, and then use this distance to calculate how many seconds it takes light to reach the moon from the Earth.