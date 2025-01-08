from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import MD5PasswordHasher
from datetime import datetime



class UserModels(AbstractUser):
    last_name = None
    first_name = None
    name = models.CharField(max_length=256)
    id = models.CharField(verbose_name='username',primary_key=True, max_length=10,editable=False, null=False, blank=False)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        related_name='group',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        related_name='permisions',
        blank=True
    )
    
class Validate(models.Manager):
    def validate(self, token=None):
        exist = super().filter(token=MD5PasswordHasher().encode(password=token, salt='secrettoken')) # type: ignore
        if exist:
            exists = exist.values()[0]
            
            if datetime.now().isoformat() <= exists.get('end_time').isoformat(): # type: ignore
                return exist, True
            else:
                exist.delete()
        return [],False
    
class ResetPassword(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, blank=False, null=False)
    user_id = models.ForeignKey('simple.UserModels', on_delete=models.CASCADE)
    token = models.CharField(unique=True, editable=False, null=False, blank=False, max_length=50)
    end_time = models.DateTimeField(null=False, blank=False)
    objects = Validate()
    