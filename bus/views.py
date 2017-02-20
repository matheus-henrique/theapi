from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime


from rest_framework.response import Response

from .models import Reclamacao,Veiculo,Linha,LinhaOnibus
from .serializers import ReclamacaoSerializers,LinhaSerializers,LinhaOnibusSerializers
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

def verifica_token():
	global token
	now = datetime.now().minute
	if (now - init >= 9):
		token = pegar_token()
	else:
		print("Nao precisa de nova requisicao")


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
	if (now - init >= 9):
		token = pegar_token()
	else:
		print("Nao precisa de nova requisicao")

	return HttpResponse(token.text)



def linhas_estaticas(request):
	verifica_token()
	url = "https://api.inthegra.strans.teresina.pi.gov.br/v1/linhas"
	data = requests.get(url,proxies=proxies, data=json.dumps(dados),headers = cb)
	lin = json.loads(data.text)
	index = 0;
	s = 0;
	l = 0;
	n = 0;
	su = 0;
	t = 0;
	for x in lin:
		zona = '';
		if (lin[index]['CodigoLinha'] == '0100' or lin[index]['CodigoLinha'] == '0504' or lin[index]['CodigoLinha'] == '0505' or 
			lin[index]['CodigoLinha'] == '0506' or lin[index]['CodigoLinha'] == '0507' or lin[index]['CodigoLinha'] == '0508' or 
			lin[index]['CodigoLinha'] == '0509' or lin[index]['CodigoLinha'] == '0510' or lin[index]['CodigoLinha'] == '0515' or 
			lin[index]['CodigoLinha'] == '0516' or lin[index]['CodigoLinha'] == '0517' or lin[index]['CodigoLinha'] == '0519' or 
			lin[index]['CodigoLinha'] == '0520' or lin[index]['CodigoLinha'] == '0601' or lin[index]['CodigoLinha'] == '0602' or 
			lin[index]['CodigoLinha'] == '0603' or lin[index]['CodigoLinha'] == '0604' or lin[index]['CodigoLinha'] == '0611' or 
			lin[index]['CodigoLinha'] == '0612' or lin[index]['CodigoLinha'] == '0619' or lin[index]['CodigoLinha'] == '0702' or 
			lin[index]['CodigoLinha'] == '0703' or lin[index]['CodigoLinha'] == '0704' or lin[index]['CodigoLinha'] == '0705' or 
			lin[index]['CodigoLinha'] == '0710' or lin[index]['CodigoLinha'] == '0004'):
				print("Sudeste")
				zona = "Sudeste"
				s = s + 1;

		if( lin[index]['CodigoLinha'] == '0245' or lin[index]['CodigoLinha'] == '0401' or lin[index]['CodigoLinha'] == '0402' or 
			lin[index]['CodigoLinha'] == '0403' or lin[index]['CodigoLinha'] == '0404' or lin[index]['CodigoLinha'] == '0405' or 
			lin[index]['CodigoLinha'] == '0406' or lin[index]['CodigoLinha'] == '0501' or lin[index]['CodigoLinha'] == '0502' or 
			lin[index]['CodigoLinha'] == '0503' or lin[index]['CodigoLinha'] == '0512' or lin[index]['CodigoLinha'] == '0513' or 
			lin[index]['CodigoLinha'] == '0518' or lin[index]['CodigoLinha'] == '0521' or lin[index]['CodigoLinha'] == '0522' or
			lin[index]['CodigoLinha'] == '0523' or lin[index]['CodigoLinha'] == '0610'):
				print("leste")
				zona = "Leste"
				l = l + 1;

		if( lin[index]['CodigoLinha'] == '0101' or lin[index]['CodigoLinha'] == '0106' or lin[index]['CodigoLinha'] == '0202' or 
			lin[index]['CodigoLinha'] == '0102' or lin[index]['CodigoLinha'] == '0107' or lin[index]['CodigoLinha'] == '0203' or 
			lin[index]['CodigoLinha'] == '0103' or lin[index]['CodigoLinha'] == '0108' or lin[index]['CodigoLinha'] == '0204' or 
			lin[index]['CodigoLinha'] == '0104' or lin[index]['CodigoLinha'] == '0109' or lin[index]['CodigoLinha'] == '0205' or 
			lin[index]['CodigoLinha'] == '0105' or lin[index]['CodigoLinha'] == '0201' or lin[index]['CodigoLinha'] == '0206' or
			lin[index]['CodigoLinha'] == '0301' or lin[index]['CodigoLinha'] == '0302' or lin[index]['CodigoLinha'] == '0303' or
			lin[index]['CodigoLinha'] == '0304' or lin[index]['CodigoLinha'] == '0730'):
				print("norte")
				zona = "Norte"
				n = n + 1;
		if( lin[index]['CodigoLinha'] == '0605' or lin[index]['CodigoLinha'] == '0606' or lin[index]['CodigoLinha'] == '0607' or 
			lin[index]['CodigoLinha'] == '0608' or lin[index]['CodigoLinha'] == '0609' or lin[index]['CodigoLinha'] == '0613' or 
			lin[index]['CodigoLinha'] == '0614' or lin[index]['CodigoLinha'] == '0615' or lin[index]['CodigoLinha'] == '0616' or 
			lin[index]['CodigoLinha'] == '0617' or lin[index]['CodigoLinha'] == '0618' or lin[index]['CodigoLinha'] == '0620' or
			lin[index]['CodigoLinha'] == '0621' or lin[index]['CodigoLinha'] == '0622' or lin[index]['CodigoLinha'] == '0623' or
			lin[index]['CodigoLinha'] == '0624' or lin[index]['CodigoLinha'] == '0625' or lin[index]['CodigoLinha'] == '0626' or
			lin[index]['CodigoLinha'] == '0627' or lin[index]['CodigoLinha'] == '0688' or lin[index]['CodigoLinha'] == '0706' or
			lin[index]['CodigoLinha'] == '0709' or lin[index]['CodigoLinha'] == '0711' or lin[index]['CodigoLinha'] == '0712' or
			lin[index]['CodigoLinha'] == '0713' or lin[index]['CodigoLinha'] == '0714' or lin[index]['CodigoLinha'] == '0715' or
			lin[index]['CodigoLinha'] == '0716' or lin[index]['CodigoLinha'] == '0801' or lin[index]['CodigoLinha'] == '0802' or
			lin[index]['CodigoLinha'] == '0901' or lin[index]['CodigoLinha'] == '0902'):
				print("sul")
				zona = "Sul"
				su = su + 1;
		if( lin[index]['CodigoLinha'] == 'A602' or lin[index]['CodigoLinha'] == 'T501' or lin[index]['CodigoLinha'] == 'A604' or 
			lin[index]['CodigoLinha'] == 'A601' or lin[index]['CodigoLinha'] == 'A505' or lin[index]['CodigoLinha'] == 'A504' or 
			lin[index]['CodigoLinha'] == 'T503' or lin[index]['CodigoLinha'] == 'T502' or lin[index]['CodigoLinha'] == 'T602' or 
			lin[index]['CodigoLinha'] == 'A503' or lin[index]['CodigoLinha'] == 'A502' or lin[index]['CodigoLinha'] == 'A531' or
			lin[index]['CodigoLinha'] == 'T531' or lin[index]['CodigoLinha'] == 'A535' or lin[index]['CodigoLinha'] == 'T532' or
			lin[index]['CodigoLinha'] == 'A534' or lin[index]['CodigoLinha'] == 'A532' or lin[index]['CodigoLinha'] == 'T533' or
			lin[index]['CodigoLinha'] == 'IT01' or lin[index]['CodigoLinha'] == 'A501' or lin[index]['CodigoLinha'] == 'A632' or
			lin[index]['CodigoLinha'] == 'T632' or lin[index]['CodigoLinha'] == 'A634' or lin[index]['CodigoLinha'] == 'A631' or
			lin[index]['CodigoLinha'] == 'T631' or lin[index]['CodigoLinha'] == 'A537' or lin[index]['CodigoLinha'] == 'IT02' or
			lin[index]['CodigoLinha'] == 'A638' or lin[index]['CodigoLinha'] == 'A538' or lin[index]['CodigoLinha'] == 'A637' or
			lin[index]['CodigoLinha'] == 'A636' or lin[index]['CodigoLinha'] == 'A536' or lin[index]['CodigoLinha'] == 'TRLV001'):
				print("terminal")
				zona = "Terminal"
				t = t + 1;

		if (zona == ''):
			LinhaOnibus.objects.create(Numero=lin[index]['CodigoLinha'],Denomicao=lin[index]['Denomicao'],Zona="Outros")
		else:
			numero = str(lin[index]['CodigoLinha'])
			codigo = ''
			i = 0;
			if (not( zona == "Terminal")):
				for x in numero:
					if (i > 0):
						codigo = codigo + x
					i = i + 1;

				print(codigo)
			else:
				codigo = lin[index]['CodigoLinha']


			LinhaOnibus.objects.create(Numero=codigo,Denomicao=lin[index]['Denomicao'],Zona=zona)
		index = index + 1
	print("Sudeste "+ str(s))
	print("Leste "+str(l))
	print("Norte "+str(n))
	print("Sul "+str(su))
	print("Terminal "+str(t))

	return HttpResponse("Ok")


def todos_veiculos(request,pk):
	verifica_token()
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
def todas_linhas_estaticas(request):
	verifica_token()
	if request.method == 'GET':
		linha = LinhaOnibus.objects.all()
		serializer = LinhaOnibusSerializers(linha, many=True)
		return Response(serializer.data)

@api_view(['GET', 'POST'])
def veiculo_especifico(request,pk):
	print("aqui")
	verifica_token()
	if request.method == 'GET':
		linha = Linha.objects.filter(CodigoLinha=pk)
		serializer = LinhaSerializers(linha, many=True)
		return Response(serializer.data)

@api_view(['GET', 'POST'])
def linhas_por_zona(request,pk):
	verifica_token()
	if request.method == 'GET':
		linha = LinhaOnibus.objects.filter(Zona=pk)
		serializer = LinhaOnibusSerializers(linha, many=True)
		return Response(serializer.data)