import pandas as pd
import matplotlib.pyplot as plt

# Load your metrics file
df = pd.read_csv("metrics.csv")

fig, ax1 = plt.subplots(figsize=(9,5))

# Left y-axis: safe creatures
ax1.plot(df["generation"], df["num_reproducers"], color="tab:green", label="Safe creatures")
ax1.set_xlabel("Generation")
ax1.set_ylabel("Safe creatures (num_reproducers)", color="tab:green")
ax1.tick_params(axis="y", labelcolor="tab:green")

# Right y-axis: behavioral entropy
ax2 = ax1.twinx()
ax2.plot(df["generation"], df["behavioral_entropy"], color="tab:orange", label="Behavioral entropy")
ax2.set_ylabel("Behavioral entropy", color="tab:orange")
ax2.tick_params(axis="y", labelcolor="tab:orange")

# Title and grid
plt.title("Safe creatures vs. Behavioral entropy over generations")
fig.tight_layout()
plt.grid(True, linestyle="--", alpha=0.6)

plt.show()
