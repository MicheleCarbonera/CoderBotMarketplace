from django.db import models

# Create your models here.
class package_db(models.Model):
    NamePackage = models.CharField(max_length=100)
    IT_Name = models.CharField(max_length=100)
    IT_Desc = models.CharField(max_length=500)
    image_cover = models.CharField(max_length=500)