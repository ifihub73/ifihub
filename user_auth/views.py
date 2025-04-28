from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your views here.

def index(request):

    return render(request, 'user_auth/index.html')


@require_http_methods(['POST'])
def create_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not all([username, password]) or len(username.strip()) < 5 or len(password.strip()) < 6:
        return JsonResponse({'error':"invalid username or password"})
    
    
    user = User(username=username, password=password)



    if request.POST.get('type') and request.POST.get('type').strip() == 'email':
        if User.objects.filter(username=username.strip()).exists():
            return JsonResponse({'error':"user with email already exist"})
        
        try:
            user.email = username
            user.full_clean()
            user.save()
            return JsonResponse({'success':"you are registered"})
        
        except Exception as e:
            print(e)
            return JsonResponse({'error':'invalid email'})
        
    elif request.POST.get('type') and request.POST.get('type').strip() == 'phone':
        if User.objects.filter(username=username.strip()).exists():
            return JsonResponse({'error':"user with phone number already exist"})
        
        try:
            user.phone = username
            user.full_clean()
            user.save()
            return JsonResponse({'success':"you are registered"})
        
        except Exception as e:
            print(e)
            return JsonResponse({'error':'invalid phone'})
        
    else:
        return JsonResponse({'error':'invalid type'})


@require_http_methods(['POST'])
def login_user(request):  
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not all([username.strip(), password]):
        return JsonResponse({'error':'empty email or password fields'})
    
    try:
        user = User.objects.get(username=username.strip())
        print(user)
    except User.DoesNotExist:
        return JsonResponse({'error':f'invalid credentials for {username} and {password}'})
    
    if not (user.password == password):
        print(user.check_password(password))
        print(user.password)
        return JsonResponse({'error':'password does not match'})

    
    login(request, user)
    return JsonResponse({'success':'you are logged in'})


@login_required
def logout_user(request):
    logout(request)
    return JsonResponse({'success':'you are logged out'})