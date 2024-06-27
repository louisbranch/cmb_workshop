## Understanding Cosmic Light

### Blackbody Radiation

Blackbody radiation describes the light emitted by an object that absorbs all light falling on it. This ideal object, called a "black body," re-emits light in a pattern that depends only on its temperature. Understanding blackbody radiation helps us learn about stars and the Cosmic Microwave Background (CMB).

Planck's Law describes how much light a blackbody emits at different wavelengths. The formula is:

$B(\lambda, T) = \frac{2hc^2}{\lambda^5} \frac{1}{\exp\left(\frac{hc}{\lambda kT}\right) - 1}$

with the spectral radiance $B(\lambda, T)$ given in units of $W \cdot m^{-2} \cdot sr^{-1} \cdot m^{-1}$. Here:
* $h$ is the Planck constant ($6.626 \times 10^{-34}$ J s)
* $c$ is the speed of light in a vacuum ($3.00 \times 10^8$ m/s)
* $k$ is the Boltzmann constant ($1.381 \times 10^{-23}$ J/K)
* $T$ is the absolute temperature of the blackbody in Kelvin (K)
* $\lambda$ is the wavelength in meters (m).

##### Optional Challenge: Write your own implementation of Planck's Law:

Try implementing Planck's Law in Python to see how much light is emitted at different wavelengths and temperatures.