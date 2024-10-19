from django.shortcuts import render,HttpResponse,redirect
from .models import Short_url,People
from .seralizers import LinkSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import qrcode
import os
from django.conf import settings
from .models import Short_url, People
from rest_framework.views import APIView
from .utils import generate_hash
from django.shortcuts import get_object_or_404


from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)
# Create your views here.

# def index(request):
#     return render(request, 'user_app/edit_url.html') 

def Welcome_page(request):
    return render(request, 'user_app/index.html')  

@api_view(['GET'])
def get_links(request):
    links = Short_url.objects.all()
    serialzer = LinkSerializer(links,many=True)
    return Response(serialzer.data)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        # Check if passwords match
        if password == confirm_password:
            # Create a new People instance with hashed password
            user = People(
                username=username,
                email=email,
                password=make_password(password)  # Hashing the password
            )
            user.save()
            return redirect('login')  # Redirect to login page after successful signup

    return render(request, 'user_app/register.html')  # 


@never_cache
def login(request):
    if 'username' in request.session:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Attempt to get the user from the People model
        try:
            user = People.objects.get(email=email)
        except People.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'user_app/login.html')

        # Check if the password matches using check_password
        if user and check_password(password, user.password):
            request.session['email'] = email
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'user_app/login.html')

    return render(request, 'user_app/login.html')



def logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('login')


# Create Shortened URL API
@api_view(['POST'])
def create_shortened_url(request):
    if 'email' not in request.session:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    email = request.session['email']
    try:
        user = People.objects.get(email=email)
    except People.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    original_url = request.data.get('original_url')
    if not original_url:
        return Response({'error': 'Original URL is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the original URL already exists in the database
    if Short_url.objects.filter(original_url=original_url, user=user).exists():
        return Response({'error': 'URL already exists in the database , Try another Url'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate a unique short code
    short_code = generate_hash()

    short_url = f"http://54.252.28.90/{short_code}"  # Build the full short URL

    # Ensure the 'qr_codes/' directory exists within the media directory
    qr_code_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
    if not os.path.exists(qr_code_dir):
        os.makedirs(qr_code_dir)  # Create the directory if it doesn't exist

    # Generate and save the QR code
    qr_code_path = os.path.join(qr_code_dir, f'{short_code}.png')
    qr = qrcode.make(short_url)
    qr.save(qr_code_path)

    # Save the Short_url instance
    short_url_instance = Short_url.objects.create(
        user=user,
        original_url=original_url,
        short_code=short_code,
        short_url=short_url,  # This will now store the full short URL
        qr_code_url=f'qr_codes/{short_code}.png',
        created_at=timezone.now()
    )
    
    # Increment the number of shortened links for the user
    user.Number_of_shorterned_links += 1  # Increment the counter
    user.save()  # Save the updated user instance
    # Serialize the response
    serializer = LinkSerializer(short_url_instance)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



def redirect_to_original_url(request, short_code):
    try:
        # Retrieve the Short_url instance using the short_code
        short_url_instance = Short_url.objects.get(short_code=short_code)
        
        # Increment the visit count
        short_url_instance.visit_count += 1
        short_url_instance.save()
        
        # Get the original URL
        original_url = short_url_instance.original_url
        
        return redirect(original_url)
    except Short_url.DoesNotExist:
        return HttpResponse('URL not found', status=404)
    


class View_Person_url_Details(APIView):
    def get(self, request, *args, **kwargs):
        # Get the email from session
        email = request.session.get('email')

        if not email:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Get the user based on the email
            user = People.objects.get(email=email)
        except People.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get all short URLs for the user
        urls = Short_url.objects.filter(user=user)
        
        if not urls.exists():
            return Response({'message': 'No URLs found for this user'}, status=status.HTTP_200_OK)

        # Serialize the queryset and return the data
        serializer = LinkSerializer(urls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Edit_Person_url_Details(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')  # Get the URL ID from the URL parameters
        try:
            obj = Short_url.objects.get(id=id)  # Fetch the URL object by ID
        except Short_url.DoesNotExist:
            return Response({'error': 'URL not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LinkSerializer(obj)  # Serialize the object data

        return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data as JSON
    
    def put(self, request, id, *args, **kwargs):
        # Get the URL object by ID
        short_url_obj = get_object_or_404(Short_url, id=id)

        # Update the object with new data
        serializer = LinkSerializer(short_url_obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  # Save the updated URL

            # Generate the response with the updated short URL and QR code URL
            response_data = {
                'original_url': serializer.data['original_url'],
                'short_code': short_url_obj.short_code,  # Make sure this is updated
                'short_url': short_url_obj.short_url,    # Return the updated short URL
                'qr_code_url': short_url_obj.qr_code_url.url if short_url_obj.qr_code_url else None  # Use qr_code_url
            }

            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        short_url = get_object_or_404(Short_url, id=id)
        short_url.delete()
        return Response({"message": "URL deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

    # Debugging
    # def put(self, request, id, *args, **kwargs):
    #     try:
    #         # Get the URL object by ID
    #         short_url_obj = get_object_or_404(Short_url, id=id)
            
    #         # Log the request data
    #         logger.info(f"Received PUT request with data: {request.data}")

    #         # Update the object with new data
    #         serializer = LinkSerializer(short_url_obj, data=request.data, partial=True)

    #         if serializer.is_valid():
    #             serializer.save()

    #             # Generate the response with the updated short URL and QR code path
    #             response_data = {
    #                 'original_url': serializer.data['original_url'],
    #                 'short_url': short_url_obj.short_url,    # Updated short URL
    #                 'qr_code': short_url_obj.qr_code.url if short_url_obj.qr_code else None  # QR code path
    #             }

    #             logger.info(f"Successfully updated URL: {response_data}")
    #             return Response(response_data, status=status.HTTP_200_OK)
            
    #         # Log any validation errors
    #         logger.error(f"Validation failed: {serializer.errors}")
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #     except Exception as e:
    #         # Log the exception for debugging
    #         logger.error(f"Error occurred while updating URL: {str(e)}")
    #         return JsonResponse({'error': 'Internal Server Error', 'details': str(e)}, status=500)
    

    

   
        
    
def edit(request, id):  # Add 'id' as a parameter to the function
    if 'email' in request.session:
        email = request.session["email"]
        try:
            person = People.objects.get(email=email)
            # Fetch the original URL using the API
            short_url = Short_url.objects.get(id=id)
            context = {
                "person_name": person.username,
                "url_id": id,  # Pass the 'id' to the context so it can be used in the template
                "original_url": short_url.original_url  # Pass the original URL to pre-fill the form
            }
            return render(request, 'user_app/edit_url.html', context)
        except (People.DoesNotExist, Short_url.DoesNotExist):
            # Handle case where the user or the URL does not exist
            return redirect('login')
    return redirect('login')

@never_cache
def home(request):
    if 'email' in request.session:
        email = request.session["email"]
        try:
            person = People.objects.get(email=email)
            context = {"person_name": person.username,}
            return render(request, 'user_app/home.html', context)
        except People.DoesNotExist:
            # Handle case where the user does not exist
            return redirect('login')
    return redirect('login')