import numpy as np


def generate_square_signal(timepts, signal_data):
  """
  Gera um sinal quadrado baseado em pontos de tempo e dados de sinal.

  Parâmetros:
  ---
  - timepts: array-like, os pontos de tempo onde o sinal é avaliado.
  - signal_data: list of tuples, onde cada tupla é (tempo, valor).
  """
  signal = np.zeros(len(timepts))
  for i, t in enumerate(timepts):
    for j in range(len(signal_data) - 1):
      if signal_data[j][0] <= t < signal_data[j + 1][0]:
        signal[i] = signal_data[j][1]
        break
    else:
      signal[i] = signal_data[-1][1]
  return signal
