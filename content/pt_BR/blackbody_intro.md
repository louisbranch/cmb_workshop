## Compreendendo a Luz Cósmica

### Radiação de Corpo Negro

A radiação de corpo negro descreve a luz emitida por um objeto que absorve toda a luz que incide sobre ele. Esse objeto ideal, chamado de "corpo negro," emite luz em todos os comprimentos de onda. A quantidade de luz emitida depende apenas de sua temperatura. Esse conceito nos ajuda a entender as estrelas e o Fundo Cósmico de Micro-ondas (CMB).

A Lei de Planck descreve a quantidade de luz que um corpo negro emite em diferentes comprimentos de onda. A fórmula é:

$B(\lambda, T) = \frac{2hc^2}{\lambda^5} \frac{1}{\exp\left(\frac{hc}{\lambda kT}\right) - 1}$

onde:

* $B(\lambda, T)$ é a radiância espectral, medida em $W/m^{3}$,
* $h$ é a constante de Planck ($6.626 \times 10^{-34}$ J s),
* $c$ é a velocidade da luz no vácuo ($3.00 \times 10^8$ m/s),
* $k$ é a constante de Boltzmann ($1.381 \times 10^{-23}$ J/K),
* $T$ é a temperatura absoluta do corpo negro em Kelvin (K),
* $\lambda$ é o comprimento de onda em metros (m).

**Compreendendo Funções Exponenciais:**

Uma função exponencial, como $\exp(x)$, representa um crescimento rápido, onde o valor da função aumenta exponencialmente à medida que x aumenta. Na Lei de Planck, o termo exponencial ajusta a quantidade de luz emitida em diferentes comprimentos de onda com base na temperatura.


### Desafio de Código: Implemente sua própria versão da Lei de Planck:

Tente implementar a Lei de Planck em Python para ver quanta luz é emitida em diferentes comprimentos de onda e temperaturas.