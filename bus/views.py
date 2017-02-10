from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

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

# Create your views here.
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


def post_detail(request,pk):
	url = "https://api.inthegra.strans.teresina.pi.gov.br/v1/"
	busca = request.GET.get('busca')
	if busca is None:
		url += pk
	else:
		url += pk + "?" + "busca=" + busca 
	data = requests.get(url,proxies=proxies, data=json.dumps(dados),headers = cb)

	#print(url)
	#print(busca)
	return HttpResponse(data.text)