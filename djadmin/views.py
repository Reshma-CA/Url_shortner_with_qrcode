from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from userapp.models import Short_url,People
from rest_framework import generics
from rest_framework.views import APIView
from .seralizers import Url_LinkSerializer,User_Serializer

# Create your views here.
def admin_dashboard(request):
     return render(request, 'djadmin/dashboard.html')

@never_cache
def admin_login_view(request):
    if 'username' in request.session:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Attempt to get the user from the People model
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'djadmin/admin_login.html')

        # Check if the password matches using check_password
        if user and check_password(password, user.password):
            request.session['username'] = username
            return redirect('admin_dashboard') 
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'djadmin/admin_login.html')
    return render(request, 'djadmin/admin_login.html')

def admin_logout_view(request):
    if 'username' in request.session:
        request.session.flush()
    return render(request, 'djadmin/admin_login.html')

class User_List(generics.ListAPIView):
    queryset = People.objects.all()
    serializer_class = User_Serializer


class Personal_link_Admin(APIView):
    def get(self, request, id):
        try:
            user = People.objects.get(id=id)
            short_urls = Short_url.objects.filter(user=user)
            serializer = Url_LinkSerializer(short_urls, many=True)

            # Render the template and pass the user and serializer data
            return render(request, 'djadmin/personal_link.html', {
                'user': user,
                'short_urls': serializer.data,
            })
        except People.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
    

