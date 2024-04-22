import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

# # Iterate through rows
# for index, row in df.iterrows():
#     print(f"Index: {index}, A: {row['A']}, B: {row['B']}, C: {row['C']}")

# Iterate through rows
for row in df.itertuples():
    print(f"Index: {row.Index}, A: {row.A}, B: {row.B}, C: {row.C}")
