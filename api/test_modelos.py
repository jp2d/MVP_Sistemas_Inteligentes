from model import *

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

def converter_para_float(valor_str):
    return float(valor_str.replace(",", "."))

# Parâmetros    
url_dados = "./MachineLearning/data/customer_churn_data.csv"
colunas = ['age', 'gender', 'tenure', 'monthly_charges', 'contract_type', 'internet_service', 'total_charges', 'tech_support', 'churn']

# Carga dos dados
dataset = Carregador.carregar_dados(url_dados, colunas)

dataset['monthly_charges'] = dataset['monthly_charges'].apply(converter_para_float)
dataset['total_charges'] = dataset['total_charges'].apply(converter_para_float)

array = dataset.values
X = array[:,0:-1]
y = array[:,-1]
    
# Método para testar o modelo de Regressão Logística a partir do arquivo correspondente
# O nome do método a ser testado necessita começar com "test_"
def test_modelo():  
    # Importando o modelo de regressão logística
    path = './MachineLearning/models/model.pkl'
    modelo = Model.carrega_modelo(path)

    # Obtendo as métricas da Regressão Logística
    acuracia = Avaliador.avaliar(modelo, X, y)
    
    # Testando 
    assert acuracia >= 0.78 
