from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
#Модель для сохранения изображения
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_image')
    description = models.CharField(max_length = 100, blank=True)
    date_created = models.DateField(auto_now_add=True, db_index=True)
    title = models.CharField(max_length =100)
    slug = models.SlugField(blank=True, max_length=100)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    users_likes = models.ManyToManyField(User, related_name='images_like', blank=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse ('image_detail', kwargs = {'slug':self.slug, 'pk':self.pk})
#автоматичуское заполнение поля slug по полю title
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        return super(Image,self).save(*args, **kwargs)

# Create your models here.
