# petitions/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class MoviePetition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    class Meta:
        app_label = 'petitions'  
    
    def __str__(self):
        return self.title
    
    def vote_count(self):
        return self.votes.count()

class Vote(models.Model):
    petition = models.ForeignKey(MoviePetition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        app_label = 'petitions'
        unique_together = ('petition', 'user')  # Prevent duplicate votes
