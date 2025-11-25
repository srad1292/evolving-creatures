import pandas as pd
import matplotlib.pyplot as plt

# Load your metrics file
df = pd.read_csv("metrics.csv")

# Plot right_half vs generation
plt.figure(figsize=(8,5))
plt.plot(df["generation"], df["num_reproducers"], marker="o", color="tab:green", label="Safe creatures")

plt.xlabel("Generation")
plt.ylabel("Number of safe creatures")
plt.title("Safe creatures over generations")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.show()
