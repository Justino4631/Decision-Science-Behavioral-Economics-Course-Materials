"""
A game about statistics inspired by 'Guess the Correlation'

author: Justin Baratta
date: 6/2/2026
version: 3.13
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import scipy.stats as stats
import math

GTC = {

}

def generate_GTC_question(r: float, num_pts:int = 200) -> None:
    mean_x_y = [0, 0]
    covariance = [[1, r], [r, 1]]

    data = np.random.multivariate_normal(mean_x_y, covariance, num_pts)
    
    x = data[:, 0].tolist()
    y = data[:, 1].tolist()
    data = (tuple(x), tuple(y))

    GTC[data] = r
    return

DIST = {

}

def generate_DIST_question(dist:str, num_pts:int = 200) -> None:
    if dist not in ["norm", "log", "exp", "quad", "logistic", "trig"]:
        raise ValueError("Inputted distribution not in acceptable distributions")
    
    match dist:
        case "norm":
            mean, var = 0, 1
            std = math.sqrt(var)

            x = np.linspace(mean - 3*std, mean + 3*std, num_pts)
            y = stats.norm.pdf(x, 0, 1)
            noise = np.random.normal(loc=0, scale=random.uniform(0.03, 0.07), size=len(x))
            y += noise

        case "log":
            base = random.randint(2, 10)
            x = np.linspace(0.1, 5, num_pts)
            y = np.log(x) / np.log(base)
            noise = np.random.normal(loc=0, scale=random.uniform(0.3, 0.5), size=len(x))
            y += noise

        case "exp":
            if random.choice([0, 1]) == 0:
                base = random.randint(2, 5)
                x = np.linspace(0, 3, num_pts)
                y = np.power(base, x)
                scale = np.max(y)*0.075
            else:
                base = 0.1*random.randint(5, 8)
                x = np.linspace(0, 7, num_pts*2)
                y = np.power(base, x)
                scale = 0.075

            noise = np.random.normal(loc=0, scale=scale, size=len(x))
            y += noise

        case "quad":
            x = np.linspace(-1, 4, num_pts*2)
            y = np.square(x)
            noise = np.random.normal(loc=0, scale=np.max(y)*0.1, size=len(x))
            y += noise

        case "logistic":
            x = np.linspace(-5, 5, num_pts*2)
            y = stats.logistic.cdf(x)
            noise = np.random.normal(loc=0, scale=random.uniform(0.1, 0.2), size=len(x))
            y += noise
        
        case "trig":
            x = np.linspace(-3, 3, num_pts)
            func = random.choice([0, 1, 2])
            if func == 0:
                y = np.sin(x)
            elif func == 1:
                y = np.cos(x)
            else:
                y = np.tan(x)

            noise = np.random.normal(loc=0, scale=random.uniform(0.1, 0.2), size=len(x))
            y += noise

    DIST[((tuple(x), tuple(y)))] = dist

MCQs = {
    "When converting from a scatterplot to z-scores, what point does the z-score regression line ALWAYS contain?": ["The minimum", "The maximum", "The mean (correct)", "The median"],
    "What theorem states that, given enough data and the correct circumstances, the distribution of data will follow a normal distribution?": ["Fermat's Last Theorem", "The Central Limit Theorem", "Euler's Normality Postulate", "The Normal Distribution Theorem"],
    "What percentage of data is contained within 3 standard deviations of a mean given a perfect normal distribution?": [68, 95, 99.5, 00.7],
    
}

# generate_DIST_question("trig")
# coordinates = list(DIST.keys())[0]
# x, y = coordinates[0], coordinates[1]
# plt.scatter(x, y, alpha=0.6, edgecolor="none", s=15, color='blue')
# plt.xlabel("X")
# plt.ylabel("Y")
# plt.grid(True, linestyle='--', alpha=0.5)
# plt.show()

# random_rs = [round(random.uniform(-1, 1), 2) for _ in range(25)]
# for r in random_rs:
#     generate_GTC_question(r=r, num_pts=100)

# correct = 0
# for data in list(GTC.keys())[:25]:
#     plt.scatter(data[0], data[1], color="blue", marker="o", alpha=0.6)
#     plt.grid(True)
#     plt.xlabel("X")
#     plt.ylabel("Y")
#     plt.ion()
#     plt.show()

#     guessed_r = float(input("What is the correlation (r) for this scatterplot? "))
#     if abs(guessed_r - GTC[data]) <= 0.05:
#         print(f"Correct! (The true correlation was {GTC[data]})\n")
#         correct += 1
#     else:
#         print(f"Incorrect! (The true correlation was {GTC[data]})\n")
#     plt.close()
# print(f"\nYou got {correct} correct out of 25 GTC!")