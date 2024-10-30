import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load data
try:
    data = pd.read_csv('employees.csv')
except FileNotFoundError:
    print("Error: CSV file not found.")
else:
    print("Ok")

    # Gender distribution
    gender_counts = data['Стать'].value_counts()
    print("Gender distribution:", gender_counts.to_dict())  # Convert Series to dict for cleaner output
    gender_counts.plot(kind='bar', title="Gender Distribution")
    plt.savefig('gender_distribution.png')
    plt.close()

    # Ensure 'Дата народження' is in a recognizable date format
    try:
        data['Дата народження'] = pd.to_datetime(data['Дата народження'], errors='raise')
    except Exception as e:
        print("Error in date parsing:", e)
    
    # Calculate age based on birth date
    current_year = datetime.now().year
    data['Age'] = data['Дата народження'].apply(lambda x: current_year - x.year)

    # Define age categories
    age_bins = [0, 18, 45, 70, 100]
    age_labels = ["<18", "18-45", "45-70", ">70"]
    data['Age Group'] = pd.cut(data['Age'], bins=age_bins, labels=age_labels)

    # Age group distribution
    age_group_counts = data['Age Group'].value_counts()
    print("Age group distribution:", age_group_counts.to_dict())  # Convert Series to dict for cleaner output
    age_group_counts.plot(kind='bar', title="Age Group Distribution")
    plt.savefig('age_group_distribution.png')
    plt.close()

    # Gender distribution by age group
    age_gender_counts = data.groupby(['Age Group', 'Стать'], observed=True).size().unstack()
    print("Gender by age group:\n", age_gender_counts)  # Table format is already readable
    age_gender_counts.plot(kind='bar', stacked=True, title="Gender by Age Group")
    plt.savefig('gender_by_age_group.png')
    plt.close()
