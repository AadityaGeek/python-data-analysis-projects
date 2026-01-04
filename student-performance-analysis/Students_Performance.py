# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('data\\StudentsPerformance.csv')

# Initial data exploration
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())
print(df.isnull().sum()) # If output is all zeros, there are no missing values else it shows count of missing values per column
print(df.describe())

# Create a new column for average score
df["average_score"] = (df["math score"] + df["reading score"] + df["writing score"]) / 3

# Basic analysis
low_performancers = df[df["average_score"] < 40]
print(low_performancers.head())
print(low_performancers.shape)

# Average scores based on test preparation course
print("Average scores based on test preparation course:")
prep_avg = df.groupby("test preparation course")["average_score"].mean()
print(prep_avg)

# Numpy conversion
math_scores = df["math score"].to_numpy()
reading_scores = df["reading score"].to_numpy()
writing_scores = df["writing score"].to_numpy()

print("Maths Average: ",np.mean(math_scores))
print("Reading Average: ",np.mean(reading_scores))
print("Writing Average: ",np.mean(writing_scores))

overall_average = np.mean(df["average_score"].to_numpy())
print("Overall Average Score: ", overall_average)


# Data Visualization
subjects = ['Maths', 'Reading', 'Writing']
average_scores = [
    np.mean(math_scores), 
    np.mean(reading_scores), 
    np.mean(writing_scores)
    ]

# Bar plot for average scores by subject
plt.figure()    # Create a new figure
plt.bar(subjects, average_scores, width=0.5)
plt.xlabel('Subjects', fontsize=12, weight='bold')
plt.ylabel('Average Scores', fontsize=12, weight='bold')
plt.title('Average Scores by Subject')
plt.ylim(0, 100)  # Set y-axis limits
plt.yticks(range(0, 101, 10))
plt.gca().set_axisbelow(True)   # Ensure grid lines are below bars
plt.grid(axis='y')
plt.show()


# Bar plot for average scores by test preparation course
plt.figure()
preparation = ["Completed", "Not Completed"]
plt.bar(prep_avg.index, prep_avg.values, width=0.4)
plt.xlabel('Test Preparation Course', fontsize=12, weight='bold')
plt.ylabel('Average Scores', fontsize=12, weight='bold')
plt.title('Impact of Test Preparation Course on Average Scores')
plt.xticks(prep_avg.index, preparation)
plt.ylim(0, 100)
plt.yticks(range(0, 101, 10))
plt.gca().set_axisbelow(True)
plt.grid(axis='y')
plt.show()


# Histogram for distribution of average scores
bins = range(0, 101, 10)
plt.figure()
plt.hist(df['average_score'], bins=bins)
plt.xlabel('Average Score', fontsize=12, weight='bold')
plt.ylabel('Number of Students', fontsize=12, weight='bold')
plt.title('Distribution of Average Scores')
plt.xticks(np.arange(0, 101, 10))
plt.yticks(np.arange(0, 301, 50))
plt.gca().set_axisbelow(True)
plt.grid(axis='y')
plt.show()