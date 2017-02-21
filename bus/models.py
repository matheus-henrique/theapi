from django.db import models
from django import forms
# Create your models here.


class Reclamacao(models.Model):
	user = models.ForeignKey('auth.User')
	texto = models.TextField()
	img = models.FileField()


class Linha(models.Model):
	CodigoLinha = models.CharField(max_length=10)
	Origem = models.CharField(max_length=200)
	Retorno = models.CharField(max_length=200)
	Denomicao = models.CharField(max_length=200)


class Veiculo(models.Model):
	CodigoVeiculo = models.CharField(max_length=10)
	Lat = models.CharField(max_length=30)
	Long = models.CharField(max_length=30)
	Hora = models.CharField(max_length=30)
	Linha = models.ForeignKey(Linha,related_name='Veiculos')
	Cadeirante = models.BooleanField(default=False)

class LinhaOnibus(models.Model):
	Numero = models.CharField(max_length=30)
	Denomicao = models.CharField(max_length=200)
	Zona = models.CharField(max_length=200)
