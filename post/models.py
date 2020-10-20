from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse
from PIL import Image
from cartoonify.models import Image as Img

class Post(models.Model):
    title = models.CharField(max_length = 250)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    header_image = models.ImageField(upload_to = 'posts')
    caption  = models.TextField(max_length=500)
    pub_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=100,default='general')
    tags = TaggableManager()
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    
    def __str__(self):
        return self.title + '|' + str(self.author)

    def get_absolute_url(self):
        return reverse('detail_post', kwargs={"pk":self.id})

    def get_like_url(self):
        return reverse('like-toggle', kwargs={"pk":self.id})
    
    def get_api_like_url(self):
        return reverse('like-api-toggle', kwargs={"pk":self.id})

    




    