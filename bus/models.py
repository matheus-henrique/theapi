from django.db import models
from django import forms
# Create your models here.


class Reclamacao(models.Model):
	user = models.ForeignKey('auth.User')
	texto = models.TextField()
	img = models.FileField()