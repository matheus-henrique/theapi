from rest_framework import serializers
from .models import Reclamacao,Veiculo,Linha


class ReclamacaoSerializers(serializers.ModelSerializer):
	class Meta:
		model = Reclamacao
		fields = ('id','user','texto','img')


class VeiculoSerializers(serializers.ModelSerializer):
	class Meta:
		model = Veiculo
		fields = ('CodigoVeiculo','Lat','Long','Hora')

class LinhaSerializers(serializers.ModelSerializer):
	Veiculos = VeiculoSerializers(many=True)
	class Meta:
		model = Linha
		fields = ('CodigoLinha','Origem','Retorno','Denomicao','Veiculos')




