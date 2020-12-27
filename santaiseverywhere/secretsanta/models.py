from django.db import models
from django.contrib.auth.models import User 
from django.utils.text import slugify 
from django.urls import reverse

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField()
    budget = models.PositiveIntegerField(blank=False,default=20)
    description = models.TextField(blank=True,null=True)
    users = models.ManyToManyField(User,blank=True)
    password = models.CharField(max_length=256)
    masterPassword = models.CharField(max_length=256,default=password)
    active = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.name


    def save(self,*args,**kwargs) -> None:
        self.slug = slugify(self.name,self.password)
        return super().save(*args,**kwargs)


    class ActiveManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(active=True)

    activeRooms = ActiveManager()
    objects = models.Manager()


    def get_absolute_url(self):
        return reverse('room_password',args=[self.id])