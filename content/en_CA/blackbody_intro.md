## Understanding Cosmic Light

### Blackbody Radiation

Blackbody radiation describes the light emitted by an object that absorbs all light falling on it. This ideal object, called a "black body," emits light across all wavelengths. The amount of light emitted depends only on its temperature. This concept helps us understand stars and the Cosmic Microwave Background (CMB).

Planck's Law describes how much light a blackbody emits at different wavelengths. The formula is:

$B(\lambda, T) = \frac{2hc^2}{\lambda^5} \frac{1}{\exp\left(\frac{hc}{\lambda kT}\right) - 1}$

where:

* $B(\lambda, T)$ is the spectral radiance, measured in $W/m^{3}$,
* $h$ is the Planck constant ($6.626 \times 10^{-34}$ J s),
* $c$ is the speed of light in a vacuum ($3.00 \times 10^8$ m/s),
* $k$ is the Boltzmann constant ($1.381 \times 10^{-23}$ J/K),
* $T$ is the absolute temperature of the blackbody in Kelvin (K),
* $\lambda$ is the wavelength in meters (m).

**Understanding Exponential Functions:**

An exponential function, like $\exp(x)$, represents rapid growth where the value of the function increases exponentially as xx increases. In Planck's Law, the exponential term adjusts the amount of light emitted at different wavelengths based on temperature.


### Coding Challenge: Write your own implementation of Planck's Law:

Try implementing Planck's Law in Python to see how much light is emitted at different wavelengths and temperatures.