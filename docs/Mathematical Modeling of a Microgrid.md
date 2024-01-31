# Modelagem Matemática de uma Microrrede

## 1. Introdução

Neste guia, abordaremos a modelagem matemática de uma microrrede representada por um conversor buck com uma CPL, carga de potência constante. O conversor buck é um tipo de conversor de potência que converte tensão contínua de alta tensão para tensão contínua de baixa tensão. A CPL é um tipo de carga que requer uma potência constante, independentemente da tensão de entrada.

## 2. Descrição do Sistema e Circuito

O sistema a seguir foi projetado para simplificar a representação de uma microrrede, visando facilitar cálculos e análises. Composto por um conversor buck e uma CPL configurada como carga de potência constante, representada por uma fonte de corrente, o sistema oferece uma abordagem eficiente para modelar o comportamento da microrrede.

<p align="center">
  <img src="../assets/imgs/buck_conversor_with_cpl_circuit.svg" alt="Circuito Elétrico do Sistema" style="max-width:100%; height:240px;"/>
</p>

No circuito apresentado:

- $R_L, \space R_C, \space C, \space L$: Resistores, capacitor e indutor do circuito.
- $d$: Duty Cycle
- $I_{CPL}$: Corrente da CPL
- $V_{in}$: Tensão de entrada.
- $V_{out}$: Tensão de entrada.

## 3. Formulação das Equações do Circuito

As equações que descrevem o comportamento do sistema podem ser derivadas usando as leis fundamentais da eletricidade. Para isso, consideraremos o circuito em duas situações: chave fechada e aberta.

### 3.1 Chave Fechada

Na situação em que a chave está fechada, o circuito é equivalente a um circuito série com uma fonte de tensão, um resistor e uma indutância.

<div style="text-align:center">
  <img src="../assets/imgs//buck_conversor_with_cpl_circuit_m1_transparent.png" alt="Circuito Elétrico do Sistema" style="max-width: 80%;"/>
</div>
<br>

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

### 3.2 Chave Aberta

Na situação em que a chave está aberta, o circuito é desconectado da fonte de tensão.

<div style="text-align:center">
  <img src="../assets/imgs/buck_conversor_with_cpl_circuit_m2_transparent.png" alt="Circuito Elétrico do Sistema" style="max-width: 80%;"/>
</div>
<br>

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

### 3.3 Modelo Médio do Sistema

O modelo médio do sistema é:

$$
\begin{equation}
\begin{cases}
\frac{d}{dt}i_L &= \frac{V_{in}}{L} d - \frac{R_L}{L} i_L - \frac{1}{L} v_C \\ \\
\frac{d}{dt} v_C &= \frac{1}{C} i_L - \frac{1}{C R_C} v_C - \frac{1}{C v_C} P_{CPL}
\end{cases}
\end{equation}
$$

<br>

## 4. Modelo do Sistema Transladado

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

## 5. Linearização do Sistema

A seguir é apresentado os parâmetros para a linearização do sistema:

### Tabela de estados, entradas, parâmetros, ponto de operação e saída

| **Categoria**         | **Nome**                             | **Definição**                                  |
| --------------------- | ------------------------------------ | ---------------------------------------------- |
| **Estados**           | Variação da corrente do indutor      | $\delta i_L(t) = i_L(t) - {i_L}_0$             |
|                       | Variação da tensão do capacitor      | $\delta v_C(t) = v_C(t) - {v_C}_0$             |
| **Entradas**          | Variação do duty cycle               | $\delta d(t) = d(t) - d_0$                     |
|                       | Variação da potência da carga        | $\delta P_{cpl}(t) = P_{cpl}(t) - {P_{cpl}}_0$ |
| **Parâmetros**        | Tensão de entrada                    | $V_{in}$                                       |
|                       | Resistência em série com o indutor   | $R_L$                                          |
|                       | Resistência em paralelo ao capacitor | $R_c$                                          |
|                       | Indutância                           | $L$                                            |
|                       | Capacitância                         | $C$                                            |
| **Ponto de operação** | Corrente do indutor                  | ${i_L}_0$                                      |
|                       | Tensão do capacitor                  | ${v_C}_0$                                      |
|                       | Duty cycle                           | ${d}_0$                                        |
|                       | Potência da carga                    | ${P_{cpl}}_0$                                  |
| **Saída**             | Variação da Tensão do Capacitor      | $y = \delta v_C$                               |

O sistema linearizado terá a forma:

$$
  \begin{cases}
    \frac{d}{dt} (\delta i_L) &= k_1 \cdot \delta i_L + k_2 \cdot \delta v_C + k_3 \cdot \delta d \\ \\
    \frac{d}{dt} (\delta v_C) &= k_4 \cdot \delta i_L + k_5 \cdot \delta v_C + k_6 \cdot \delta P_{CPL}
  \end{cases}
$$

Considerando as seguinte relações:

$$P_f = (i_L, v_C, d), \space\space {P_f}_0 = ({i_L}_0, {v_C}_0, d_0)$$  
$$P_g = (i_L, v_C, P_{CPL}), \space\space   {P_g}_0 = ({i_L}_0, {v_C}_0, {P_{CPL}}_0)$$  
$$f(P_f) = \frac{d}{dt}i_L, \space\space  g(P_g) = \frac{d}{dt}v_C$$

Podemos obter as constante:

$$
k_1 = \dfrac{\partial f}{\partial i_L} \vert _{P_f = {P_f}_0}, \space \space
k_2 = \dfrac{\partial f}{\partial v_C} \vert _{P_f = {P_f}_0}, \space \space
k_3 = \dfrac{\partial f}{\partial d} \vert _{P_f = {P_f}_0}
$$

$$
k_4 = \dfrac{\partial g}{\partial i_L} \vert _{P_g = {P_g}_0}, \space \space
k_5 = \dfrac{\partial g}{\partial v_C} \vert _{P_g = {P_g}_0}, \space \space
k_6 = \dfrac{\partial g}{\partial P_{CPL}} \vert _{P_g = {P_g}_0}
$$

Desta forma, os termos são:

$$
k_1 = - \frac{R_L}{L}, \space\space
k_2 = - \frac{1}{L}, \space\space
k_3 = \frac{V_{in}}{L}
$$

$$
k_4 = \frac{1}{C}, \space\space
k_5 = \frac{1}{C}\left(\frac{{P_{CPL}}_0}{{{{v_{C}}_0}^2}} - \frac{1}{R_C}\right), \space\space
k_6 = - \frac{1}{C {v_C}_0}
$$

Portanto, o sistema linearizado é:

$$
  \begin{cases}
    \frac{d}{dt} (\delta i_L) &= - \frac{R_L}{L} \delta i_L - \frac{1}{L} \delta v_C + \frac{V_{in}}{L} \delta d \\ \\
    \frac{d}{dt} (\delta v_C) &= \frac{1}{C} \delta i_L + \frac{1}{C}\left(\frac{{P_{CPL}}_0}{{{{v_{C}}_0}^2}} - \frac{1}{R_C}\right) \delta v_C - \frac{1}{C {v_C}_0} \delta P_{CPL}
  \end{cases}
$$
