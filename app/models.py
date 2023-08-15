import environ, os, ast
from cryptography.fernet import Fernet
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.utils.text import slugify

    
class Stage(models.Model):
    stage_name = models.CharField(max_length = 150)
    parent=models.ForeignKey('self', blank=True, null=True, related_name='stage_children', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, blank=True)
    stage_index = models.IntegerField(blank=True, null=True)
    #stage_dependens_on = models.ForeignKey('app.Answer', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.stage_name
    
    class Meta:
        ordering = ['stage_index']
    

    def save(self, *args, **kwargs):
        if self.stage_name:
            self.slug=slugify(self.stage_name.replace('ı','i').replace('ə','e').replace('ö','o').replace('ü','u').replace('ç','c')\
                              .replace("I", "I").replace('Ə','E').replace('Ö','O').replace('Ü','U').replace('Ç','C'))
            
        return super().save(*args, **kwargs)
            
