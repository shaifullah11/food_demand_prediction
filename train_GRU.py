import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential, load_model
from keras.layers import GRU, Dense
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error
from math import sqrt
import pickle


# Load the dataset and preprocess
data = pd.read_csv(r'D:\My projects\supplychain bigdata\supplychain\train.csv')
center = pd.read_csv(r'D:\My projects\supplychain bigdata\fulfilment_center_info.csv')
meal = pd.read_csv(r'D:\My projects\supplychain bigdata\meal_info.csv')
test = pd.read_csv(r'D:\My projects\supplychain bigdata\test.csv')

# Merge datasets
data = pd.concat([data, test], axis=0)
data = data.merge(center, on='center_id', how='left')
data = data.merge(meal, on='meal_id', how='left')

# Discount Amount
data['discount amount'] = data['base_price'] - data['checkout_price']
data = data.drop(['center_type', 'category', 'cuisine'], axis=1)

# Train-test split
train = data[data['week'].isin(range(1, 146))]
test = data[data['week'].isin(range(146, 156))]

# Feature engineering
data['center_id'] = data['center_id'].astype('object')
data['meal_id'] = data['meal_id'].astype('object')
data['region_code'] = data['region_code'].astype('object')

scaler = StandardScaler()
cat = data.drop(['checkout_price', 'base_price', 'discount amount'], axis=1)
num = data[['checkout_price', 'base_price', 'discount amount']]
scal = pd.DataFrame(scaler.fit_transform(num), columns=num.columns)
datas = pd.concat([scal, cat], axis=1)

train = datas[datas['week'].isin(range(1, 136))]
test = datas[datas['week'].isin(range(136, 156))]

# Prepare data for modeling
X_train = train.drop(['id', 'num_orders', 'city_code', 'region_code', 'op_area', 'discount amount'], axis=1)
y_train = np.log(train['num_orders'])

X_test = test.drop(['id', 'num_orders', 'city_code', 'region_code', 'op_area', 'discount amount'], axis=1)
y_test = np.log(test['num_orders'])

# Reshape input data for GRU
X_train_gru = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1])).astype('float32')
X_test_gru = X_test.values.reshape((X_test.shape[0], 1, X_test.shape[1])).astype('float32')

# Define the GRU model
model = Sequential()
model.add(GRU(units=50, input_shape=(X_train_gru.shape[1], X_train_gru.shape[2])))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# Fit the model
history = model.fit(X_train_gru, y_train, epochs=10, batch_size=64, validation_data=(X_test_gru, y_test), verbose=2, shuffle=False)

# Save the model
model.save('gru_model.h5')

