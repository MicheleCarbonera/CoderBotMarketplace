from django.db import models

# Create your models here.
class package_db(models.Model):
    NamePackage = models.CharField(max_length=100)
    IT_Name = models.CharField(max_length=100)
    IT_Desc = models.CharField(max_length=500)
    image_cover = models.CharField(max_length=500)
    Category = models.IntegerField()

# Create your models here.
class package_category(models.Model):
    NameCategory = models.CharField(max_length=100)
    IT_NameCategory = models.CharField(max_length=100)

class package_version(models.Model):
    id_package = models.IntegerField()
    version = models.CharField(max_length=100)
    timeupload = models.DateTimeField(max_length=100)
    downloadcount = models.IntegerField()