import numpy as np
import matplotlib.pyplot as plt
import control as ct
import control.optimal as opt
from control.matlab import *
import cvxpy as cp
import math
import pandas as pd
ct.use_fbs_defaults()


def show_matrix(name, matrix, decimal_places=2):
  """
  Apresenta uma matriz com a quantidade de casas decimais desejadas.

  Parâmetros:
  ---
  - matrix: numpy.ndarray, a matriz a ser apresentada.
  - casas_decimais: int, o número de casas decimais desejadas (padrão é 2).
  """
  pattern = "{:." + str(decimal_places) + "e}"

  def format_elem(elem):
    return pattern.format(elem)

  width = [max(map(len, map(format_elem, coluna))) for coluna in matrix.T]

  print(name, "=")

  nspaces = sum(width) + 2 * matrix.shape[1]

  print("    ┌" + " " * nspaces + "┐")
  for line in matrix:
    formatted_line = "  ".join(format_elem(e).rjust(largura)
                               for e, largura in zip(line, width))
    print("    │ " + formatted_line + " │")
  print("    └" + " " * nspaces + "┘")
  print()


def set_axs(axs, x, y, label, x_label, y_label, title):
  axs.plot(x, y, linestyle='-', color='black', label=label, linewidth=1.)
  axs.set_xlabel(x_label)
  axs.set_ylabel(y_label)
  axs.set_title(title)
  # axs.legend()
  axs.grid(linestyle='--')
  axs.tick_params(axis='both', direction='in', length=4, width=1,
                  colors='black', top=True, right=True)


def generate_square_signal(timepts, signal_data):
  signal = np.zeros(len(timepts))
  for i, t in enumerate(timepts):
    for j in range(len(signal_data) - 1):
      if signal_data[j][0] <= t < signal_data[j + 1][0]:
        signal[i] = signal_data[j][1]
        break
    else:
      signal[i] = signal_data[-1][1]
  return signal


def set_subplot(ax, x_data, y_data, xlabel, ylabel, title, line_color='#120a8f', linewidth=1.5):
  line, = ax.plot(x_data, y_data, linestyle='-',
                  color=line_color, linewidth=linewidth)
  ax.set_xlabel(xlabel, fontsize=18)
  ax.set_ylabel(ylabel, fontsize=18)
  ax.grid(linestyle='--')
  ax.set_title(title, fontsize=20)
  ax.tick_params(axis='both', direction='in', length=4, width=1,
                 colors='black', top=True, right=True, labelsize=16)

  return line


def set_axe_stem(ax, x, y, xlabel, ylabel, linefmt='-', markerfmt=None, basefmt=' ', bottom=0, grid=True, fontsize=16):
  """
  Plota os gráficos de hastes (stem plots) em um subplot e configura os eixos.

  Parâmetros:
                  ax (AxesSubplot): Eixo do subplot.
                  x (array): Valores para o eixo x.
                  y (array): Valores para o eixo y.
                  xlabel (str): Rótulo do eixo x.
                  ylabel (str): Rótulo do eixo y.
                  linefmt (str): Formato da linha. O padrão é '-'.
                  markerfmt (str): Formato do marcador. O padrão é None.
                  basefmt (str): Formato da base. O padrão é None.
                  bottom (float): Posição da base das hastes. O padrão é 0.
                  grid (bool): Se True, habilita as linhas de grade. O padrão é True.
                  fontsize (int): Tamanho da fonte. O padrão é 16.
  """
  ax.stem(x, y, linefmt=linefmt, markerfmt=markerfmt,
          basefmt=basefmt, bottom=bottom)
  ax.set_xlabel(xlabel, fontsize=fontsize)
  ax.set_ylabel(ylabel, fontsize=fontsize)
  ax.tick_params(axis='both', direction='in', length=4, width=1,
                 colors='black', top=True, right=True, labelsize=fontsize)
  if grid:
    ax.grid(linestyle='--')


def create_figure_two_by_one(title_figure, data_1, data_2, fig_name, path='./'):
  fig, axs = plt.subplots(1, 2, figsize=(12, 3))
  fig.suptitle(title_figure, fontsize=22)

  set_subplot(
      axs[0], data_1['x'], data_1['y'],
      data_1['x_label'], data_1['y_label'], data_1['title'],
  )

  set_subplot(
      axs[1], data_2['x'], data_2['y'],
      data_2['x_label'], data_2['y_label'], data_2['title'],
  )

  plt.tight_layout()
  plt.savefig(
      path + '/' + fig_name + '.eps',
      format='eps', bbox_inches='tight')
  plt.close()


def create_figure_two_by_two(title_figure, data_1, data_2, legends, fig_name, path='./'):
  fig, axs = plt.subplots(1, 2, figsize=(12, 3))
  fig.suptitle(title_figure, fontsize=22)

  line1 = set_subplot(
      axs[0], data_1['x1'], data_1['y1'],
      data_1['x_label'], data_1['y_label'], data_1['title'],
  )

  line2 = set_subplot(
      axs[0], data_1['x2'], data_1['y2'],
      data_1['x_label'], data_1['y_label'], data_1['title'],
      line_color='#8b0000'
  )

  set_subplot(
      axs[1], data_2['x1'], data_2['y1'],
      data_2['x_label'], data_2['y_label'], data_2['title'],
  )

  set_subplot(
      axs[1], data_2['x2'], data_2['y2'],
      data_2['x_label'], data_2['y_label'], data_2['title'], line_color='#8b0000'
  )

  fig.legend([line1, line2], legends,
             fontsize=18, loc='upper center', bbox_to_anchor=(.5, 0.0), fancybox=False, shadow=False, ncol=2)

  plt.tight_layout()
  plt.savefig(
      path + '/' + fig_name + '.eps',
      format='eps', bbox_inches='tight')
  plt.close()


def create_etm_results_figures(
    title, fig_prefix, path, op,
    t_etm_nl, y_etm_nl, iet_etm_nl, et_etm_nl,
    t_etm_l, y_etm_l, iet_etm_l, et_etm_l
):

  create_figure_two_by_two(
      title_figure=title + ': States $i_L$ and $v_C$',
      data_1={
          'x1': t_etm_nl, 'x2': t_etm_l,
          'y1': y_etm_nl[0] + op['iL'], 'y2': y_etm_l[0] + op['iL'],
          'x_label': 'Time (s)', 'y_label': '$i_L$ (A)',
          'title': 'Inductor Current $i_L(t)$'
      },
      data_2={
          'x1': t_etm_nl, 'x2': t_etm_l,
          'y1': y_etm_nl[1] + op['vC'], 'y2': y_etm_l[1] + op['vC'],
          'x_label': 'Time (s)', 'y_label': '$v_C$ (V)',
          'title': 'Capacitor Voltage $v_C(t)$'
      },
      legends=['Non-linear', 'Linearized'],
      fig_name=fig_prefix + '_states',
      path=path
  )

  create_figure_two_by_one(
      title_figure=title + ': States $i_L$ and $v_C$',
      data_1={
          'x': t_etm_nl[1:], 'y': y_etm_nl[2][1:] + op['d'],
          'x_label': 'Time (s)', 'y_label': '$d$',
          'title': 'Duty Cycle (Non-linear)'
      },
      data_2={
          'x': t_etm_l[1:], 'y':  y_etm_l[2][1:] + op['d'],
          'x_label': 'Time (s)', 'y_label': '$d$',
          'title': 'Duty Cycle (Linearized)'
      },
      fig_name=fig_prefix + '_duty_cycle',
      path=path
  )

  fig, axs = plt.subplots(1, 2, figsize=(12, 3))
  fig.suptitle(title + ": Inter-event Times", fontsize=20)

  set_axe_stem(
      axs[0], et_etm_nl, iet_etm_nl,
      'Tempo (s)', 'IET (s)', linefmt='#120a8f', markerfmt='o', bottom=0)
  set_axe_stem(
      axs[1], et_etm_l, iet_etm_l, 'Tempo (s)',
      'IET (s)', linefmt='#8b0000', markerfmt='o', bottom=0)

  fig.legend(['Não Linear', 'Linearizado'],
             fontsize=14, loc='upper center', bbox_to_anchor=(.5, 0.), fancybox=False, shadow=False, ncol=2)

  plt.tight_layout()
  plt.savefig(
      path + '/' + fig_prefix + '_inter_event_times.eps',
      format='eps', bbox_inches='tight')
  plt.close()

  if len(y_etm_nl) == 4 and len(y_etm_l) == 4:
    fig, axs = plt.subplots(1, 2, figsize=(12, 3))
    fig.suptitle(title + ": Dynamic Variable", fontsize=20)
    line1 = set_subplot(
        axs[0], t_etm_nl, y_etm_nl[3] + op['d'],
        'Time (s)', '$\eta$', '')
    line2 = set_subplot(
        axs[1], t_etm_l, y_etm_l[3] + op['d'],
        'Time (s)', '$\eta$', '',
        line_color='#8b0000')

    fig.legend([line1, line2], ['Non-linear', 'Linearized'],
               fontsize=18, loc='upper center', bbox_to_anchor=(.5, 0.0), fancybox=False, shadow=False, ncol=2)
    plt.tight_layout()
    plt.savefig(
        path + '/' + fig_prefix + '_eta.eps',
        format='eps', bbox_inches='tight')
    plt.close()
