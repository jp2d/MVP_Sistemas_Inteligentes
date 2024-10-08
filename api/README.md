# Projeto MVP API

Este pequeno projeto é o MVP da disciplina **Qualidade de Software, Segurança e Sistemas Inteligentes** 

O objetivo é criar uma pequena POC (`Proof of consept`) de um sistema de aprendizado de máquina com o conteúdo apresentado nas disciplinas.

---
## Como executar 


O sistema foi desenvolvido em Python 3.12.6.

> É fortemente indicado o uso de ambiente virtual utilize o comando:

```
 python -m venv env
```

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas em um ambiente virtual.

```
(env)$ pip install -r requirements.txt
```

Para executar o teste basta executar:

```
(env)$ pytest -v test_modelos.py
```

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.