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

class users(models.Model):
    gender = models.IntegerField()
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

class users_saved_package(models.Model):
    pack_id = models.ForeignKey(package_db,on_delete=models.CASCADE)
    email_user = models.CharField(max_length=100)
    timestamp = models.DateTimeField(max_length=100)

class users_download_package(models.Model):
    pack_id = models.ForeignKey(package_db,on_delete=models.CASCADE)
    version_id = models.CharField(max_length=100)
    email_user = models.CharField(max_length=100)
    timestamp = models.DateTimeField(max_length=100, auto_now=True)

class carousel_home_slider(models.Model):
    visible = models.IntegerField()
    img_src = models.CharField(max_length=100)
    line_1st = models.CharField(max_length=100)
    line_2nd = models.CharField(max_length=100)
    bck_rgba = models.CharField(max_length=100)
    url_txt = models.CharField(max_length=100)
    url_class = models.CharField(max_length=100)
    url_link = models.CharField(max_length=100)
    url_visible = models.IntegerField()

class package_collection(models.Model):
    NameCollection = models.CharField(max_length=100)
    IT_Name = models.CharField(max_length=100)
    IT_Desc = models.CharField(max_length=100)
    image_cover = models.CharField(max_length=100)

class package_collection_join(models.Model):
    package_id = models.ForeignKey(package_db,on_delete=models.CASCADE)
    collection_id = models.ForeignKey(package_collection, on_delete=models.CASCADE)