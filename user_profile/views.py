from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from blog.models import *

# Create your views here.
#utils functions
User =get_user_model()

def calculate_likes(blogs):
    total = 0
    for i in blogs:
        total += i.blog_likes.count()

    return total

def calculate_comments(blogs):
    total = 0
    for i in blogs:
        total += i.blog_comments.count()

    return total


#profile home
def index(request):
    profiles = User.objects.filter(is_editor=True)
    data = [{'first_name':profile.first_name, 'id':profile.pk} for profile in profiles]
    return render(request, 'user_profile/index.html', {'error':'', 'profiles':data})





# view profile function
def view_profile(request, pk):
    requesting_user = request.user
    try:
        user = User.objects.prefetch_related(
            Prefetch(
                'user_blogs',
                queryset= Blog.objects.prefetch_related('blog_likes').prefetch_related('blog_comments')
            ),
        ).get(pk=pk)
    except User.DoesNotExist:
        return render(request, 'user_profile/index.html', {'error':'the user no longer exist'})

    if not user.is_editor:
        return render(request, 'user_profile/index.html', {'error':'You are not authorised'})
    
    if user.first_name.strip() == '':
        return render(request, 'user_profile/index.html', {'error':'Unverified User'})


    data = {
        'first_name': user.first_name,
        'last_name': user.last_name if user.last_name.strip() != '' else '',
        'total_blogs': user.user_blogs.count(),
        'total_likes': calculate_likes(user.user_blogs.filter(public=True)),
        'total_comments': calculate_comments(user.user_blogs.filter(public=True)),
        'all_blogs': [{'title':blog.title, 'id':blog.pk, 'snippet':f"{blog.snippet.split('</p>')[0]}...</p>", 'total_likes':blog.blog_likes.count(), 'total_comments':blog.blog_comments.count(), 'date':blog.time} for blog in user.user_blogs.filter(public=True).order_by('-time')]
    }
    if requesting_user == user:
        data.update({'pending_blogs': user.user_blogs.filter(public=False).count()})
        data.update({'id': user.pk})
        data.update({'is_user': True})

    return render(request, 'user_profile/userProfile.html', {'data':data})

#edit profile Home
def edit_profile_home(request, pk):
    requesting_user = request.user
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return render(request, 'user_profile/editProfileHome.html', {'error':'Unauthorised Access'})

    if user != requesting_user:
        return render(request, 'user_profile/editProfileHome.html', {'error':'Unauthorised Access'})

    if not user.is_authenticated:
        return render(request, 'user_profile/editProfileHome.html', {'error':'Unauthorised Access'})

    if not user.is_editor:
        return render(request, 'user_profile/editProfileHome.html', {'error':'You are not Verified'})

    return render(request, 'user_profile/editProfileHome.html', {'error':'','id':user.pk})
    