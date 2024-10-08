from django.urls import path,include
from .import views

from djadmin.views import User_List,Personal_link_Admin

urlpatterns = [
   
    path("admin_dashboard/",views.admin_dashboard,name="admin_dashboard"),
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('admin_logout/', views.admin_logout_view, name='admin_logout'),

    path('api/profiles/', User_List.as_view(), name='user-url-lists'), # class based view(Rest API)
    path('url/personal_links/<int:id>/', Personal_link_Admin.as_view(), name='personal_details'),
]