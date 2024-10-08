
from django.urls import path,include
from .import views
from userapp.views import View_Person_url_Details,Edit_Person_url_Details

urlpatterns = [

    path("",views.Welcome_page,name="welcome"),
   
    path("home/",views.home,name="home"),
    path("register/",views.register,name="register"),
    path("login/",views.login,name="login"),
    path('logout/', views.logout, name='logout'),
   

    path('api/shorten-url/', views.create_shortened_url, name='create_shortened_url'),
    path('<str:short_code>/', views.redirect_to_original_url, name='redirect_to_original_url'),

    path('api/user-urls/', View_Person_url_Details.as_view(), name='user-url-details'), # class based view(Rest API)
    path('api/delete/<int:id>/', Edit_Person_url_Details.as_view(), name='delete_shortened_url'),
    path('api/edit/<int:id>/', Edit_Person_url_Details.as_view()),  # API for fetch/update URL
    path('url/edit/<int:id>/', views.edit, name='edit'),  # Template rendering route
   
    # path('url/edit/', views.edit, name='edit'),
     
]
    # path("api/link/",views.get_links,name="get_links"),

