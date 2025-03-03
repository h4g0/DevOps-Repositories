import math

# Given values
N = 200023  # Population size
n = 197410  # Sample size
p = n / N  # Sample proportion (assuming all are positive cases)
Z = 1.96  # Z-score for 95% confidence level

# Standard Error (SE)
SE = math.sqrt((p * (1 - p)) / n)

# Finite Population Correction (FPC)
FPC = math.sqrt((N - n) / (N - 1))

# Margin of Error (E)
E = Z * SE * FPC

# Confidence Interval (CI)
CI_lower = (p - E) * 100  # Convert to percentage
CI_upper = (p + E) * 100  # Convert to percentage

# Margin of Error as percentage
E_percentage = E * 100  # Convert to percentage

# Print results rounded to 1 decimal
print(f"Sample Proportion (p): {p * 100:.2f}%")
print(f"Standard Error (SE): {SE * 100:.2f}%")
print(f"Finite Population Correction (FPC): {FPC:.2f}")
print(f"Margin of Error (E): {E_percentage:.2f}%")
print(f"95% Confidence Interval: ({CI_lower:.2f}%, {CI_upper:.2f}%)")
