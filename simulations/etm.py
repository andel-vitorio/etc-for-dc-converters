import numpy as np
import cvxpy as cp
import control as ct

from utils import generate_square_signal


def get_etm_parameters(Asys, Bsys, ρ=0.5):
  A = cp.Parameter((2, 2), value=Asys)
  BU = cp.Parameter((2, 1), value=Bsys)
  I = cp.Parameter((2, 2), name='I', value=np.identity(2))

  Ξ_TIL = cp.Variable((2, 2), name='Ξ_TIL', PSD=True)
  Ψ_TIL = cp.Variable((2, 2), name='Ψ_TIL', PSD=True)
  X = cp.Variable((2, 2), name='X', PSD=True)
  K_TIL = cp.Variable((1, 2), name='K_TIL')

  obj = cp.Minimize(cp.trace(ρ * Ξ_TIL + (1 - ρ) * Ψ_TIL))

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

  return [K, Ξ, Ψ]


class StaticETM:
  """
  Class to represent the model of an Event-Triggered Mechanism (ETM) system.

  Parameters:
                  name (str): Name of the ETM.
                  Ψ (array): Ψ matrix for the calculation of Γ.
                  Ξ (array): Ξ matrix for the calculation of Γ.
  """

  def __init__(self, name, Ψ, Ξ):
    self.Ψ = Ψ
    self.Ξ = Ξ
    self.name = name
    self.previous_time = 0
    self.first_simulation = True
    self.event_times = [0.]
    self.system = ct.NonlinearIOSystem(
        None, self.etm_output,
        name=self.name,
        inputs=('x1_hat', 'x2_hat', 'x1', 'x2'),
        outputs=('x1', 'x2')
    )

  def get_gama(self, current_states, last_states_sent):
    """
    Calculates the value of Γ based on the current states and the last sent states.

    Parameters:
                    current_states (array): Current states.
                    last_states_sent (array): Last sent states.

    Returns:
                    float: Value of Γ.
    """
    error = last_states_sent - current_states
    return np.dot(current_states.T, np.dot(self.Ψ, current_states)) - np.dot(error.T, np.dot(self.Ξ, error))

  def etm_output(self, t, x, u, params):
    """
    Output function of the ETM system.

    Parameters:
                    t (float): Current time.
                    x (array): System states (not used).
                    u (array): System inputs.
                    params (dict): System parameters (not used).

    Returns:
                    array: States to be sent.
    """
    if t != self.previous_time:
      self.previous_time = t
      if self.first_simulation and t == 0.:
        self.first_simulation = False

    last_states_sent = u[0:2]
    current_states = u[2:4]

    Γ = self.get_gama(current_states, last_states_sent)
    trigger = Γ < 0

    if self.first_simulation and trigger:
      self.event_times.append(t)

    state_to_send = current_states if trigger or t == 0. else last_states_sent
    return [state_to_send[0], state_to_send[1]]


class DynamicETM:
  """
  Class to represent the model of a Dynamic Event-Triggered Mechanism (ETM) system.

  Parameters:
                  name (str): Name of the ETM.
                  Ψ (array): Ψ matrix for the calculation of Γ.
                  Ξ (array): Ξ matrix for the calculation of Γ.
                  θ (float): Threshold parameter for the event trigger mechanism.
                  λ (float): Decay rate for the dynamic update.
  """

  def __init__(self, name, Ψ, Ξ, θ, λ):
    self.Ψ = Ψ
    self.Ξ = Ξ
    self.name = name
    self.previous_time = 0
    self.first_simulation = True
    self.event_times = [0.]
    self.θ = θ
    self.λ = λ
    self.system = ct.NonlinearIOSystem(
        self.etm_update, self.etm_output,
        name=self.name, states=('n'),
        inputs=('x1_hat', 'x2_hat', 'x1', 'x2'),
        outputs=('x1', 'x2', 'n')
    )

  def get_gama(self, current_states, last_states_sent):
    """
    Calculates the value of Γ based on the current states and the last sent states.

    Parameters:
                    current_states (array): Current states.
                    last_states_sent (array): Last sent states.

    Returns:
                    float: Value of Γ.
    """
    error = last_states_sent - current_states
    return np.dot(current_states.T, np.dot(self.Ψ, current_states)) - np.dot(error.T, np.dot(self.Ξ, error))

  def etm_update(self, t, n, u, params):
    """
    Update function for the dynamic state 'n' of the ETM system.

    Parameters:
                    t (float): Current time.
                    n (array): Current value of the dynamic state 'n'.
                    u (array): System inputs.
                    params (dict): System parameters (not used).

    Returns:
                    array: Derivative of the dynamic state 'n'.
    """
    last_states_sent = u[0:2]
    current_states = u[2:4]
    Γ = self.get_gama(current_states, last_states_sent)
    dn = -self.λ * n + Γ
    return [dn]

  def etm_output(self, t, n, u, params):
    """
    Output function of the ETM system.

    Parameters:
                    t (float): Current time.
                    n (array): Current value of the dynamic state 'n'.
                    u (array): System inputs.
                    params (dict): System parameters (not used).

    Returns:
                    array: States to be sent.
    """
    if t != self.previous_time:
      self.previous_time = t
      if self.first_simulation and t == 0.:
        self.first_simulation = False

    last_states_sent = u[0:2]
    current_states = u[2:4]

    Γ = self.get_gama(current_states, last_states_sent)
    trigger = Γ < 0

    if self.first_simulation and trigger:
      self.event_times.append(t)

    state_to_send = current_states if trigger or t == 0. else last_states_sent
    return [state_to_send[0], state_to_send[1], n[0]]


class ZeroOrderHold:
  """
  Class representing a Zero-Order Hold (ZOH) system.

  This system maintains the last received input values and provides them as output for a given time step.

  """

  def __init__(self):
    self.previous_time = 0
    self.previous = []
    self.last_states_sent = [0, 0]
    self.system = ct.ss(
        None, self.zoh_output,
        name='zoh',
        inputs=('x1', 'x2'),
        outputs=('x1_hat', 'x2_hat'),
    )

  def zoh_output(self, t, x, u, params):
    """
    Output function of the ZOH system.

    Parameters:
                    t (float): Current time.
                    x (array): System states (not used).
                    u (array): System inputs.
                    params (dict): System parameters (not used).

    Returns:
                    array: Last received input values.
    """
    if t != self.previous_time:
      self.last_states_sent = self.previous
      self.previous_time = t
    self.previous = u
    return self.last_states_sent


class Controller:
  """
  Class representing a control system.

  This system applies control law to the estimated states and computes the control signal.

  """

  def __init__(self, K):
    self.K = K
    self.system = ct.ss(
        None, self.control_output,
        name='control',
        inputs=('x1_hat', 'x2_hat'),
        outputs=('u'),
    )

  def control_output(self, t, x, u, params):
    """
    Output function of the control system.

    Parameters:
                    t (float): Current time.
                    x (array): System states (not used).
                    u (array): System inputs (estimated states).
                    params (dict): System parameters (not used).

    Returns:
                    array: Control signal computed using the control law.
    """
    duty_cycle = self.K @ u
    return [duty_cycle]


def closed_loop_simulate(converter, etm, K, params, end_time,
                         perturbation_signal_data=None,
                         x0_factor=[1.5, 0.13], step=1e-5):
  """
  Simulate the closed-loop system consisting of a converter and an event-triggered mechanism (ETM).

  Parameters:
                  converter: Instance of the converter system.
                  etm: Instance of the event-triggered mechanism (ETM).
                  params (dict): Dictionary of system parameters.
                  end_time (float): End time of simulation.
                  perturbation_signal_data (list): List of tuples representing perturbation signal data.
                  x0_factor (list): Factor to multiply the initial state values to obtain the initial conditions.
                  step (float): Time step for simulation.

  Returns:
                  tuple: A tuple containing the following arrays:
                                  - t (array): Array of time points for simulation.
                                  - y (array): Array of system outputs for simulation.
                                  - inter_event_times (array): Array of inter-event times for the ETM.
                                  - event_times (array): Array of event times for the ETM.
  """
  etm.previous_time = 0
  etm.first_simulation = True
  etm.event_times = [0.]

  X_OP = np.array([params['op']['iL'], params['op']['vC']])
  timepts = np.arange(0, end_time + step, step)

  IL_INIT = x0_factor[0] * params['op']['iL']
  VC_INIT = x0_factor[1] * params['op']['vC']
  X0 = np.array([IL_INIT, VC_INIT])

  if perturbation_signal_data == None:
    perturbation_signal_data = [(0., params['op']['Pcpl'])]
  P_CPL = generate_square_signal(
      timepts, perturbation_signal_data) - params['op']['Pcpl']

  outlist = (converter.system.name + '.δiL',
             converter.system.name + '.δvC',
             converter.system.name + '.δd',
             )

  output = ('δiL', 'δvC', 'u')

  if len(etm.system.state_labels) == 1:
    outlist += (etm.system.name + '.n',)
    output += ('n',)
    X_OP = np.append(X_OP, 0)
    X0 = np.append(X0, 0)

  zoh = ZeroOrderHold()
  controller = Controller(K)

  CLOSED_LOOP_BUCK_SYSTEM = ct.interconnect(
      (converter.system, etm.system, zoh.system, controller.system),
      connections=(
          # Connection between the controller output and the plant
          (converter.system.name + '.δd', 'control.u'),

          # Connection between ZOH outputs and plant to ETM
          (etm.name + '.x1_hat', 'zoh.x1_hat'),
          (etm.name + '.x2_hat', 'zoh.x2_hat'),
          (etm.name + '.x1', converter.system.name + '.δiL'),
          (etm.name + '.x2', converter.system.name + '.δvC'),

          # Connection of ETM output in ZOH
          ('zoh.x1', etm.name + '.x1'),
          ('zoh.x2', etm.name + '.x2'),

          # Connection of ZOH output in controller
          ('control.x1_hat', 'zoh.x1_hat'),
          ('control.x2_hat', 'zoh.x2_hat'),
      ),
      name='closed_loop_buck_system',
      inplist=(converter.system.name + '.δPcpl'),
      outlist=outlist,
      output=output
  )

  t, y = ct.input_output_response(
      sys=CLOSED_LOOP_BUCK_SYSTEM, T=timepts,
      U=P_CPL,
      X0=X0 - X_OP,
      solve_ivp_method='RK45',
      solve_ivp_kwargs={'max_step': step},
      params=params
  )

  inter_event_times = [0.]

  for i in range(1, len(etm.event_times)):
    inter_event_times.append(
        etm.event_times[i] - etm.event_times[i-1])

  return t, y, inter_event_times, etm.event_times
