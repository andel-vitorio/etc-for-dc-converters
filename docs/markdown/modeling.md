# Modelagem Matemática de uma Microrrede

## Introdução

Neste guia, abordaremos a modelagem matemática de uma microrrede representada por um conversor buck com uma CPL, carga de potência constante. O conversor buck é um tipo de conversor de potência que converte tensão contínua de alta tensão para tensão contínua de baixa tensão. A CPL é um tipo de carga que requer uma potência constante, independentemente da tensão de entrada.

## Passo 1: Descrição do Sistema e Circuito

Abaixo está o circuito simplificado representando o sistema:

![Circuito Elétrico do Sistema](images/buck_conversor_with_cpl_circuit.png)

No circuito:

- $R_L, R_C, C, L$: Resistores, capacitor e indutor do circuito.
- $V_{in}$: Tensão de entrada.
- $V_{out}$: Tensão de entrada.

## Passo 2: Formulação das Equações do Circuito

As equações que descrevem o comportamento do sistema podem ser derivadas usando as leis fundamentais da eletricidade. Para isso, consideraremos o circuito em duas situações: chave fechada e aberta.

### Chave Fechada

Na situação em que a chave está fechada, o circuito é equivalente a um circuito série com uma fonte de tensão, um resistor e uma indutância.

![Circuito Elétrico do Sistema](images/buck_conversor_with_cpl_circuit_m1.png)

As equações que descrevem esse circuito são as seguintes:

1. Lei de Kirchhoff das Tensões

$$ V_{in} - L \frac{d}{dt}i_L - R_L i_L - v_C = 0 $$
$$ L \frac{d}{dt}i_L = V_{in} - R_L i_L - v_C $$

$$ \frac{d}{dt}i_L =  \frac{1}{L} V_{in}  - \frac{R_L}{L} i_L - \frac{1}{L} v_C $$

2. Lei de Kirchhoff das Correntes

$$ i_L = i_C + I_{CPL} + I_{R_{C}} $$
$$ i_L = C \frac{d}{dt} v_C + \frac{P_{CPL}}{v_C} + \frac{v_C}{R_C} $$
$$ C \frac{d}{dt} v_C = i_L - \frac{v_C}{R_C} - \frac{P_{CPL}}{v_C} $$

$$ \frac{d}{dt} v_C = \frac{1}{C} i_L - \frac{1}{C R_C} v_C - \frac{1}{C v_C} P_{CPL} $$

### Chave Aberta

Na situação em que a chave está aberta, o circuito é desconectado da fonte de tensão.

![Circuito Elétrico do Sistema](images/buck_conversor_with_cpl_circuit_m2.png)

As equações que descrevem esse circuito são as seguintes:

1. Lei de Kirchhoff das Tensões

$$ L \frac{d}{dt}i_L + R_L i_L + v_C = 0 $$

$$
\frac{d}{dt}i_L = - \frac{R_L}{L} i_L - \frac{1}{L} v_C \\
$$

2. Lei de Kirchhoff das Correntes

$$ i_L = i_C + I_{CPL} + I_{R_{C}} $$
$$ i_L = C \frac{d}{dt} v_C + \frac{P_{CPL}}{v_C} + \frac{v_C}{R_C} $$
$$ C \frac{d}{dt} v_C = i_L - \frac{v_C}{R_C} - \frac{P_{CPL}}{v_C} $$

$$ \frac{d}{dt} v_C = \frac{1}{C} i_L - \frac{1}{C R_C} v_C - \frac{1}{C v_C} P_{CPL} $$

### Modelo Médio do Sistema

O modelo médio do sistema é:

\begin{equation}
\begin{cases}
\frac{d}{dt}i_L &= \frac{V_{in}}{L} d - \frac{R_L}{L} i_L - \frac{1}{L} v_C \\ \\
\frac{d}{dt} v_C &= \frac{1}{C} i_L - \frac{1}{C R_C} v_C - \frac{1}{C v_C} P_{CPL}
\end{cases}
\end{equation}

## Passo 3: Modelo do Sistema em Torno do PE

Temos que

1. $P_E = \left( \overline{i_L}, \, \overline{V_C}, \, \overline{d}, \, \overline{P_{CPL}} \right)$

2.
$$
\begin{cases}
  i_L &= \overline{i_L} + \delta i_L \\
  v_C &= \overline{V_C} + \delta V_C \\
  d &= \overline{d} + \delta d \\
  P_{CPL} &= \overline{P_{CPL}} + \delta P_{CPL} \\
\end{cases}
$$
 
3.
$$
\begin{cases}
  \dot{i_L} &= \overline{\dot{i_L}} + \delta \dot{i_L} \\
  \dot{v_C} &= \overline{\dot{v_C}} + \delta \dot{v_C} \\
\end{cases}
$$

Além disto, 

$$ f(i_L, \, v_C, \, d, \, P_{CPL}) = \dot{i_L} = - \frac{R_L}{L} i_L - \frac{1}{L} v_C + \frac{V_{in}}{L} d $$
$$ g(i_L, \, v_C, \, d, \, P_{CPL}) = \dot{v_C}= - \frac{1}{C R_C} v_C + \frac{1}{C} i_L - \frac{1}{C v_C} P_{CPL} $$

$$ f(P_E) = g(P_E) = \overline{\dot{i_L}} = \overline{\dot{v_C}} = 0 $$

### Equação da Corrente $i_L$
Temos, 

$$
f(P_E) = - \frac{R_L}{L} \overline{i_L} - \frac{1}{L} \overline{v_C} + \frac{V_{in}}{L}  \overline{d} = 0
$$

$$ - R_L \overline{i_L} - \overline{v_C} + V_{in}  \overline{d} = 0 $$

$$ V_{in}  \overline{d} = R_L \overline{i_L} + \overline{v_C} $$

$$ \overline{d} = \frac{R_L}{V_{in}} \overline{i_L} + \frac{\overline{v_C}}{V_{in}} $$


Baseado nisto, podemos simplificar a equação $\dot{i_L}$ em,

$$ \dot{i_L} = - \frac{R_L}{L} i_L - \frac{1}{L} v_C + \frac{V_{in}}{L} d $$

$$ \overline{\dot{i_L}} + \delta \dot{i_L} = - \frac{R_L}{L} \left(\overline{i_L} + \delta i_L\right) - \frac{1}{L} \left(\overline{v_C} + \delta v_C\right) + \frac{V_{in}}{L} \left(\overline{d} + \delta d\right) $$

$$ \delta \dot{i_L} = - \frac{R_L}{L} \overline{i_L} - \frac{R_L}{L} \delta i_L - \frac{1}{L} \overline{v_C} - \frac{1}{L} \delta v_C + \frac{V_{in}}{L} \overline{d} + \frac{V_{in}}{L} \delta d $$

$$ \delta \dot{i_L} = - \frac{R_L}{L} \overline{i_L} - \frac{R_L}{L} \delta i_L - \frac{1}{L} \overline{v_C} - \frac{1}{L} \delta v_C + \frac{V_{in}}{L} \left( \frac{R_L}{V_{in}} \overline{i_L} + \frac{\overline{v_C}}{V_{in}}\right) + \frac{V_{in}}{L} \delta d $$

$$ \delta \dot{i_L} = - \frac{R_L}{L} \overline{i_L} - \frac{R_L}{L} \delta i_L - \frac{1}{L} \overline{v_C} - \frac{1}{L} \delta v_C +  \frac{R_L}{L} \overline{i_L} + \frac{1}{L} \overline{v_C} + \frac{V_{in}}{L} \delta d $$

$$ \delta \dot{i_L} = - \frac{R_L}{L} \delta i_L - \frac{1}{L} \delta v_C  + \frac{V_{in}}{L} \delta d $$

### Equação da Tensão $v_C$

Temos, 

$$ g(P_E) = - \frac{1}{C R_C} \overline{v_C} + \frac{1}{C} \overline{i_L} - \frac{1}{C \overline{v_C}} \overline{P_{CPL}} = 0 $$

$$ - \frac{1}{R_C} \overline{v_C} + \overline{i_L} - \frac{1}{\overline{v_C}} \overline{P_{CPL}} = 0 $$

$$  \overline{i_L} = \frac{1}{R_C} \overline{v_C} + \frac{1}{\overline{v_C}} \overline{P_{CPL}} $$


Baseado nisto, podemos simplificar a equação $\dot{v_C}$ em,

$$ 
\dot v_C = - \frac{1}{C R_C} v_C + \frac{1}{C} i_L - \frac{1}{C v_C} P_{CPL} 
$$

$$ 
\overline{\dot{v_C}} + \delta \dot{v_C} = - \frac{1}{C R_C} \left(\overline{v_C} + \delta v_C\right) + \frac{1}{C} \left( \overline{i_L} + \delta i_L\right) - \frac{1}{C \left(\overline{v_C} + \delta v_C\right)} \left(\overline{P_{CPL}} + \delta P_{CPL}\right) 
$$

$$ 
\delta \dot{v_C} = - \frac{1}{C R_C} \overline{v_C} - \frac{1}{C R_C} \delta v_C + \frac{1}{C} \overline{i_L} + \frac{1}{C}  \delta i_L - \frac{1}{C \left(\overline{v_C} + \delta v_C\right)} \left(\overline{P_{CPL}} + \delta P_{CPL}\right) 
$$

$$ 
\delta \dot{v_C} = - \frac{1}{C R_C} \overline{v_C} - \frac{1}{C R_C} \delta v_C + \frac{1}{C} \left(\frac{1}{R_C} \overline{v_C} + \frac{1}{\overline{v_C}} \overline{P_{CPL}}\right) + \frac{1}{C}  \delta i_L - \frac{1}{C \left(\overline{v_C} + \delta v_C\right)} \left(\overline{P_{CPL}} + \delta P_{CPL}\right) 
$$

$$ 
\delta \dot{v_C} = - \frac{1}{C R_C} \delta v_C + \frac{1}{C \overline{v_C}} \overline{P_{CPL}} + \frac{1}{C}  \delta i_L - \frac{1}{C \left(\overline{v_C} + \delta v_C\right)} \left(\overline{P_{CPL}} + \delta P_{CPL}\right) 
$$

$$ 
\delta \dot{v_C} = - \frac{1}{C R_C} \delta v_C  + \frac{1}{C}  \delta i_L + \frac{\overline{P_{CPL}} \delta v_C - \overline{v_C} \delta P_{CPL}}{C \overline{v_C} \left(\overline{v_C} + \delta v_C\right)} 
$$
