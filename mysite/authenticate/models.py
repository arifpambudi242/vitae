from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# The table that would be created -> AppName_ModelName: authenticate_system_user
#class SystemUser(models.Model):
#    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
#    address_1 = models.CharField(max_length=256, blank=True)
#    address_2 = models.CharField(max_length=256, blank=True)
#    suburb = models.CharField(max_length=100, blank=True)
#    postcode = models.CharField(max_length=10, blank=True)
#    state = models.CharField(max_length=100, blank=True)
#    country = models.CharField(max_length=100, blank=True)
#    phone = models.CharField(max_length=20, blank=True)

#    def __str__(self):
#        return self.user.username
    
#    class Meta:
#        verbose_name = 'System User'
#        verbose_name_plural = 'System Users'

categories = (("Computer", "Computer"), ("Litature", "Litature"), ("Science", "Science"), ("Math", "Math"), ("History", "History"), ("Geography", "Geography"), ("Art", "Art"), ("Music", "Music"), ("Sport", "Sport"), ("Other", "Other"))


class User(AbstractUser):
    address_1 = models.CharField(max_length=256)
    address_2 = models.CharField(max_length=256, blank=True)
    suburb = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    content = models.TextField()
    category = models.CharField(max_length=100, choices=categories, default="Other")
    tags = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title + ' ' + self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'Response'
        verbose_name_plural = 'Responses'