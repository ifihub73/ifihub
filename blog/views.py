from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.views.decorators.http import require_http_methods
from django.conf import settings


from .models import Blog

def index(request):
    return render(request, 'blog/index.html', {'message':''})

# Create your views here.

def check_authenticated(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error':'you are not logged in'})
    else:
         user = request.user
         return JsonResponse({'success':'authenticated', 'id':user.pk, 'firstname':user.first_name, 'lastname':user.last_name, 'is_verified':user.is_verified, 'is_editor':user.is_editor})


#blog create home
def create_blog_home(request):
        if not request.user.is_authenticated:
            return render(request, 'blog/index.html', {'message':'you are not logged in'})
        
        if not request.user.is_editor:
            return render(request, 'blog/index.html', {'message':'you are not an editor'})
        
        if request.user.first_name.strip() == '':
            print('create a profile before proceeding')
            return render(request, 'blog/index.html', {'message':'create a profile before proceeding'})

        return render(request, 'blog/createBlog.html')


#submit blog 
@require_http_methods(['POST'])
def create_blog(request):
     user = request.user
     if not user.is_authenticated:
          return JsonResponse({'error':'you must be logged in to perform this operation'})
     
     if not user.is_editor:
          return JsonResponse({'error':'you are not authorized  to make this request '})
     
     if user.first_name.strip() == '':
        return JsonResponse({'error':'create a profile before proceeding'})
     
     title = request.POST.get('title')
     content = request.POST.get('content')

     if len(title.strip()) < 5:
          return JsonResponse({'error':'title is too short'})
     
     if len(content.strip()) < 20:
          return JsonResponse({'error':'content is too short'})
     

     snipet = f"{content.split('</p>')[0]}</p>"

     blog = Blog(title=title, snippet=snipet, content=content, author=user)

     if request.POST.get('visibility') and request.POST.get('visibility') == 'public':
          blog.public = True

     blog.save()

     return JsonResponse({'success':{'id':blog.pk, 'author':blog.author.first_name, 'author_id':blog.author.pk}})    




#upload image 

import traceback


@csrf_exempt
def upload_image(request):
    try:
        if request.method == "POST" and request.FILES.get("upload"):
            image = request.FILES["upload"]
            saved_path = default_storage.save(f"uploads/{image.name}", image)
            print("✅ Image saved to:", saved_path)
            return JsonResponse({
                "url": f"{settings.MEDIA_URL}{saved_path}"
            })
        return JsonResponse({"error": "Upload failed. No file."}, status=400)
    except Exception as e:
        print("❌ Upload failed with error:")
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
    
#view all blogs
def view_all(request):
     blogs = Blog.objects.filter(public=True).select_related('author').prefetch_related('blog_likes').prefetch_related('blog_comments').order_by('-time')
     filtered = [
          {
             'id': blog.pk,
             'title':blog.title, 
             'date':blog.time, 
             'author':f"{blog.author.first_name} {blog.author.last_name if blog.author.last_name.strip() != '' else '...'}",
             'likes': blog.blog_likes.count(),
             'comments': blog.blog_comments.count(),
             'content': f"{blog.snippet.split('</p>')[0]}  .....</p>"
          } 
          for blog in blogs
     ]
     return render(request, 'blog/viewBlog.html', {'blogs':filtered})

#view one
from django.db.models import Prefetch
from .models import Like, Comment
def view_one(request, pk):
     try:
          blog = Blog.objects.prefetch_related(
               Prefetch(
                    'blog_likes',
                    queryset= Like.objects.select_related('user')
               ),
               Prefetch(
                    'blog_comments',
                    queryset= Comment.objects.select_related('user')
               )

          ).get(pk=pk, public=True)
     except Blog.DoesNotExist:
          return render(request, 'blog/oneBlog.html', {'found':False})

     filtered = {
          'id':blog.pk,
          'title':blog.title,
          'content': blog.content,
          'date':blog.time,
          'likes_count':blog.blog_likes.count(),
          'likes': [
               name.user.first_name if name.user.first_name != '' else 'UnNamed' for name in blog.blog_likes.all()
          ], 
          'comments_count':blog.blog_comments.count(),
          'comments': [
               {'user':name.user.first_name if name.user.first_name != '' else 'UnNamed', 'comment':name.comment} for name in blog.blog_comments.all()
          ],
          'author':f"{blog.author.first_name}{blog.author.last_name if blog.author.last_name else ''}",
          'author_id': blog.author.pk
          
     }
     return render(request, 'blog/oneBlog.html', {'found':True, 'data':filtered}) 

#like a post
@require_http_methods(['POST'])
def like_post(request, pk):
     user = request.user
     if not user.is_authenticated:
          return JsonResponse({'error':'you are not logged in'})
     
     try:
          blog = Blog.objects.get(pk=pk, public=True)
     except Blog.DoesNotExist:
          return JsonResponse({'error':'Blog not found'})
     
     if Like.objects.filter(user=user, blog=blog).exists():
          Like.objects.filter(user=user,blog=blog).delete()
          result = blog.blog_likes.select_related('user').all()
          return JsonResponse({'success':'successful', 'liked':False, 'value':blog.blog_likes.count(), 'likes':[name.user.first_name if name.user.first_name.strip() != '' else 'UnNamed' for name in result]})
     
     else:
          Like.objects.create(blog=blog, user=user)
          result = blog.blog_likes.select_related('user').all()
          return JsonResponse({'success':'successful', 'liked':True, 'value':blog.blog_likes.count(), 'likes':[name.user.first_name if name.user.first_name.strip() != '' else 'UnNamed' for name in result]})
     

# save a comment
@require_http_methods(['POST'])
def make_comment(request, pk):
     user = request.user
     if not user.is_authenticated:
          return JsonResponse({'error':'unauthenticated user'})
     comment = request.POST.get('comment')
     if not comment or len(comment.strip()) < 2:
          return JsonResponse({'error':'invalid comment'})
     
     try:
          blog = Blog.objects.get(pk=pk)
     except Blog.DoesNotExist:
          return JsonResponse({'error':'blog data not found'})
     
     Comment.objects.create(user=user, blog=blog, comment=comment)

     comments = blog.blog_comments.select_related('user').all().order_by('-time')

     return JsonResponse({'success':'successful', 'count':comments.count(), 'comment':[{'user':name.user.first_name if name.user.first_name.strip() != '' else 'UnNamed', 'comment':name.comment }for name in comments]})