import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import control as ct
import control.optimal as opt
from control.matlab import *
import cvxpy as cp
import math
import pandas as pd
import json
import argparse

import utils
import etm

ct.use_fbs_defaults()
matplotlib.use('Agg')


class NonlinearBuckConverter:
  """
  Classe para criar e gerenciar o modelo não linear de um conversor Buck.

  Parâmetros:
                  name (str): Nome do sistema.
  """

  def __init__(self, name):
    self.name = name
    self.inputs = ('D', 'P_CPL')
    self.outputs = ('iL', 'vC')
    self.states = ('iL', 'vC')
    self.system = ct.NonlinearIOSystem(
        self.update, self.output, name=self.name,
        inputs=self.inputs, outputs=self.outputs, states=self.states
    )

  def update(self, t, x, u, params):
    """
    Função de atualização para a representação em espaço de estados do conversor Buck.

    Parâmetros:
                    t (float): Tempo.
                    x (array): Estados do sistema.
                    u (array): Entradas do sistema.
                    params (dict): Dicionário de parâmetros do sistema.

    Retorna:
                    dx (array): Derivada dos estados do sistema.
    """
    V_IN = params.get('Vin', 0)  # Tensão de entrada
    RL = params.get('rL', 0)     # Resistência (indutor)
    RC = params.get('rC', 0)     # Resistência (capacitor)
    L = params.get('L', 1)       # Indutância
    C = params.get('C', 1)       # Capacitância

    D, P_CPL = u

    IL, VC = x

    diL = (V_IN / L) * D - (RL / L) * IL - VC / L
    dvC = IL / C - VC / (C * RC) - P_CPL / (C * VC)

    dx = np.array([diL, dvC])
    return dx

  def output(self, t, x, u, params):
    """
    Função de saída para a representação em espaço de estados do conversor Buck.

    Parâmetros:
                    t (float): Tempo.
                    x (array): Estados do sistema.
                    u (array): Entradas do sistema.
                    params (dict): Dicionário de parâmetros do sistema.

    Retorna:
                    array: Saída do sistema.
    """
    return x[0:2]


class ShiftedNonlinearBuckConverter:
  """
  Classe para criar e gerenciar o modelo não linear deslocado de um sistema.

  Parâmetros:
                  name (str): Nome do sistema.
  """

  def __init__(self, name):
    self.name = name
    self.inputs = ('δd', 'δPcpl')
    self.outputs = ('δiL', 'δvC')
    self.states = ('δiL', 'δvC')
    self.system = ct.NonlinearIOSystem(
        self.update, self.output, name=self.name,
        inputs=self.inputs, outputs=self.outputs, states=self.states
    )

  def update(self, t, x, u, params):
    """
    Função de atualização para a representação em espaço de estados do sistema não linear deslocado.

    Parâmetros:
                    t (float): Tempo.
                    x (array): Estados do sistema.
                    u (array): Entradas do sistema.
                    params (dict): Dicionário de parâmetros do sistema.

    Retorna:
                    dx (array): Derivada dos estados do sistema.
    """
    V_IN = params.get('Vin', 0)  # Tensão de entrada
    RL = params.get('rL', 0)     # Resistência (indutor)
    RC = params.get('rC', 0)     # Resistência (capacitor)
    L = params.get('L', 1)       # Indutância
    C = params.get('C', 1)       # Capacitância
    OP = params.get('op', {'Pcpl': 0, 'vC': 0})  # Ponto de operação

    # print(params)

    δD, δP_CPL = u
    δIL, δVC = x

    DELTA_IL_DOT = - (RL / L) * δIL - δVC / L + (V_IN / L) * δD
    DELTA_VC_DOT = - δVC / (C * RC) + δIL / C + \
        (OP['Pcpl'] * δVC - OP['vC'] * δP_CPL) / \
        (C * OP['vC'] * (OP['vC'] + δVC))

    dx = np.array([DELTA_IL_DOT, DELTA_VC_DOT])
    return dx

  def output(self, t, x, u, params):
    """
    Função de saída para a representação em espaço de estados do sistema não linear deslocado.

    Parâmetros:
                    t (float): Tempo.
                    x (array): Estados do sistema.
                    u (array): Entradas do sistema.
                    params (dict): Dicionário de parâmetros do sistema.

    Retorna:
                    array: Saída do sistema.
    """
    return x[:2]


class LinearizedBuckConverter:
  """
  Classe para criar e gerenciar o modelo linearizado de um sistema.

  Parâmetros:
                  name (str): Nome do sistema.
                  params (dict): Dicionário de parâmetros do sistema e ponto de operação.
  """

  def __init__(self, name, params):
    self.name = name
    self.params = params
    self.system = self.create_system()

  def create_system(self):
    """
    Cria o modelo linearizado do sistema com base nos parâmetros fornecidos.

    Retorna:
                    system: Representação do sistema em espaço de estados linearizado.
    """
    OP = self.params['op']

    # Elementos da matriz de estados
    A11 = - (self.params['rL'] / self.params['L'])
    A12 = - (1. / self.params['L'])
    A21 = 1. / self.params['C']
    A22 = (1. / self.params['C']) * (OP['Pcpl'] /
                                     (OP['vC'] ** 2) - 1. / self.params['rC'])

    # Elementos da matriz de entrada
    B11 = self.params['Vin'] / self.params['L']
    B12 = 0.
    B21 = 0.
    B22 = - 1.0 / (self.params['C'] * OP['vC'])

    # Matriz de estados: iL e vC
    A = [[A11, A12], [A21, A22]]

    # Matriz de entrada: δd e δP_cpl
    B = [[B11, B12], [B21, B22]]

    # Matriz de saída: iL e vC
    C = [[1., 0], [0., 1]]

    # Matriz de alimentação direta: nula
    D = [[0., 0.], [0., 0.]]

    # Criando o sistema linearizado
    system = ct.ss2io(ct.ss(A, B, C, D), name=self.name, inputs=(
        'δd', 'δPcpl'), outputs=('δiL', 'δvC'), states=('δiL', 'δvC'))
    return system


def create_params(V_IN, RL, RC, L, C, PCPL_OP, VC_OP):
  """
  Create a dictionary of parameters for the system model.

  Parameters:
                  V_IN (float): Input voltage.
                  RL (float): Resistance of the inductor.
                  RC (float): Resistance of the capacitor.
                  L (float): Inductance.
                  C (float): Capacitance.
                  PCPL_OP (float): Operating power of the CPL.
                  VC_OP (float): Operating voltage of the capacitor.

  Returns:
                  dict: Dictionary of system parameters.

  """
  # Calculate the operating point (OP) values for inductor current and duty cycle
  IL_OP = (VC_OP / RC) + PCPL_OP / VC_OP
  D_OP = (RL * IL_OP) / V_IN + VC_OP / V_IN

  # Create the dictionary of parameters
  params = {
      "Vin": V_IN,
      "rL": RL,
      "rC": RC,
      "L": L,
      "C": C,
      "op": {"Pcpl": PCPL_OP, "vC": VC_OP, "iL": IL_OP, "d": D_OP},
  }

  return params


def simulate(converter, params, perturbation_signal_data=None, end_time=0.1, step=1e-5, initial_factor=[1.5, 0.13]):
  """
  Simulate the system based on the provided parameters and time settings.

  Parameters:
                  params (dict): Dictionary of system parameters obtained from create_params function.
                  end_time (float): End time of simulation.
                  step (float): Time step for simulation.
                  initial_factor (float): Factor to multiply the initial state values to obtain the initial conditions.
                  perturb_factor (float): Factor to multiply the perturbation values to obtain the perturbed conditions.

  Returns:
                  tuple: A tuple containing the following arrays:
                                  - timepts (array): Array of time points for simulation.
                                  - U (array): Array of system inputs for simulation.
                                  - X0 (array): Array of initial states for simulation.
                                  - δU (array): Array of perturbations in system inputs.
                                  - δX0 (array): Array of perturbations in initial states.
                                  - params (dict): Dictionary of system parameters.
  """

  # Ponto de operação de cada entrada e estado do sistema
  U_OP = np.array([params['op']['d'], params['op']['Pcpl']])
  X_OP = np.array([params['op']['iL'], params['op']['vC']])

  # Instantes de tempo
  timepts = np.arange(0, end_time + step, step)

  # Entradas do Sistema
  if perturbation_signal_data == None:
    perturbation_signal_data = [(0., U_OP[1])]
  P_CPL = utils.generate_square_signal(timepts, perturbation_signal_data)

  D = [params['op']['d'] for _ in range(len(timepts))]
  U = [D, P_CPL.tolist()]

  # Estados Iniciais do Sistema
  IL_INIT = initial_factor[0] * params['op']['iL']
  VC_INIT = initial_factor[1] * params['op']['vC']
  X0 = np.array([IL_INIT, VC_INIT])

  INPUT, INITIAL_STATE = U, X0

  if not isinstance(converter, NonlinearBuckConverter):
    INPUT = U - U_OP[:, np.newaxis]
    INITIAL_STATE = X0 - X_OP
  else:
    INPUT = U
    INITIAL_STATE = X0

  if isinstance(converter, LinearizedBuckConverter):
    return ct.input_output_response(
        sys=converter.system, T=timepts,
        U=INPUT, X0=INITIAL_STATE,
    )

  return ct.input_output_response(
      sys=converter.system, T=timepts,
      U=INPUT, X0=INITIAL_STATE, params=params,
  )


def main(args):
  with open(args.json_file, 'r') as file:
    data = json.load(file)

  for scenario in data:

    if data[scenario]['ignore']:
      continue

    end_time = data[scenario]['end_time_simulation']
    scenario_tag = data[scenario]['tag']
    initial_states_factor = data[scenario]['initial_states_factor']
    circuit_params = data[scenario]['circuit_params']
    desired_values = data[scenario]['desired_values']
    pcpl_signal_data = [(d['t'], d['pcpl'])
                        for d in data[scenario]['pcpl_signal_data']]
    params = create_params(
        V_IN=circuit_params['input_voltage'],
        RC=circuit_params['constant_resistance_load'],
        RL=circuit_params['inductor_winding_resistance'],
        L=circuit_params['inductance'],
        C=circuit_params['capacitance'],
        PCPL_OP=desired_values['pcpl_power'],
        VC_OP=desired_values['capacitor_voltage']
    )
    step = 1e-5
    path = './buck/results/' + scenario_tag
    os.makedirs(path, exist_ok=True)

    print(f'[{scenario_tag}]\tNew simulation started!')

    buck_nonlinear = NonlinearBuckConverter('buck_nonlinear')

    print(f'[{scenario_tag}]\tNon-linear buck converter simulation start')
    t_nonlinear, y_nonlinear = simulate(
        converter=buck_nonlinear,
        params=params,
        end_time=end_time,
        initial_factor=initial_states_factor,
        perturbation_signal_data=pcpl_signal_data,
        step=step,
    )
    print(f'[{scenario_tag}]\tNon-linear buck converter simulation finalized')

    utils.create_figure_two_by_one(
        title_figure='Non-linear Buck Converter: States $i_L$ and $v_C$',
        data_1={
            'x': t_nonlinear, 'y': y_nonlinear[0],
            'x_label': 'Time (s)', 'y_label': '$i_L$ (A)',
            'title': 'Inductor Current $i_L(t)$'
        },
        data_2={
            'x': t_nonlinear, 'y': y_nonlinear[1],
            'x_label': 'Time (s)', 'y_label': '$v_C$ (V)',
            'title': 'Capacitor Voltage $v_C(t)$'
        },
        fig_name='buck_nonlinear_states',
        path=path
    )

    print(f'[{scenario_tag}]\tNon-linear buck converter simulation result saved\n')

    buck_shifted_nonlinear = ShiftedNonlinearBuckConverter(
        'buck_shifted_nonlinear')

    print(f'[{scenario_tag}]\tShifted non-linear buck converter simulation start')
    t_shifted_nonlinear, y_shifted_nonlinear = simulate(
        converter=buck_shifted_nonlinear,
        params=params,
        end_time=end_time,
        initial_factor=initial_states_factor,
        perturbation_signal_data=pcpl_signal_data,
        step=step,
    )

    print(f'[{scenario_tag}]\tShifted non-linear buck converter simulation finalized')
    utils.create_figure_two_by_one(
        title_figure='Shifted Non-linear Buck Converter: States $i_L$ and $v_C$',
        data_1={
            'x': t_shifted_nonlinear,
            'y': y_shifted_nonlinear[0] + params['op']['iL'],
            'x_label': 'Time (s)', 'y_label': '$i_L$ (A)',
            'title': 'Inductor Current $i_L(t)$'
        },
        data_2={
            'x': t_shifted_nonlinear,
            'y': y_shifted_nonlinear[1] + params['op']['vC'],
            'x_label': 'Time (s)', 'y_label': '$v_C$ (V)',
            'title': 'Capacitor Voltage $v_C(t)$'
        },
        fig_name='buck_shifted_nonlinear_states',
        path=path
    )
    print(
        f'[{scenario_tag}]\tShifted non-linear buck converter simulation result saved')

    buck_linearized = LinearizedBuckConverter(
        'buck_linearized', params)

    t_linearized, y_linearized = simulate(
        converter=buck_linearized,
        params=params,
        end_time=end_time,
        initial_factor=initial_states_factor,
        perturbation_signal_data=pcpl_signal_data,
        step=step,
    )

    print(f'\n[{scenario_tag}]\tLinearized buck converter simulation started')
    utils.create_figure_two_by_one(
        title_figure='Linearized Buck Converter: States $i_L$ and $v_C$',
        data_1={
            'x': t_linearized,
            'y': y_linearized[0] + params['op']['iL'],
            'x_label': 'Time (s)', 'y_label': '$i_L$ (A)',
            'title': 'Inductor Current $i_L(t)$'
        },
        data_2={
            'x': t_linearized,
            'y': y_linearized[1] + params['op']['vC'],
            'x_label': 'Time (s)', 'y_label': '$v_C$ (V)',
            'title': 'Capacitor Voltage $v_C(t)$'
        },
        fig_name='buck_linearized_states',
        path=path
    )

    print(f'[{scenario_tag}]\tLinearized buck converter simulation finalized')
    utils.create_figure_two_by_two(
        title_figure='Non-linear vs Linearized Buck Converter: States $i_L$ and $v_C$',
        data_1={
            'x1': t_shifted_nonlinear, 'x2': t_linearized,
            'y1': y_shifted_nonlinear[0] + params['op']['iL'],
            'y2': y_linearized[0] + params['op']['iL'],
            'x_label': 'Time (s)', 'y_label': '$i_L$ (A)',
            'title': 'Inductor Current $i_L(t)$'
        },
        data_2={
            'x1': t_shifted_nonlinear, 'x2': t_linearized,
            'y1': y_shifted_nonlinear[1] + params['op']['vC'],
            'y2': y_linearized[1] + params['op']['vC'],
            'x_label': 'Time (s)', 'y_label': '$v_C$ (V)',
            'title': 'Capacitor Voltage $v_C(t)$'
        },
        legends=['Non-linear', 'Linearized'],
        fig_name='buck_nonlinear_vs_linearized_states',
        path=path
    )
    print(f'[{scenario_tag}]\tLinearized buck converter simulation result saved')

    print(f'\n[{scenario_tag}]\tSolving the optimization problem to obtain the ETM design parameters.')

    A = cp.Parameter((2, 2), value=buck_linearized.system.A)
    BU = cp.Parameter((2, 1), value=buck_linearized.system.B[:, 0])
    I = cp.Parameter((2, 2), name='I', value=np.identity(2))

    Ξ_TIL = cp.Variable((2, 2), name='Ξ_TIL', PSD=True)
    Ψ_TIL = cp.Variable((2, 2), name='Ψ_TIL', PSD=True)
    X = cp.Variable((2, 2), name='X', PSD=True)
    K_TIL = cp.Variable((1, 2), name='K_TIL')

    _lambda = .5

    obj = cp.Minimize(cp.trace(_lambda * Ξ_TIL + (1 - _lambda) * Ψ_TIL))

    M11 = A @ X + BU @ K_TIL + X @ A.T + K_TIL.T @ BU.T
    M12 = BU @ K_TIL
    M13 = X

    M21 = K_TIL.T @ BU.T
    M22 = -Ξ_TIL
    M23 = np.zeros(shape=(2, 2))

    M31 = X
    M32 = np.zeros(shape=(2, 2))
    M33 = -Ψ_TIL

    M = cp.bmat([[M11, M12, M13],
                [M21, M22, M23],
                [M31, M32, M33]])

    constraints = [M << 0]
    constraints += [1e-9 * np.eye(2) <= Ξ_TIL]
    constraints += [Ξ_TIL <= 1e9 * np.eye(2)]
    constraints += [1e-9 * np.eye(2) <= Ψ_TIL]
    constraints += [Ψ_TIL <= 1e9 * np.eye(2)]

    prob = cp.Problem(obj, constraints)
    prob.solve(solver=cp.MOSEK, verbose=False)

    K = None
    Ξ = None
    Ψ = None

    if prob.status not in ["infeasible", "unbounded"]:
      # print("Optimal value: %s\n" % prob.value)
      # for variable in prob.variables():
        # if len(variable.shape) == 2:
        #   show_matrix(variable.name(), variable.value)
        # else:
        #   print(variable.name(), '=', variable.value, '\n')

        # Compute the inverse of X and use it to calculate Ξ and K
      X_INV = np.linalg.inv(X.value)
      Ξ = X_INV @ Ξ_TIL.value @ X_INV

      _K = K_TIL @ X_INV
      K = _K.value

      # utils.show_matrix('K', K)

      Ψ = np.linalg.inv(Ψ_TIL.value)

      # utils.show_matrix('Ξ', Ξ)
      # utils.show_matrix('Ψ', Ψ)
    else:
      print('The problem is not feasible')
      continue

    print(f'[{scenario_tag}]\tDesign parameters obtained\n')

    print(
        f'[{scenario_tag}]\tNon-linear buck converter under static etm simulation start')

    setm = etm.StaticETM('etm', Ψ, Ξ)

    t_setm_nl, y_setm_nl, iet_setm_nl, et_setm_nl = etm.closed_loop_simulate(
        buck_shifted_nonlinear, setm, K, params, end_time,
        pcpl_signal_data, initial_states_factor)

    print(
        f'[{scenario_tag}]\tNon-linear buck converter under static etm simulation finalized')

    print(
        f'[{scenario_tag}]\tLinearized buck converter under static etm simulation start')

    t_setm_l, y_setm_l, iet_setm_l, et_setm_l = etm.closed_loop_simulate(
        buck_linearized, setm, K, params, end_time,
        pcpl_signal_data, initial_states_factor,)
    print(
        f'[{scenario_tag}]\tLinearized buck converter under static etm simulation finalized')

    utils.create_etm_results_figures(
        'Buck Converter Under Static ETM',
        'buck_under_static_etm', path, params['op'],
        t_setm_nl, y_setm_nl, iet_setm_nl, et_setm_nl,
        t_setm_l, y_setm_l, iet_setm_l, et_setm_l
    )

    print(
        f'[{scenario_tag}]\tBuck converter under static etm simulation result saved')

    print(
        f'[{scenario_tag}]\tNon-linear buck converter under static etm simulation start')

    detm = etm.DynamicETM('etm', Ψ, Ξ, θ=1, λ=100)

    t_detm_nl, y_detm_nl, iet_detm_nl, et_detm_nl = etm.closed_loop_simulate(
        buck_shifted_nonlinear, detm, K, params, end_time,
        pcpl_signal_data, initial_states_factor)

    print(
        f'[{scenario_tag}]\tNon-linear buck converter under dynamic etm simulation finalized')

    print(
        f'[{scenario_tag}]\tLinearized buck converter under dynamic etm simulation start')

    t_detm_l, y_detm_l, iet_detm_l, et_detm_l = etm.closed_loop_simulate(
        buck_linearized, detm, K, params, end_time,
        pcpl_signal_data, initial_states_factor,)
    print(
        f'[{scenario_tag}]\tLinearized buck converter under dynamic etm simulation finalized')

    utils.create_etm_results_figures(
        'Buck Converter Under Dynamic ETM',
        'buck_under_dynamic_etm', path, params['op'],
        t_detm_nl, y_detm_nl, iet_detm_nl, et_detm_nl,
        t_detm_l, y_detm_l, iet_detm_l, et_detm_l
    )

    print(
        f'[{scenario_tag}]\tBuck converter under dynamic etm simulation result saved')

    print('\n')


    
    


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Process a JSON file.')
  parser.add_argument('json_file', type=str, help='Path to the JSON file')
  args = parser.parse_args()
  main(args)
