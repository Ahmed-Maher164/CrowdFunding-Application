from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
# Create your models here.

class Users(AbstractBaseUser):
    phone_regex = RegexValidator(regex=r'^01[1|0|2|5][0-9]{8}$',message='phone must be an egyptian phone number...')
    first_name = models.CharField(verbose_name="first_name" ,null=False, max_length=50)
    last_name = models.CharField(verbose_name= "last_name" ,null=False, max_length=50)
    email = models.EmailField(verbose_name='email', null=False, max_length=254,unique=True)
    phone = models.CharField(verbose_name="phone",null=True,validators=[phone_regex],max_length=14)
    photo = models.ImageField(verbose_name="photo",upload_to='images')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone','email']
