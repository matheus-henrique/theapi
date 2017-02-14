from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime


from rest_framework.response import Response

from .models import Reclamacao,Veiculo,Linha
from .serializers import ReclamacaoSerializers,LinhaSerializers
from rest_framework.decorators import api_view

import requests
import json
import time


init = datetime.now().minute # 20

proxies = {
    	"http": "http://matheus.oliveira:bv0sdq2wbx@proxy.tre-pi.gov.br:3128/",
    	"https": "https://matheus.oliveira:bv0sdq2wbx@proxy.tre-pi.gov.br:3128/",
	}
dados = {"email": "matheusbynickzinho@hotmail.com", "password": "bv0sdq2wb8"}
cb = {"Content-Type": "application/json", "Accept-Language": "en", "Date": "Wed, 13 Apr 2016 12:07:37 GMT", "X-Api-Key":"b4dadc9bd9284ea9afcc5889ba80f04a"}

def pegar_token():
	print("dadasd")
	return requests.post('https://api.inthegra.strans.teresina.pi.gov.br/v1/signin',proxies=proxies, data=json.dumps(dados),headers = cb)

token = pegar_token()
cb['X-Auth-Token'] = json.loads(token.text)['token']
#print(token.text)
#print(token.text)

# Create your views here.


@api_view(['GET', 'POST'])
def reclamacoes(request):
	if request.method == 'GET':
		reclamacoes = Reclamacao.objects.all()
		print(reclamacoes)
		serializer = ReclamacaoSerializers(reclamacoes, many=True)
		print(serializer)
		return Response(serializer.data)

@api_view(['GET', 'POST'])
def linhas(request):
	if request.method == 'GET':
		linha = Linha.objects.all()
		serializer = LinhaSerializers(linha, many=True)
		return Response(serializer.data)


def post_list(request):
	global token
	now = datetime.now().minute
	#print(init)
	#print(now)
	if (now - init >= 9):
		token = pegar_token()
	else:
		print("Nao precisa de nova requisicao")

	return HttpResponse(token.text)


def todos_veiculos(request,pk):
	url = "https://api.inthegra.strans.teresina.pi.gov.br/v1/"
	busca = request.GET.get('busca')
	if busca is None:
		url += pk
	else:
		url += pk + "?" + "busca=" + busca 
	data = requests.get(url,proxies=proxies, data=json.dumps(dados),headers = cb)

	vec = json.loads(data.text)
	linha = ''
	veiculo = ''
	print(vec)
	for x in vec:
		if Linha.objects.filter(CodigoLinha=x['Linha']['CodigoLinha']).exists():
			linha = Linha.objects.get(CodigoLinha=x['Linha']['CodigoLinha'])
		else:
			linha = Linha.objects.create(CodigoLinha=x['Linha']['CodigoLinha'],Origem=x['Linha']['Origem'],Retorno=x['Linha']['Retorno'],Denomicao=x['Linha']['Denomicao'])

		for y in x['Linha']['Veiculos']:
			if Veiculo.objects.filter(CodigoVeiculo=y['CodigoVeiculo']).exists():
				veiculo = Veiculo.objects.get(CodigoVeiculo=y['CodigoVeiculo'])
				veiculo.Lat = y['Lat']
				veiculo.Long = y['Long']
				veiculo.Hora = y['Hora']
				veiculo.save()
			else:
				veiculo = Veiculo.objects.create(CodigoVeiculo=y['CodigoVeiculo'],Lat=y['Lat'],Long=y['Long'],Hora=y['Hora'],Linha=linha)
	return HttpResponse(data.text)

@api_view(['GET', 'POST'])
def veiculo_especifico(request,pk):
	print("aqui")
	if request.method == 'GET':
		linha = Linha.objects.filter(CodigoLinha=pk)
		serializer = LinhaSerializers(linha, many=True)
		return Response(serializer.data)