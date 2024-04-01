import numpy as np

# Start with an empty array (shape (0, n) for n columns if appending rows, or (m, 0) for m rows if appending columns)
arr = np.empty((0, 3), int)

# Append rows to the array
arr = np.append(arr, [[1, 2, 3]], axis=0)
arr = np.append(arr, [[4, 5, 6]], axis=0)

print(arr)