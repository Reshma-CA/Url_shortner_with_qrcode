
from django.urls import path,include
from .import views

urlpatterns = [
   
    path("",views.home,name="home"),
    path("register/",views.register,name="register"),
    path("login/",views.login,name="login"),
    path('logout/', views.logout, name='logout'),

    path('api/shorten-url/', views.create_shortened_url, name='create_shortened_url'),
    path('<str:short_code>/', views.redirect_to_original_url, name='redirect_to_original_url'),
     
]
    # path("api/link/",views.get_links,name="get_links"),

