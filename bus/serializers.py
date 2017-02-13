from rest_framework import serializers
from .models import Reclamacao


class ReclamacaoSerializers(serializers.ModelSerializer):
	class Meta:
		model = Reclamacao
		fields = ('id','user','texto','img')