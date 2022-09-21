from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField

class candidat(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    description = models.TextField()
    github = models.URLField(max_length=200)
    linkedin = models.URLField(max_length=200)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "confer_candidat"


class recruteur(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    societe = models.CharField(max_length=100)
    photo = models.ImageField(default="profile.jpg",null=True ,blank=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "confer_recrutement"


class offre(models.Model):
    recruteur = models.ForeignKey(recruteur,null=True,on_delete=models.CASCADE)
    salaire = models.FloatField()
    annonce = models.TextField()
    date_publication = models.DateField()
    deadline = models.DateField()
    question = models.TextField()
    extraction = models.JSONField(null=True)

    class Meta:
        db_table = "confer_offre"


class submit(models.Model):
    offre = models.ForeignKey(offre,null=True,on_delete=models.CASCADE)
    candidat = models.ForeignKey(candidat,null=True,on_delete=models.CASCADE)
    cv = models.FileField(upload_to='pdf')
    cv_extraction = models.JSONField(null=True)
    res_cv = models.FloatField(null=True)
    test = models.TextField()
    res_test = models.FloatField(null=True)
    res_photo = models.FloatField(null=True)
    video = models.FileField(upload_to='mp4')
    res_video = models.FloatField(null=True)
    rank = models.FloatField(null=True)

    class Meta:
        db_table = "confer_submit"

# Create your models here.
