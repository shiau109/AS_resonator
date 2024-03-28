import numpy as np

# Example array
arr = np.array([[1, 20, 3], [4, 5, 60]])

# Value to compare against
threshold = 10

# Modify elements that are greater than the threshold
arr[arr > threshold] = threshold

print(arr)
