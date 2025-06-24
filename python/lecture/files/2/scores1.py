# Averages three numbers using a list and a loop

from cs50 import get_int

# Get scores
scores = []
for i in range(3):
    score = get_int("Score: ")
    # scores.append(score)
    scores += [score] ## is like append !!!!!

# Print average
average = sum(scores) / len(scores)
print(f"Average: {average}")
