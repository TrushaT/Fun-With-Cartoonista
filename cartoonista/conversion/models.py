from django.db import models
from taggit.managers import TaggableManager



class Post(models.Model):
    title = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    pub_date = models.DateField(auto_now_add=True)
    #slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()

    def __str__(self):
        return self.title
    

    