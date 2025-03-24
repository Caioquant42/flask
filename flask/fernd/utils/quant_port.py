#from django.shortcuts import render

import pandas as pd
import numpy as np
import random
#import wget
from zipfile import ZipFile
from time import sleep

from numpy.linalg import multi_dot
import time
import yfinance as yf
from sklearn.cluster import KMeans
#import matplotlib.pyplot as plt
import json 

import warnings

warnings.filterwarnings('ignore')


def encontraClusters(carteira, nclusters = 4, period_ret = 1, plotOn = True):
    
    retornos=100*carteira.pct_change(period_ret)
    
    stocks=retornos.columns

    X=100*np.array([[np.std(retornos[sto]), np.mean(retornos[sto])] for sto in stocks])

    N=nclusters

    kmeans = KMeans(n_clusters=N, random_state=0).fit(X)
    y_kmeans = kmeans.predict(X)
    '''
    if plotOn: 
        fig = plt.subplots(figsize=(20,10))

        ax1=plt.subplot(1,1, 1) 
        ax1.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
        ax1.set_title('Retornos de '+str(len(stocks))+' Ações do Índice Amplo',fontsize=20)
        ax1.set_xlabel('Risco [%]',fontsize=25)
        ax1.set_ylabel('Retorno [%]',fontsize=25)
    '''
    centers = kmeans.cluster_centers_
    #if plotOn:   
    #    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=150, alpha=0.2);

    best=[]
    for i in range(N):
        ind=retornos[retornos.columns[np.where(y_kmeans==i)[0]]].mean()/retornos[retornos.columns[np.where(y_kmeans==i)[0]]].std()
        best.append(ind[ind==np.max(ind)])
    rb=list(pd.DataFrame(best).columns)
    print("Ativos com Melhor Relação em Cada Cluster:", rb)
    
    #if plotOn:
        #for r in rb:
        #    plt.text(X[stocks==r][0][0],X[stocks==r][0][1],r,fontsize=15)
    
    return rb



def simulacaoMelhoresAtivosClusters(carteira, nret = 20, list_clust = [4,7,10,20]):
    lista_ativos = []
    for i in range(1,nret):
        for j in list_clust:
            lista_ativos.append(encontraClusters(carteira=carteira, nclusters = j, period_ret = i, plotOn = False))
    di = dict(calculaQtdRepetidaDeAtivos(lista_ativos))
    sort_dict= dict(sorted(di.items(), key=lambda item: item[1], reverse=True)) 
    return sort_dict

def calculaQtdRepetidaDeAtivos(lista_ativos):
    # avalia numa lista de listas de ativos a quantidade que um nome de ativo aparece
    # arquivo proveniente do modelo de k-means
    total = []
    for i in lista_ativos:
        for j in i:
            total.append(j)
    from collections import Counter
    r = Counter(total)
    sort_dict= dict(sorted(dict(r).items(), key=lambda item: item[1], reverse=True)) 
    return sort_dict


def calculaValorIntrinsecoGrahamSiteFundamentos(ativos, indice_graham = 22.5):
    # ativos - lista com os nomes de ativos
    # ´válido apenas para empresas que possuem grande patrimonio 
    # empresas de TI nao funciona devido baixo patrimonio liquido e grande investimentos (graham não viveu na era da info)
    # Graham considera P/L máximo de 15 e P/VP de 1.5 - 15*1.5 = 22.5 (para a geração de vida de Graham)
    resp = []
    for a in ativos:
        print("Baixando dados do ativo = "+a)
        url = "https://www.fundamentus.com.br/detalhes.php?papel="+a
        resposta = requests.get(url,headers=agent)
        soup = BeautifulSoup(resposta.text,'lxml')
        table = soup.find_all('table')
        df = pd.read_html(str(table), decimal=',', thousands='.')
        tb = df[2]
        P_L = float(tb.iloc[1,3])
        P_VP = float(tb.iloc[2,3])
        LPA = float(tb.iloc[1,5])
        VPA = float(tb.iloc[2,5])
        VI = np.sqrt(indice_graham * LPA*VPA)
        
        resp.append([a,VI,P_L,P_VP,LPA,VPA])
        time.sleep(1)
    dr = pd.DataFrame(resp,columns=['Ativo','ValorIntrinseco','P/L','P/VP','LPA','VPA'])
    return dr

def transformaDictToDataFrame(di, leg=['Ativo','Qtd']):
    da = di.items()
    return pd.DataFrame(list(da),columns = leg)

#/*--------
def calculaQtdRepetidaDeAtivos(lista_ativos):
    # avalia numa lista de listas de ativos a quantidade que um nome de ativo aparece
    # arquivo proveniente do modelo de k-means
    total = []
    for i in lista_ativos:
        for j in i:
            total.append(j)
    from collections import Counter
    r = Counter(total)
    sort_dict= dict(sorted(dict(r).items(), key=lambda item: item[1], reverse=True)) 
    return sort_dict

def simulacaoMelhoresAtivosMonteCarlo(dados, ret = 1, sim_MC = 500, tam_port = 7, plotOn=False):
    # a df deve conter o ativo BOVA11 ou IND ou WIND para motivos de comparação
    #plt.rcParams["figure.figsize"] = (20,10)
    df = dados.copy()
    nome_ibov = [a for a in df.columns if(a.startswith("BOVA") or a.startswith("WIN") or a.startswith("IND"))][0]
    p_ibov = df[nome_ibov]
    p_ibov = p_ibov / p_ibov.iloc[0] # normalizando
    
    if len(nome_ibov)>4:
        
        df.drop(nome_ibov, inplace=True, axis=1) # remover o ibov da carteira 
    else:
        print("O ativo BOVA11 não está contido dentro da massa de dados!")
    d = df.copy()
    retorno = df.pct_change(ret)
    ret_sumcum = retorno.cumsum()
    ret_sumcum.iloc[0] = d.iloc[0]
    
    # Estou com dúvida aqui embaixo ... pq ele nao utilizou o cumsum() mas sim cumprod()????
    retorno_acumulado = (1 + retorno).cumprod()
    retorno_acumulado.iloc[0] = 1
    
    carteira_saldo = {}

    for i in range(sim_MC):
      carteira = random.sample( list(d.columns) , k=tam_port) # tam_port - dita os sorteios dos nomes dos portfolios
      carteira = 10000 * retorno_acumulado.loc[: , carteira]
      carteira['saldo'] = carteira.sum(axis=1)
      #if (plotOn):
      #  plt.plot(carteira['saldo'])
              
            #carteira['saldo'].plot() #figsize=(18,8)
        
      carteira_saldo[carteira['saldo'][-1]] = list(carteira.columns) # posso simplificar isso apenas para um df
    
    #if (plotOn):

    #(p_ibov*10000*tam_port).plot() #linewidth=4,color='black'
      #plt.plot(p_ibov*10000*tam_port,linewidth=4,color='black')
      
    #plt.show()
    
    # total de carteiras acima do IBOV
    port_acima_ibov = []
    ret_ibov = p_ibov[-1]*10000*tam_port
    
    sort_keys= sorted(carteira_saldo.keys(), reverse=True) # nao precisamos dessa ordenação
    
    cont = 0
    for i in sort_keys:
        if i > ret_ibov:
            #print(carteira_saldo[i])
            cont = cont + 1
            port_acima_ibov.append(carteira_saldo[i])
    
    # os 5 melhores portfólios
    top_5 = pd.DataFrame()
    for i in sort_keys[:6]:
        top_5[i] = carteira_saldo[i]
    top_5 = top_5.iloc[:-1,:] # retirar a ultima linha q possui legenda 'saldo'
    
    freq = calculaQtdRepetidaDeAtivos(port_acima_ibov)
    #plt.legend()
    print('Tam Port = '+str(tam_port)+', retorno = '+str(ret)+', Tivermos '+str(cont)+' portfólios acima do IBOV de um total de '+str(sim_MC))
    
    return carteira_saldo, port_acima_ibov, freq, top_5

def mlnsupport(data, nret_ = 20, list_clust_ = [3,4,5]):
    c1 = simulacaoMelhoresAtivosClusters(data, nret = nret_, list_clust = list_clust_)

    # Ordena ativos
    sort_orders = sorted(c1.items(), key=lambda x: x[1], reverse=True)

    #print(sort_orders)

    df_res = pd.DataFrame(sort_orders, columns=['ATIVO','FREQ'])
    #json_mlnsupport = df_res.to_json(orient='records')
    
    return df_res.to_dict(orient='records')


def mcport(data, ret = 5, n_sim_mc = 1200, tam_port_ = 4):
    carteira_saldo, port_acima_ibov, freq, top_5 = simulacaoMelhoresAtivosMonteCarlo(data, ret = ret, 
                                                                                     sim_MC = n_sim_mc, 
                                                                                     tam_port = tam_port_)
    res_dict = {"carteira_saldo":carteira_saldo,
                "freq":freq,"top_5":top_5.to_dict(orient='records')}
    


    json_mcport = freq  #json.dumps(res_dict, indent=4)

    return json_mcport