from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Note(models.Model):
    """
    Note model to store each user's notes.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)
    # Optional fields for tags/folders/favorite/archived
    folder = models.CharField(max_length=255, blank=True, default="")
    is_favorite = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.owner.username})"
