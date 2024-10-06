from django.shortcuts import render,HttpResponse

# Create your views here.
def admin_dashboard(request):
    return HttpResponse("Welcome to admin dashboard")