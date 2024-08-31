import numpy as np


def generate_square_signal(timepts, signal_data):
  """
  Generates a square wave signal based on time points and signal data.

  Parameters:
  ---
  - timepts: array-like, the time points where the signal is evaluated.
  - signal_data: list of tuples, where each tuple is (time, value). Each tuple defines the time and the corresponding signal value at that time.

  Returns:
  - numpy.ndarray: an array representing the square wave signal evaluated at the given time points.
  """
  # Initialize the signal array with zeros
  signal = np.zeros(len(timepts))

  # Iterate over each time point
  for i, t in enumerate(timepts):
    # Find the interval in signal_data that the current time point falls into
    for j in range(len(signal_data) - 1):
      if signal_data[j][0] <= t < signal_data[j + 1][0]:
        signal[i] = signal_data[j][1]
        break
    else:
      # If the time point is beyond the last defined time, use the last value
      signal[i] = signal_data[-1][1]

  return signal
