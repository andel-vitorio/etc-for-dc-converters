import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator


def set_subplot(ax, x_data, y_data, xlabel, ylabel, title, label='',
                x_digits=1, y_digits=1, line_color='#120a8f', linewidth=2.,
                title_pad=20, x_label_pad=8, y_label_pad=8,
                y_min=None, y_max=None,
                x_tick_interval=None, y_tick_interval=None):
  """
  Configura um subplot com as propriedades definidas.
  """
  ax.xaxis.set_major_formatter(
      FuncFormatter(lambda v, _: f'{v:.{x_digits}f}'))
  ax.yaxis.set_major_formatter(
      FuncFormatter(lambda v, _: f'{v:.{y_digits}f}'))

  if y_min is not None and y_max is not None:
    ax.set_ylim(y_min, y_max)

  if x_tick_interval is not None:
    ax.xaxis.set_major_locator(MultipleLocator(x_tick_interval))

  if y_tick_interval is not None:
    ax.yaxis.set_major_locator(MultipleLocator(y_tick_interval))

  line, = ax.plot(x_data, y_data, label=label, linestyle='-',
                  color=line_color, linewidth=linewidth)

  ax.set_xlabel(xlabel, fontsize=20, labelpad=x_label_pad)
  ax.set_ylabel(ylabel, fontsize=20, labelpad=y_label_pad)
  ax.grid(linestyle='--')
  ax.set_title(title, fontsize=24, pad=title_pad)
  ax.tick_params(axis='both', direction='in', length=4, width=1,
                 colors='black', top=True, right=True, labelsize=18)

  if label:
    ax.legend(frameon=True, loc='best', framealpha=1, prop={'size': 16})

  return line


def set_stem(ax, x_data, y_data, xlabel, ylabel, title,
             x_digits=3, y_digits=2, line_color='#120a8f', marker_size=4,
             stem_width=2., title_pad=16, x_label_pad=8, y_label_pad=8, label='',
             x_min=None, x_max=None, y_min=None, y_max=None):
  """
  Configura um gráfico do tipo stem com as propriedades definidas.
  """
  ax.xaxis.set_major_formatter(FuncFormatter(
      lambda v, _: f'{v:.{x_digits}f}'.rjust(x_digits + y_digits + 1)))
  ax.yaxis.set_major_formatter(FuncFormatter(
      lambda v, _: f'{v:.{y_digits}f}'.rjust(x_digits + y_digits + 1)))

  markerline, stemlines, baseline = ax.stem(x_data, y_data, linefmt=line_color,
                                            markerfmt='o', basefmt=' ', bottom=0, label=label)
  plt.setp(stemlines, 'linewidth', stem_width)
  plt.setp(markerline, 'markersize', marker_size)

  ax.set_xlabel(xlabel, fontsize=20, labelpad=x_label_pad)
  ax.set_ylabel(ylabel, fontsize=20, labelpad=y_label_pad)
  ax.grid(linestyle='--')
  ax.set_title(title, fontsize=24, pad=title_pad)

  if x_min is not None and x_max is not None:
    ax.set_xlim(x_min, x_max)

  if y_min is not None and y_max is not None:
    ax.set_ylim(y_min, y_max)

  ax.tick_params(axis='both', direction='in', length=4, width=1,
                 colors='black', top=True, right=True, labelsize=18)

  if label:
    ax.legend(frameon=True, loc='best', framealpha=1, prop={'size': 16})

  return markerline, stemlines, baseline


def use_latex():
  """
  Configura o Matplotlib para usar o LaTeX se disponível.
  Se o LaTeX não estiver disponível, utiliza fontes padrão.
  """
  try:
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "Palatino"
    })
    print("LaTeX foi habilitado para renderização de textos.")
  except Exception:
    plt.rcParams.update({
        "text.usetex": False,
        "font.family": "sans-serif"
    })
    print("LaTeX não está disponível. Usando fontes padrão.")
