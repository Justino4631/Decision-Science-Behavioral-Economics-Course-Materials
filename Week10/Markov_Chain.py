import numpy as np
import random

# Sample text for Markov chain
with open("Week10/Pride_And_Prejudice.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Tokenize the text
words = text.split()
word_count = len(set(words))

# Create a transition matrix
transition_matrix = np.zeros((word_count, word_count))

for i in range(word_count - 1):
    current_word_idx = words.index(words[i])
    next_word_idx = words.index(words[i + 1])
    transition_matrix[current_word_idx][next_word_idx] += 1

# Normalize the transition matrix
for i in range(word_count):
    row_sum = np.sum(transition_matrix[i])
    if row_sum > 0:
        transition_matrix[i] /= row_sum

# print(transition_matrix[0])
# t = transition_matrix.tolist()
# print(f"    {text.replace(".", "")}")

# for r in t:
#     print(words[t.index(r)], r)

# quit()

# Function to generate text
def generate_text(start_word, length=200):
    global transition_matrix
    current_word = start_word
    generated_text = [current_word]

    for _ in range(length - 1):
        current_word_idx = words.index(current_word)
        next_word_idx = np.random.choice(range(word_count), p=transition_matrix[current_word_idx])
        current_word = words[next_word_idx]
        generated_text.append(current_word)

    return ' '.join(generated_text)

print(generate_text('Catherine'))