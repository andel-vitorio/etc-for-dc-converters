import numpy as np


def show_matrix(matrix, name='ans', decimal_places=2, scientific_notation=True):
  """
  Displays a matrix with the specified number of decimal places.

  Parameters:
  ---
  - matrix: numpy.ndarray, the matrix to be displayed.
  - name: str, the name to be used in the display header (default is 'ans').
  - decimal_places: int, the number of decimal places to display (default is 2).
  - scientific_notation: bool, if True, uses scientific notation; otherwise, uses fixed-point notation (default is True).
  """
  # Define the format pattern based on whether scientific notation is used
  pattern = f"{{:.{decimal_places}{'e' if scientific_notation else 'f'}}}"

  def format_elem(elem):
    """
    Formats a single matrix element according to the defined pattern.

    Parameters:
    - elem: the element to be formatted.

    Returns:
    - str: the formatted element.
    """
    return pattern.format(elem)

  # Calculate the maximum width required for each column
  col_widths = [max(map(len, map(format_elem, col))) for col in matrix.T]

  print(f"{name} =")  # Print the matrix name
  # Calculate the spacing for the matrix border
  nspaces = sum(col_widths) + 2 * matrix.shape[1]

  # Print the top border of the matrix
  print("    ┌" + " " * nspaces + "┐")

  # Print each row of the matrix
  for row in matrix:
    # Format each element of the row and right-align according to column width
    formatted_row = "  ".join(format_elem(e).rjust(w)
                              for e, w in zip(row, col_widths))
    print(f"    │ {formatted_row} │")

  # Print the bottom border of the matrix
  print("    └" + " " * nspaces + "┘\n")