from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from model.customer import Customer
from schemas.customer_schema import CustomerBuscaSchema, CustomerSchema, CustomerViewSchema, apresenta_customer, apresenta_customers
from schemas.error_schema import ErrorSchema
from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Customer API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
customer_tag = Tag(name="Clientes", description="Adição, visualização, remoção e predição de clientes de serviço de internet")


# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota de listagem de clientes
@app.get('/customers', tags=[customer_tag],
         responses={"200": CustomerViewSchema, "404": ErrorSchema})
def get_customers():
    """Lista todos os clientes cadastrados na base
    Args:
       none
        
    Returns:
        list: lista de clientes cadastrados na base
    """
    logger.debug("Coletando dados sobre todos os clientes")
    # Criando conexão com a base
    session = Session()
    # Buscando todos os pacientes
    customer = session.query(Customer).all()
    
    if not customer:
        # Se não houver pacientes
        return {"customers": []}, 200
    else:
        logger.debug(f"%d pacientes econtrados" % len(customer))
        print(customer)
        return apresenta_customers(customer), 200


# Rota de adição de cliente
@app.post('/customer', tags=[customer_tag],
          responses={"200": CustomerViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: CustomerSchema):
    """Adiciona um novo cliente à base de dados
    Retorna uma representação dos clientes e diagnósticos associados.
    """
        
    # Preparando os dados para o modelo
    X_input = PreProcessador.preparar_form(form)
    # Carregando modelo
    model_path = './MachineLearning/models/model.pkl'
    # modelo = Model.carrega_modelo(ml_path)
    modelo = Pipeline.carrega_pipeline(model_path)
    # Realizando a predição
    outcome = int(Model.realiza_predicao(modelo, X_input)[0])
    
    customer = Customer(
        name=form.name,
        age=form.age,
        gender=form.gender,
        tenure=form.tenure,
        monthly_charges=form.monthly_charges,
        contract_type=form.contract_type,
        internet_service=form.internet_service,
        total_charges=form.total_charges,
        tech_support=form.tech_support,
        churn=outcome
    )
    logger.debug(f"Adicionando cliente de nome: '{customer.name}'")
    
    try:
        # Criando conexão com a base
        session = Session()
        
        # Checando se cliente já existe na base
        if session.query(Customer).filter(Customer.name == form.name).first():
            error_msg = "Cliente já existente na base :/"
            logger.warning(f"Erro ao adicionar Cliente '{customer.name}', {error_msg}")
            return {"message": error_msg}, 409
        
        # Adicionando paciente
        session.add(customer)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado paciente de nome: '{customer.name}'")
        return apresenta_customer(customer), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cliente '{customer.name}', {error_msg}")
        return {"message": error_msg}, 400
    

# Métodos baseados em nome
# Rota de busca de clentes por nome
@app.get('/customer', tags=[customer_tag],
         responses={"200": CustomerViewSchema, "404": ErrorSchema})
def get_customer(query: CustomerBuscaSchema):    
    """Faz a busca por um cliente cadastrado na base a partir do nome

    Args:
        nome (str): nome do cliente
        
    Returns:
        dict: representação do paciente e diagnóstico associado
    """
    
    customer_nome = query.name
    logger.debug(f"Coletando dados sobre produto #{customer_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    customer = session.query(Customer).filter(Customer.name == customer_nome).first()
    
    if not customer:
        # se o cliente não foi encontrado
        error_msg = f"Cliente {customer_nome} não encontrado na base :/"
        logger.warning(f"Erro ao buscar cliente '{customer_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Cliente econtrado: '{customer.name}'")
        # retorna a representação do paciente
        return apresenta_customer(customer), 200
   
    
# Rota de remoção de paciente por nome
@app.delete('/customer', tags=[customer_tag],
            responses={"200": CustomerViewSchema, "404": ErrorSchema})
def delete_customer(query: CustomerBuscaSchema):
    """Remove um cliente cadastrado na base a partir do nome

    Args:
        nome (str): nome do paciente
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    
    customer_nome = unquote(query.name)
    logger.debug(f"Deletando dados sobre cliente #{customer_nome}")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando paciente
    custumer = session.query(Customer).filter(Customer.name == customer_nome).first()
    
    if not custumer:
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao deletar cliente '{customer_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(custumer)
        session.commit()
        logger.debug(f"Deletado cliente #{customer_nome}")
        return {"message": f"Cliente {customer_nome} removido com sucesso!"}, 200
    
if __name__ == '__main__':
    app.run(debug=True)