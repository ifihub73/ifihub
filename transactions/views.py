from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import EditorRequest
# Create your views here.

#verify user home
def verify_home(request):
    user = request.user
    data= {}
    if not user.is_authenticated:
        data['error'] = 'UnAuthorised Request'
        return render(request, 'transactions/index.html', data)
    
    if user.is_verified:
        data['error'] = 'You Are Already Verified'
        return render(request, 'transactions/index.html', data)
    
    if user.first_name.strip() != '':
        data['profile'] = True
    
    data.update({'error':''})
    return render(request, 'transactions/index.html', data)

#save profile data
@require_http_methods(['POST'])
def save_profile(request):
    first_name = request.POST.get('firstName')
    last_name = request.POST.get('lastName')

    if not all([first_name, last_name]) or (len(first_name.strip()) < 2 or last_name.strip() == ''):
        return JsonResponse({'error':'all fields must be provided'})
    
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({'error':'UnAuthorized Request'})
    
    if user.first_name.strip() != '':
        return JsonResponse({'error':'invalid request'})

    
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return JsonResponse({'success':'successful'})

#send verify question
import random
def send_question(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error':'UnAuthorized Request'})
    
    if user.first_name.strip() == '':
        return JsonResponse({'error':'invalid request'})
    

    num1 = random.randint(1,10)
    num2 = random.randint(1,10)
    ops = random.choice(['+','-','*',])

    qs = f"{num1} {ops} {num2}"

    ans = eval(qs)
    request.session['answer'] = ans
    return JsonResponse({'success':'successful', 'question':qs})

#submit answer
@require_http_methods(['POST'])
def submit_answer(request):
     user = request.user
     if not user.is_authenticated:
        return JsonResponse({'error':'UnAuthorized Request'})
    
     if user.first_name.strip() == '':
        return JsonResponse({'error':'invalid request'})
     
     result = request.POST.get('answer')
     if not result:
         return JsonResponse({'error':'no data received'})
     
     try:
         submitted = int(result)
     except:
         return JsonResponse({'error':'invalid input'})
     
     system = int(request.session['answer'])
     if system != submitted:
         return JsonResponse({'error':'incorrect answer'})
     
     user.is_verified = True
     user.save()
     return JsonResponse({'success':'successful', 'result':'correct! you are verified'})
         
         
# editor request
def editor_request_home(request):
    user = request.user
    data = {}
    if not user.is_authenticated:
        data.update({'error':'AunAuthorized Request'})
        return render(request, 'transactions/editorRequestHome.html', data)

    
    if not user.is_verified:
        data.update({'error':'Your Account Is Not Verified Yet', 'verify':True})
        return render(request, 'transactions/editorRequestHome.html', data)
    
    if user.is_editor:
        data.update({'error':'You Are Already An Editor'})
        return render(request, 'transactions/editorRequestHome.html', data)
    
    if EditorRequest.objects.filter(user__id=user.id).exists():
        data.update({'error':'You Already have a pending submission'})
        return render(request, 'transactions/editorRequestHome.html', data)
    
    return render(request, 'transactions/editorRequestHome.html', data)

#submit editor request submission
require_http_methods(['POST'])
def submit_request(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error':'UnAuthorized Request'})
    
    if not user.is_verified:
        return JsonResponse({'error':'UnAuthorized Request'})
    
    if user.is_editor:
        return JsonResponse({'error':'You are already an editor'})
    
    if EditorRequest.objects.filter(user__pk=user.pk).exists():
        req = EditorRequest.objects.get(user__pk=user.pk)
        if not req.approved:
            return JsonResponse({'error':'Admins are Still Reviewing Your Request'})
        if req.approved:
            return JsonResponse({'error':'Your have been approved'})
        
        
    text = request.POST.get('text')
    submission = EditorRequest(user=user)
    if len(text.strip()) > 20:
        submission.description = text

    submission.save()
    return JsonResponse({'success':'successful', 'result':'Your request have been submitted, admins will review it.'})

        
    
        



        

    





    



