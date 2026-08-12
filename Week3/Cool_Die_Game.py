import matplotlib.pyplot as plt
import numpy as np

def calculate_avg_die_rolls(num_dice: int, num_simulations: int = 100_000):
    rolls = np.random.randint(1, 7, size=(num_simulations, num_dice))
    return np.mean(rolls, axis=1)

def plot_histogram(averages, num_dice):
    plt.figure(figsize=(8, 5))
    plt.hist(averages, bins=30, density=True, edgecolor='black', alpha=0.75, color='skyblue')
    plt.title(f"Number of Dice per Roll: {num_dice}")
    plt.xlabel("Average Roll Value")
    plt.ylabel("Probability Density")
    plt.xlim(1, 6)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def main():
    while True:
        user_input = input("Enter number of dice (or 'q' to quit): ")
        if user_input.lower() == 'q':
            break
        
        if user_input.isdigit() and int(user_input) > 0:
            num_dice = int(user_input)
            averages = calculate_avg_die_rolls(num_dice)
            plot_histogram(averages, num_dice)
        else:
            print("Please enter a valid positive integer.")

if __name__ == "__main__":
    main()