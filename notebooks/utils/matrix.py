import numpy as np


def show_matrix(matrix, name='ans', decimal_places=2, scientific_notation=True):
  """
  Apresenta uma matriz com a quantidade de casas decimais desejadas.

  Parâmetros:
  ---
  - matrix: numpy.ndarray, a matriz a ser apresentada.
  - decimal_places: int, o número de casas decimais desejadas (padrão é 2).
  - scientific_notation: bool, se True, utiliza notação científica.
  """
  pattern = f"{{:.{decimal_places}{'e' if scientific_notation else 'f'}}}"

  def format_elem(elem):
    return pattern.format(elem)

  col_widths = [max(map(len, map(format_elem, col))) for col in matrix.T]

  print(f"{name} =")
  nspaces = sum(col_widths) + 2 * matrix.shape[1]

  print("    ┌" + " " * nspaces + "┐")
  for row in matrix:
    formatted_row = "  ".join(format_elem(e).rjust(w)
                              for e, w in zip(row, col_widths))
    print(f"    │ {formatted_row} │")
  print("    └" + " " * nspaces + "┘\n")
