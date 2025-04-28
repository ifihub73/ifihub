from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now


User = get_user_model()

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_blogs')
    snippet = models.CharField(max_length=2000, blank=True, null=True)
    content = models.TextField()
    public = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class File(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    file = models.FileField(upload_to='blogfiles')

    def __str__(self):
        return self.file.name
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.blog.title} -- {self.comment}'
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_likes')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.blog} --- {self.user}'
    


    

