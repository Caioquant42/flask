from flask import Flask, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np
import yfinance as yf

from utils.quant_port import mcport, mlnsupport

# 
sym = ['BOVA11.SA','PRIO3.SA', 'PETR3.SA', 'CASH3.SA', 'POSI3.SA', 'MRFG3.SA', "JBSS3.SA", 'ITUB4.SA','VALE3.SA']



# Criar um DataFrame com números aleatórios (4 colunas, 100 linhas)
data = np.random.rand(100, 4)  # 100 linhas e 4 colunas com números aleatórios
columns = ['col1', 'col2', 'col3', 'col4']
df = pd.DataFrame(data, columns=columns)

# Visualizar o DataFrame
print(df.head())  # Exibindo as primeiras linhas do DataFrame

# Salvar em um arquivo CSV (caso queira testar os dados)
df.to_csv('random_data.csv', index=False)


app = Flask(__name__)
CORS(app)  # Isso permitirá que o React acesse a API Flask

@app.route('/api/datacsv', methods=['GET'])
def get_data_csv():
    # Carregar os dados do arquivo CSV
    df = pd.read_csv('random_data.csv')

    # Converter o DataFrame para um dicionário de listas
    data = df.to_dict(orient='records')

    # Retornar os dados como resposta JSON
    return jsonify(data)

@app.route('/api/data', methods=['GET'])
def get_data():
    # Dados simulados
    data = [
        {"col1": f"Row {i+1} Col1", "col2": f"Row {i+1} Col2", "col3": f"Row {i+1} Col3", "col4": f"Row {i+1} Col4"}
        for i in range(20)
    ]
    return jsonify(data)

@app.route('/api/data2', methods=['GET'])
def get_data2():
    # Dados simulados
    data = [
        {"col1": f"Row {i+1} Col1", "col2": f"Row {i+1} Col2"}
        for i in range(20)
    ]
    return jsonify(data)


@app.route('/api/mcport', methods=['GET'])
def get_mcport():
    # Obtem dados da simulação de Monte Carlo - Carteira quant
    # Download ativos ibovespa 
    try:

        da = yf.download(sym,period='1y')['Close'] # Virá do dolphindb
        r = mcport(da, ret = 5, n_sim_mc = 1200, tam_port_ = 4)
    except:
        r = {}
    return jsonify(r)

@app.route('/api/mlnsupport', methods=['GET'])  # machine learning não supervisionado portfolio
def get_mlnsupport():
    # Download ativos ibovespa 
    try:
        da = yf.download(sym,period='1y')['Close'] # Virá do dolphindb
        r = mlnsupport(da, nret_ = 20, list_clust_ = [3,4,5])
    except:
        r = {}
    return jsonify(r)






if __name__ == "__main__":
    app.run(debug=True)