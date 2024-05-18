from django.shortcuts import render,redirect
from .models import UserModel,Account,Product,ProductIngredient,Ingredient
from django.db.models import Q
from django.http import HttpResponse
import pandas as pd
import numpy as np
import keras


train = pd.read_csv(r'C:\Users\shaif\Documents\supplychain\supplychain\train.csv')
# Create your views here.
def home(request):
    return render(request,"home.html")

def signup(request,method=['GET','POST']):
    if request.method=='POST':
        username=request.POST.get("username")
        passw1=request.POST.get("passw1")
        passw2=request.POST.get("passw2")
        email=request.POST.get("email")
        acc=request.POST.get("acc")
        address=request.POST.get("address")
        q=UserModel.objects.filter(username=username)
       
        msg="User already exists"
        if(q):
            return render(request,"signup.html",{"msg":msg})
        else:
            
            UserModel.objects.create(username=username,password=passw1,email=email,acc_number=acc,address=address)
            q=UserModel.objects.get(username=username)
            Account.objects.create(user=q,balance=1000)
            return render(request,"login.html")

    return render(request,"signup.html")

def login(request,method=['GET','POST']):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        q=UserModel.objects.filter(Q(username=username,password=password))
        msg="User not found"
        if(q):
            
            request.session["username"]=q[0].username
            return redirect("/main/")
        else:
            return render(request,"login.html",{"msg":msg})
    return render(request,"login.html")



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


def predict_orders(user_input):
    # Load the dataset and preprocess
    data = pd.read_csv(r'C:\Users\shaif\Documents\supplychain\supplychain\train.csv')
    center = pd.read_csv(r'C:\Users\shaif\Documents\supplychain\supplychain\fulfilment_center_info.csv')
    meal = pd.read_csv(r'C:\Users\shaif\Documents\supplychain\supplychain\meal_info.csv')
    test = pd.read_csv(r'C:\Users\shaif\Documents\supplychain\supplychain\test.csv')

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

    sc = StandardScaler()
    cat = data.drop(['checkout_price', 'base_price'], axis=1)
    num = data[['checkout_price', 'base_price']]
    scal = pd.DataFrame(sc.fit_transform(num), columns=num.columns)


    with open(r"C:\Users\shaif\Documents\supplychain\supplychain\model.h5", 'rb') as file: 
        gru_model = pickle.load(file)
    # Preprocess user input
    user_input_df = pd.DataFrame(user_input, index=[0])
    user_input_df['discount amount'] = user_input_df['base_price'] - user_input_df['checkout_price']
    user_input_df['center_id'] = user_input_df['center_id'].astype('object')
    user_input_df['meal_id'] = user_input_df['meal_id'].astype('object')
    
    # Scale numerical features
    user_input_scaled = pd.DataFrame(sc.transform(user_input_df[['checkout_price', 'base_price']]), 
                                     columns=['checkout_price', 'base_price'])
    
    # Concatenate scaled numerical features with categorical features
    user_input_processed = pd.concat([user_input_scaled,user_input_df[['week', 'center_id', 'meal_id', 'emailer_for_promotion', 'homepage_featured']]], axis=1)
    
    # Predict orders
    predicted_orders_log = gru_model.predict(user_input_processed)
    predicted_orders = np.exp(predicted_orders_log)
    
    return int(predicted_orders)

def order(request, method=['GET', 'POST']):

    msg = ""
    
    if request.method == "POST":
        week = request.POST.get("week")
        c_id = request.POST.get("c_id") 
        m_id = request.POST.get("m_id")
        c_price = request.POST.get("c_price")
        b_price = request.POST.get("b_price")
        e_p = request.POST.get("e_p") 
        h_f = request.POST.get("h_pk") 
        
        user_input = {
            'week': int(week),
            'center_id': int(c_id),
            'meal_id': int(m_id),
            'checkout_price': int(c_price),
            'base_price': int(b_price),
            'emailer_for_promotion': int(e_p),
            'homepage_featured': int(h_f)
        }

        print(user_input)



        # Filter products based on meal ID
        q = Product.objects.filter(mealid=int(m_id))

        if q.exists():  # Check if any products exist for the given meal ID
            product = q.first()  # Get the first product
            # Convert the user input to a dataframe
            predictions = predict_orders(user_input)
            print(predictions)

            return render(request, "result.html", {"result": predictions, "q": product})
        else:
            msg = "Invalid Meal ID"
            return render(request, "main.html", {"msg": msg})
        
def ingred(request):
    cost=0
    order=request.GET.get("orders")
    p_id=request.GET.get("product_id")
    print(p_id)
    order=int(float(order))
    print(type(order))
    p=Product.objects.get(mealid=p_id)
    prod=ProductIngredient.objects.filter(product=p)
    k=ProductIngredient.objects.filter(product=p)
    for x in k:
        cost += x.ingredient.cost
    cost = cost*order
    return render(request,"ingredients.html",{"prod":prod,"order":order,"cost":cost})

def main(request):
    return render(request,"main.html")
 
def logout(request):
    del request.session["username"]
    return render(request,"home.html")

def cost(request):
    cost=request.GET.get("cost")
    order=request.GET.get("order")
    return render(request,"cost.html",{"cost":cost,"order":order})


