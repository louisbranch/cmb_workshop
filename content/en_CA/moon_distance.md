### Estimate the Distance of the Moon

To estimate the age of the universe using the CMB map, we can employ a methodology similar to determining the distance of the moon. Let's walk through how to do that now.

Imagine we already know the physical size (diameter) of the moon is 3,474 km. We can easily measure the angular size (how big the moon looks in the sky) to be 0.52 degrees. 

#### What is Angular Size?

Angular size is how large an object appears to be from a particular point of view. It's like holding a coin at arm's length and seeing how big it looks compared to when you hold it closer to your face.

#### Understanding Arc Length

Arc length is the distance along the curved path of a circle. Think of it like the length of a piece of string wrapped around part of a circle.

#### Estimating the Distance

To estimate the distance to the moon, we use the formula for arc length:

$$\text{distance to the moon} = \frac{\text{physical diameter of the moon}}{\text{angular size subtended by the moon}}$$

Here's a sketch to visualize angular size and arc length:

<figure>
<img src="media/arclength.png" alt="Sketch of angular size and arc length" />
<figcaption>Angular size and arc length</figcaption>
</figure>

**Important**: To use this formula correctly, we need to convert the angular size from degrees to radians. Radians are just another way to measure angles, and you can convert degrees to radians by multiplying by a conversion factor:

$$\text{angular size (radians)} = \text{angular size (degrees)} \times \frac{\pi}{180}$$

You can also use the `np.deg2rad` function in Python for this conversion.

#### Exercise

1. **Calculate the Distance to the Moon**:
   - Convert the angular size from degrees to radians.
   - Use the formula to calculate the distance to the moon.

2. **Calculate the Time for Light to Reach the Moon**:
   - Use the distance you calculated and the speed of light to find out how many seconds it takes for light to travel from the Earth to the moon.

By working through these steps, you will better understand how we can use angular size and physical size to calculate distances in space. This method will help us later when we estimate the age of the universe using the CMB.