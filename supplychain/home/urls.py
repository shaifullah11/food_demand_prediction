from django.urls import path
from .import views

urlpatterns=[
    path("",views.home,name="home"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login,name="login"),
    path("order/",views.order,name="order"),
    path("main/",views.main,name="main"),
    path("ingred/",views.ingred,name="ingred"),
    path("cost/",views.cost,name="cost"),
  

]