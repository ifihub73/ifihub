from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class EditorRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_editor_request')
    description = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def save(self):
        user = self.user
        user.is_editor = True
        user.save()
        super().save()
        
