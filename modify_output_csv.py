import pandas as pd

# Read the CSV files
meal_info = pd.read_csv('C:\\Users\\shaif\\Desktop\\food_demand_prediction\\supplychain\\meal_info.csv')
recipes = pd.read_csv('C:\\Users\\shaif\\Desktop\\food_demand_prediction\\supplychain\\recipes.csv')

# Merge the two DataFrames based on meal_id
merged_df = pd.merge(meal_info, recipes, left_on='meal_id', right_on='meal-id')

# Select the required columns and rename them
result_df = merged_df[['category', 'name', 'quantity']]
result_df.columns = ['category', 'ingredient', 'quantity']

# Write the result to a new CSV file
result_df.to_csv('output.csv', index=False)
