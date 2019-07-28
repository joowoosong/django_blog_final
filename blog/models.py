from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=200)
    writer = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published')
    body = models.TextField()
    user = models.ManyToManyField(User, blank=True)

    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:100]
    def title_summary(self):
        if len(self.title) > 30:
            return self.title[:30] + '...'
        else:
            return self.title


class Comment(models.Model):
    writer = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField('Date published', auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

