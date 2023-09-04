from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name




class Article(models.Model):
    slug = models.SlugField(unique=True,max_length=200,blank=True)
    title = models.CharField(max_length=255)
    content = RichTextField()  
    Categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    keywords = models.CharField(help_text='coma separeted every keyword',max_length=255,blank=True)
    meta = models.TextField()
    image = models.ImageField(upload_to='articles_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    