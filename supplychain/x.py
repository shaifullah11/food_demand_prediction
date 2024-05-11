import pandas as pd

train=pd.read_csv(r"C:\Users\shaif\Documents\supplychain\supplychain\train.csv")
print(train['meal_id'].unique())