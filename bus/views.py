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



cadeirantes = ['02194','02200','02196','02186','02148','02555','02128','02501','02563','02511','02521','02134','02773','04391','04402','04415','04451','04435','04349','04372','04401',
'04433','04366','04388','04441','04443','04417','04454','04431','04379','04385','04397','04446','04387','04374','04453','03404','04411','04380','04381','03257','03250','03067','03258',
'03429','03068','03468','03071','03234','03239','03254','01056','01073','01087','01072','01379','03405','03237','01076','01071','01381','01067','01080','01090','01065','01408',
'01220','01077','01393','01405','01074','04425','04365','04351','04398','04414','04452','03065','03066','03026','03448','03445','03454','03460','03451','03457','03469','03472','03416',
'03425','03437','03461','03406','03435','03447','03433','03403','03471','03455','03401','03417','03450','03422','03466','03459','03465','04410','04421','04438','04448','04371','04352',
'04390','04450','04362','04436','04439','01075','01402','01372','01396','01400','01387','01309','01070','01054','04429','04423','04428','04337','04406','04447','02529','02777','02525',
'02551','02789','02531','02782','02527','03072','03037','02783','02774','02788','02559','02519','02509','02505','02198','02212','02204','04407','04424','04358','04440','04404','04449',
'04412','04419','04422','04367','04455','04392','04361','04355','04369','04378','04413','04354','02784','02523','01059','01132','01397','01078','03251','04444','04399','04360','04382',
'04426','04395','04299','04347','01385','01378','01386','04364','04396','04356','04353','02130','02778','04393','02780','02781','04370','04430','04368','04389','01398','01390','01053',
'02190','02557','02547','04445','04357','04405','03069','03070','03242','04427','04376','03418','03462','04442','04386','02549','02553','02776','03233','01066','01069','01089','02154',
'02152','02202','02214','02150','02503','02775','04437','04408','04348','04363','02182','02188','02210','04350','04432','04400','03456','03432','03444','04434','04359','04384','04409',
'03430','02507','03255','04403','03412','04406','03074']
sem_info = ['04373','04338','04341','04333','01349','00198','00157','00183','00172','00197','00176','00194','00189','00145','00173','']
ar = ['02563','04451','04454','04446','04453','03258','03468','04452','03469','03472','03461','03471','03466','03465','04448','04450','04447','04449','04455','04444','04445','03462','03074']



print(len(cadeirantes))

def pegar_token():
	print("dadasd")
	data = requests.post('https://api.inthegra.strans.teresina.pi.gov.br/v1/signin',proxies=proxies, data=json.dumps(dados),headers = cb)
	cb['X-Auth-Token'] = json.loads(data.text)['token']
	return data

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
	verifica_token()
	url = "https://api.inthegra.strans.teresina.pi.gov.br/v1/veiculos"
	data = requests.get(url,proxies=proxies, data=json.dumps(dados),headers = cb)

	vec = json.loads(data.text)
	linha = ''
	veiculo = ''


	for x in vec:
		if Linha.objects.filter(CodigoLinha=x['Linha']['CodigoLinha']).exists():
			linha = Linha.objects.get(CodigoLinha=x['Linha']['CodigoLinha'])
		else:
			num = str(x['Linha']['CodigoLinha'])
			zona = LinhaOnibus.objects.filter(Numero=num[1::])
			if(zona.exists()):
				nome_zona = zona[0].Zona
			else:
				nome_zona = "Outros"
				print("Nao existe : " + num)

			

			linha = Linha.objects.create(CodigoLinha=x['Linha']['CodigoLinha'],Origem=x['Linha']['Origem'],Retorno=x['Linha']['Retorno'],Denomicao=x['Linha']['Denomicao'], Zona=nome_zona)

		for y in x['Linha']['Veiculos']:
			adptado = verifica_onibus_adaptado(y['CodigoVeiculo'])
			if Veiculo.objects.filter(CodigoVeiculo=y['CodigoVeiculo']).exists():
				veiculo = Veiculo.objects.get(CodigoVeiculo=y['CodigoVeiculo'])
				veiculo.Lat = y['Lat']
				veiculo.Long = y['Long']
				veiculo.Hora = y['Hora']
				veiculo.save()
			else:
				veiculo = Veiculo.objects.create(CodigoVeiculo=y['CodigoVeiculo'],Lat=y['Lat'],Long=y['Long'],Hora=y['Hora'],Linha=linha,Cadeirante=adptado)		
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



def distancia_onibus_user(request):
	url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=-5.082728,-42.799080&destinations=-5.096149,-42.757065&mode=bicycling&language=pt-BR&key=AIzaSyAXjVVb85BzbZ3GRIFH6rO2WGmBylGG-0c"
	data = requests.get(url,proxies=proxies)
	return HttpResponse(data.text)




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
			lin[index]['CodigoLinha'] == '0710' or lin[index]['CodigoLinha'] == '0004' or lin[index]['CodigoLinha'] == '0327'):
				print("Sudeste")
				zona = "Sudeste"
				s = s + 1;

		if( lin[index]['CodigoLinha'] == '0245' or lin[index]['CodigoLinha'] == '0401' or lin[index]['CodigoLinha'] == '0402' or 
			lin[index]['CodigoLinha'] == '0403' or lin[index]['CodigoLinha'] == '0404' or lin[index]['CodigoLinha'] == '0405' or 
			lin[index]['CodigoLinha'] == '0406' or lin[index]['CodigoLinha'] == '0501' or lin[index]['CodigoLinha'] == '0502' or 
			lin[index]['CodigoLinha'] == '0503' or lin[index]['CodigoLinha'] == '0512' or lin[index]['CodigoLinha'] == '0513' or 
			lin[index]['CodigoLinha'] == '0518' or lin[index]['CodigoLinha'] == '0521' or lin[index]['CodigoLinha'] == '0522' or
			lin[index]['CodigoLinha'] == '0523' or lin[index]['CodigoLinha'] == '0610' or lin[index]['CodigoLinha'] == '0365'):
				print("leste")
				zona = "Leste"
				l = l + 1;

		if( lin[index]['CodigoLinha'] == '0101' or lin[index]['CodigoLinha'] == '0106' or lin[index]['CodigoLinha'] == '0202' or 
			lin[index]['CodigoLinha'] == '0102' or lin[index]['CodigoLinha'] == '0107' or lin[index]['CodigoLinha'] == '0203' or 
			lin[index]['CodigoLinha'] == '0103' or lin[index]['CodigoLinha'] == '0108' or lin[index]['CodigoLinha'] == '0204' or 
			lin[index]['CodigoLinha'] == '0104' or lin[index]['CodigoLinha'] == '0109' or lin[index]['CodigoLinha'] == '0205' or 
			lin[index]['CodigoLinha'] == '0105' or lin[index]['CodigoLinha'] == '0201' or lin[index]['CodigoLinha'] == '0206' or
			lin[index]['CodigoLinha'] == '0301' or lin[index]['CodigoLinha'] == '0302' or lin[index]['CodigoLinha'] == '0303' or
			lin[index]['CodigoLinha'] == '0304' or lin[index]['CodigoLinha'] == '0730' or lin[index]['CodigoLinha'] == '0563'):
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
			lin[index]['CodigoLinha'] == '0901' or lin[index]['CodigoLinha'] == '0902' or lin[index]['CodigoLinha'] == '0360' or
			lin[index]['CodigoLinha'] == '0723' or lin[index]['CodigoLinha'] == '0170' or lin[index]['CodigoLinha'] == '0270' or
			lin[index]['CodigoLinha'] == '716'):
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

		
		if(not(zona == '')):
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

			if(LinhaOnibus.objects.filter(Numero=codigo).exists()):
				print("Ja Existe")
			else:
				LinhaOnibus.objects.create(Numero=codigo,Denomicao=lin[index]['Denomicao'],Zona=zona)
		index = index + 1
	print("Sudeste "+ str(s))
	print("Leste "+str(l))
	print("Norte "+str(n))
	print("Sul "+str(su))
	print("Terminal "+str(t))


	return HttpResponse("Ok")

def verifica_onibus_adaptado(num):
	for i in cadeirantes:
		if (i == num):
			return True
	return False


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
				if verifica_onibus_adaptado(['CodigoVeiculo']):
					veiculo = Veiculo.objects.create(CodigoVeiculo=y['CodigoVeiculo'],Lat=y['Lat'],Long=y['Long'],Hora=y['Hora'],Linha=linha,Cadeirante=True)
				else:
					veiculo = Veiculo.objects.create(CodigoVeiculo=y['CodigoVeiculo'],Lat=y['Lat'],Long=y['Long'],Hora=y['Hora'],Linha=linha,Cadeirante=False)
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