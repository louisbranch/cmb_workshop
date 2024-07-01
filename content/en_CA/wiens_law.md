### Peak Wavelength and Wien's Law

After exploring the blackbody radiation curves, you've seen how the peak of the radiation curve shifts with changes in temperature. This movement isn't random; it's described by Wien's Displacement Law. Wien's Law tells us the wavelength at which the radiation from a blackbody (like a star, including our Sun) is most intense. This wavelength is inversely related to the temperature of the body, meaning that as the temperature increases, the peak wavelength decreases.

Wien's Law can be stated mathematically as:

$\lambda_{\text{max}} = \frac{b}{T}$

where:
- $\lambda_{\text{max}}$ is the peak wavelength (in meters, m) — the wavelength at which the emission is strongest,
- $T$ is the absolute temperature of the blackbody (in Kelvin),
- $b$ is Wien's displacement constant, approximately $2.897 \times 10^{-3}$ m·K (meter-Kelvin).

This law reveals an important insight: as a blackbody gets hotter, its peak emission shifts to shorter wavelengths. For example, a heating metal glows red and then white as its temperature increases, meaning it emits light at shorter and shorter wavelengths.

#### Practical Implication

In astronomy, Wien's Law enables us to determine the surface temperature of stars by observing the colour of the light they emit. The colour of a star is directly related to its wavelength. A star emitting peak radiation at shorter wavelengths (more towards the blue end of the spectrum) is hotter than a star emitting peak radiation at longer wavelengths (more towards the red end of the spectrum). For reference, visible light wavelengths range from about 400 nm (nanometers) for violet light to 700 nm for red light, where 1 nm = $1 \times 10^{-9}$ meters.

### Coding Challenge: Implementing Wien's Law

Let’s implement Wien's Law to calculate the peak wavelength for a given temperature.