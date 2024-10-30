import pandas as pd
from datetime import datetime

# Load data from CSV
try:
    data = pd.read_csv('employees.csv')
except FileNotFoundError:
    print("Error: CSV file not found.")
else:
    # Calculate age based on the current year
    current_year = datetime.now().year
    data['Age'] = data['Дата народження'].apply(lambda x: current_year - int(x.split('-')[0]))

    # Define age categories
    age_categories = {
        'all': data,
        'younger_18': data[data['Age'] < 18],
        '18-45': data[(data['Age'] >= 18) & (data['Age'] <= 45)],
        '45-70': data[(data['Age'] > 45) & (data['Age'] <= 70)],
        'older_70': data[data['Age'] > 70]
    }

    # Save each category to a new sheet in the Excel file
    try:
        with pd.ExcelWriter('employees.xlsx', engine='openpyxl') as writer:
            for sheet_name, category_data in age_categories.items():
                category_data[['Прізвище', 'Ім’я По-батькові', 'Дата народження', 'Age']].to_excel(writer, sheet_name=sheet_name, index=False)
        print("Ok")
    except Exception as e:
        print(f"Error creating XLSX file: {e}")
