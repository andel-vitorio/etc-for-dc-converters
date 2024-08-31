import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator


def set_subplot(ax, x_data, y_data, xlabel, ylabel, title, label='',
                x_digits=1, y_digits=1, line_color='#120a8f', linewidth=2.,
                title_pad=20, x_label_pad=8, y_label_pad=8,
                y_min=None, y_max=None,
                x_tick_interval=None, y_tick_interval=None):
  """
  Configures a subplot with the specified properties.

  Parameters:
  ---
  - ax: matplotlib.axes.Axes, the subplot to configure.
  - x_data: array-like, the x data for the plot.
  - y_data: array-like, the y data for the plot.
  - xlabel: str, the label for the x-axis.
  - ylabel: str, the label for the y-axis.
  - title: str, the title of the subplot.
  - label: str, the label for the plot legend (default is an empty string).
  - x_digits: int, the number of decimal places for x-axis labels (default is 1).
  - y_digits: int, the number of decimal places for y-axis labels (default is 1).
  - line_color: str, the color of the plot line (default is '#120a8f').
  - linewidth: float, the width of the plot line (default is 2.0).
  - title_pad: float, the padding of the title from the plot (default is 20).
  - x_label_pad: float, the padding of the x-axis label from the plot (default is 8).
  - y_label_pad: float, the padding of the y-axis label from the plot (default is 8).
  - y_min: float, the minimum value of the y-axis (default is None).
  - y_max: float, the maximum value of the y-axis (default is None).
  - x_tick_interval: float, the interval for x-axis ticks (default is None).
  - y_tick_interval: float, the interval for y-axis ticks (default is None).
  """
  # Format x and y axis labels with specified decimal places
  ax.xaxis.set_major_formatter(
      FuncFormatter(lambda v, _: f'{v:.{x_digits}f}'))
  ax.yaxis.set_major_formatter(
      FuncFormatter(lambda v, _: f'{v:.{y_digits}f}'))

  # Set y-axis limits if specified
  if y_min is not None and y_max is not None:
    ax.set_ylim(y_min, y_max)

  # Set x and y axis tick intervals if specified
  if x_tick_interval is not None:
    ax.xaxis.set_major_locator(MultipleLocator(x_tick_interval))

  if y_tick_interval is not None:
    ax.yaxis.set_major_locator(MultipleLocator(y_tick_interval))

  # Plot the data
  line, = ax.plot(x_data, y_data, label=label, linestyle='-',
                  color=line_color, linewidth=linewidth)

  # Set axis labels and title with specified font sizes and padding
  ax.set_xlabel(xlabel, fontsize=20, labelpad=x_label_pad)
  ax.set_ylabel(ylabel, fontsize=20, labelpad=y_label_pad)
  ax.grid(linestyle='--')
  ax.set_title(title, fontsize=24, pad=title_pad)
  ax.tick_params(axis='both', direction='in', length=4, width=1,
                 colors='black', top=True, right=True, labelsize=18)

  # Display the legend if a label is provided
  if label:
    ax.legend(frameon=True, loc='best', framealpha=1, prop={'size': 16})

  return line


def set_stem(ax, x_data, y_data, xlabel, ylabel, title,
             x_digits=3, y_digits=2, line_color='#120a8f', marker_size=4,
             stem_width=2., title_pad=16, x_label_pad=8, y_label_pad=8, label='',
             x_min=None, x_max=None, y_min=None, y_max=None):
  """
  Configures a stem plot with the specified properties.

  Parameters:
  ---
  - ax: matplotlib.axes.Axes, the subplot to configure.
  - x_data: array-like, the x data for the stem plot.
  - y_data: array-like, the y data for the stem plot.
  - xlabel: str, the label for the x-axis.
  - ylabel: str, the label for the y-axis.
  - title: str, the title of the subplot.
  - x_digits: int, the number of decimal places for x-axis labels (default is 3).
  - y_digits: int, the number of decimal places for y-axis labels (default is 2).
  - line_color: str, the color of the stem lines (default is '#120a8f').
  - marker_size: int, the size of the markers (default is 4).
  - stem_width: float, the width of the stem lines (default is 2.0).
  - title_pad: float, the padding of the title from the plot (default is 16).
  - x_label_pad: float, the padding of the x-axis label from the plot (default is 8).
  - y_label_pad: float, the padding of the y-axis label from the plot (default is 8).
  - label: str, the label for the plot legend (default is an empty string).
  - x_min: float, the minimum value of the x-axis (default is None).
  - x_max: float, the maximum value of the x-axis (default is None).
  - y_min: float, the minimum value of the y-axis (default is None).
  - y_max: float, the maximum value of the y-axis (default is None).
  """
  # Format x and y axis labels with specified decimal places
  ax.xaxis.set_major_formatter(FuncFormatter(
      lambda v, _: f'{v:.{x_digits}f}'.rjust(x_digits + y_digits + 1)))
  ax.yaxis.set_major_formatter(FuncFormatter(
      lambda v, _: f'{v:.{y_digits}f}'.rjust(x_digits + y_digits + 1)))

  # Create the stem plot
  markerline, stemlines, baseline = ax.stem(x_data, y_data, linefmt=line_color,
                                            markerfmt='o', basefmt=' ', bottom=0, label=label)
  plt.setp(stemlines, 'linewidth', stem_width)
  plt.setp(markerline, 'markersize', marker_size)

  # Set axis labels and title with specified font sizes and padding
  ax.set_xlabel(xlabel, fontsize=20, labelpad=x_label_pad)
  ax.set_ylabel(ylabel, fontsize=20, labelpad=y_label_pad)
  ax.grid(linestyle='--')
  ax.set_title(title, fontsize=24, pad=title_pad)

  # Set x and y axis limits if specified
  if x_min is not None and x_max is not None:
    ax.set_xlim(x_min, x_max)

  if y_min is not None and y_max is not None:
    ax.set_ylim(y_min, y_max)

  ax.tick_params(axis='both', direction='in', length=4, width=1,
                 colors='black', top=True, right=True, labelsize=18)

  # Display the legend if a label is provided
  if label:
    ax.legend(frameon=True, loc='best', framealpha=1, prop={'size': 16})

  return markerline, stemlines, baseline


def use_latex():
  """
  Configures Matplotlib to use LaTeX if available.
  If LaTeX is not available, uses default fonts.
  """
  try:
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "Palatino"
    })
    print("LaTeX has been enabled for text rendering.")
  except Exception:
    plt.rcParams.update({
        "text.usetex": False,
        "font.family": "sans-serif"
    })
    print("LaTeX is not available. Using default fonts.")
