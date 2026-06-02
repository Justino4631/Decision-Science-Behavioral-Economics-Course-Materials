import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

ROLLS = 10_000

def plot_die_roll_averages(num_die: int = 5) -> None:
    plt.clf() 
    
    die_avgs = []

    for roll in range(ROLLS):
        die_avgs.append(sum(random.randint(1, 6) for _ in range(num_die)) / num_die)

    plt.hist(die_avgs, bins=24, edgecolor="black", density=True, alpha=0.6, color='blue')

    mean, std = np.mean(die_avgs), np.std(die_avgs)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 10_000)
    p = stats.norm.pdf(x, mean, std)

    plt.plot(x, p, 'r-', linewidth=2, label=f'Normal Dist ($\mu$={mean:.2f}, $\sigma$={std:.2f})')

    plt.ylabel("Density")
    plt.xlabel(f"Avg. Die Values for {num_die} die")

    plt.legend()
    plt.show()

plot_die_roll_averages(1)
plot_die_roll_averages(2)
plot_die_roll_averages(5)
plot_die_roll_averages(20)
plot_die_roll_averages(100)
plot_die_roll_averages(1000)